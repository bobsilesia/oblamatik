"""WebSocket support for real-time updates."""
import asyncio
import json
import logging
from typing import Any, Callable, Dict, Optional

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

class OblamatikWebSocket:
    """WebSocket client for real-time updates."""

    def __init__(self, hass: HomeAssistant, host: str, port: int = 80):
        """Initialize WebSocket client."""
        self._hass = hass
        self._host = host
        self._port = port
        self._ws_url = f"ws://{host}:{port}/ws"
        self._session = None
        self._websocket = None
        self._callbacks: Dict[str, Callable] = {}
        self._running = False
        self._reconnect_interval = 30  # seconds
        self._max_reconnect_attempts = 5

    async def connect(self) -> bool:
        """Connect to WebSocket."""
        try:
            self._session = async_get_clientsession()
            self._websocket = await self._session.ws_connect(
                self._ws_url,
                headers={"Origin": f"http://{self._host}:{self._port}"}
            )
            
            if self._websocket:
                self._running = True
                _LOGGER.info(f"Connected to WebSocket: {self._ws_url}")
                
                # Start listening task
                asyncio.create_task(self._listen())
                return True
            else:
                _LOGGER.error("Failed to connect to WebSocket")
                return False
                
        except Exception as e:
            _LOGGER.error(f"WebSocket connection error: {e}")
            return False

    async def disconnect(self):
        """Disconnect from WebSocket."""
        self._running = False
        if self._websocket:
            await self._websocket.close()
            self._websocket = None
        if self._session:
            await self._session.close()
            self._session = None
        _LOGGER.info("Disconnected from WebSocket")

    async def _listen(self):
        """Listen for WebSocket messages."""
        reconnect_attempts = 0
        
        while self._running and reconnect_attempts < self._max_reconnect_attempts:
            try:
                if self._websocket and not self._websocket.closed:
                    message = await self._websocket.receive()
                    if message:
                        await self._handle_message(message)
                        reconnect_attempts = 0  # Reset on successful message
                else:
                    _LOGGER.warning("WebSocket connection closed")
                    break
                    
            except Exception as e:
                _LOGGER.error(f"WebSocket error: {e}")
                reconnect_attempts += 1
                
                if reconnect_attempts < self._max_reconnect_attempts:
                    _LOGGER.info(f"Attempting to reconnect... ({reconnect_attempts}/{self._max_reconnect_attempts})")
                    await asyncio.sleep(self._reconnect_interval)
                    
                    # Try to reconnect
                    if await self.connect():
                        reconnect_attempts = 0
                    else:
                        break

        if reconnect_attempts >= self._max_reconnect_attempts:
            _LOGGER.error("Max reconnection attempts reached")
            await self.disconnect()

    async def _handle_message(self, message: str):
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(message)
            
            # Call registered callbacks
            for callback_name, callback in self._callbacks.items():
                if callback_name in data:
                    await callback(data[callback_name])
                    
        except json.JSONDecodeError as e:
            _LOGGER.error(f"Invalid JSON message: {e}")
        except Exception as e:
            _LOGGER.error(f"Error handling message: {e}")

    def register_callback(self, event_type: str, callback: Callable):
        """Register callback for specific event type."""
        self._callbacks[event_type] = callback

    def unregister_callback(self, event_type: str):
        """Unregister callback for specific event type."""
        if event_type in self._callbacks:
            del self._callbacks[event_type]

    async def send_message(self, message: Dict[str, Any]) -> bool:
        """Send message through WebSocket."""
        try:
            if self._websocket and not self._websocket.closed:
                await self._websocket.send_str(json.dumps(message))
                return True
            else:
                _LOGGER.warning("WebSocket not connected")
                return False
        except Exception as e:
            _LOGGER.error(f"Error sending message: {e}")
            return False

    @property
    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self._running and self._websocket and not self._websocket.closed


class OblamatikRealTimeUpdater:
    """Real-time updater for sensor values."""

    def __init__(self, hass: HomeAssistant, websocket: OblamatikWebSocket):
        """Initialize real-time updater."""
        self._hass = hass
        self._websocket = websocket
        self._sensor_callbacks: Dict[str, Callable] = {}
        
        # Register callbacks
        self._websocket.register_callback("sensor_update", self._handle_sensor_update)
        self._websocket.register_callback("device_state", self._handle_device_state)

    async def _handle_sensor_update(self, data: Dict[str, Any]):
        """Handle sensor update message."""
        try:
            # Update sensor entities in Home Assistant
            for sensor_id, value in data.items():
                if sensor_id in self._sensor_callbacks:
                    await self._sensor_callbacks[sensor_id](value)
                    
        except Exception as e:
            _LOGGER.error(f"Error handling sensor update: {e}")

    async def _handle_device_state(self, data: Dict[str, Any]):
        """Handle device state change."""
        try:
            # Handle device state changes
            state = data.get("state", "unknown")
            _LOGGER.info(f"Device state changed to: {state}")
            
            # Update all sensors
            for callback in self._sensor_callbacks.values():
                await callback()
                
        except Exception as e:
            _LOGGER.error(f"Error handling device state: {e}")

    def register_sensor_callback(self, sensor_id: str, callback: Callable):
        """Register callback for specific sensor."""
        self._sensor_callbacks[sensor_id] = callback

    def unregister_sensor_callback(self, sensor_id: str):
        """Unregister callback for specific sensor."""
        if sensor_id in self._sensor_callbacks:
            del self._sensor_callbacks[sensor_id]

    async def start(self):
        """Start real-time updates."""
        if await self._websocket.connect():
            _LOGGER.info("Real-time updates started")
        else:
            _LOGGER.error("Failed to start real-time updates")

    async def stop(self):
        """Stop real-time updates."""
        await self._websocket.disconnect()
        _LOGGER.info("Real-time updates stopped")

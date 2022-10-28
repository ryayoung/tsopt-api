# Maintainer:     Ryan Young
# Last Modified:  Oct 07, 2022
from hashlib import md5

def hash_to_int(text:str) -> int:
    digits = 13
    m = md5(text.encode('utf-8'))
    int_hash = int(m.hexdigest(), 16)
    shortened = str(int_hash)[:digits]
    return int(shortened)


import hashlib

def hashed(s):
    return hashlib.sha224(s).hexdigest()

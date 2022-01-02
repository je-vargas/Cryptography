import hashlib
import math
from string import ascii_letters
import itertools # --use this for permutations
import time
# ------------- Implementing SHA1 -------------

def sha1_encode(password):
    sha1 = hashlib.sha1(str.encode(password))
    return sha1.hexdigest()

print(sha1_encode("rong"))

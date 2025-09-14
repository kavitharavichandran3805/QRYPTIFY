import math

# rotate right input x, by n bits
def ROR(x, n, bits=32):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))

# rotate left input x, by n bits
def ROL(x, n, bits=32):
    return ROR(x, bits - n, bits)

# convert input sentence into 4 blocks of 32-bit binary
def blockConverter(sentence):
    encoded = []
    res = ""
    for i in range(len(sentence)):
        if i % 4 == 0 and i != 0:
            encoded.append(res)
            res = ""
        temp = bin(ord(sentence[i]))[2:]
        temp = temp.zfill(8)   # ensure 8 bits
        res += temp
    encoded.append(res)
    return encoded

# converts 4 blocks array of int into string
def deBlocker(blocks):
    s = ""
    for ele in blocks:
        temp = bin(ele)[2:].zfill(32)
        for i in range(4):
            s += chr(int(temp[i*8:(i+1)*8], 2))
    return s

# generate key schedule S[0...2r+3]
def generateKey(userkey):
    r = 12
    w = 32
    modulo = 2**32
    s = (2*r+4) * [0]
    s[0] = 0xB7E15163
    for i in range(1, 2*r+4):
        s[i] = (s[i-1] + 0x9E3779B9) % (2**w)

    encoded = blockConverter(userkey)
    enlength = len(encoded)
    l = enlength * [0]
    for i in range(1, enlength+1):
        l[enlength-i] = int(encoded[i-1], 2)

    v = 3 * max(enlength, 2*r+4)
    A = B = i = j = 0

    for _ in range(v):
        A = s[i] = ROL((s[i] + A + B) % modulo, 3, 32)
        B = l[j] = ROL((l[j] + A + B) % modulo, (A+B) % 32, 32)
        i = (i + 1) % (2*r + 4)
        j = (j + 1) % enlength
    return s

# PKCS7 padding
def pad(data, block_size=16):
    padding_len = block_size - (len(data) % block_size)
    return data + chr(padding_len) * padding_len

def unpad(data):
    padding_len = ord(data[-1])
    return data[:-padding_len]

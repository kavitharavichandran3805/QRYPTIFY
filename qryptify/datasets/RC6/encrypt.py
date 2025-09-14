from rc6 import *

def encrypt_block(sentence, s):
    encoded = blockConverter(sentence)
    A = int(encoded[0], 2)
    B = int(encoded[1], 2)
    C = int(encoded[2], 2)
    D = int(encoded[3], 2)

    r = 12
    w = 32
    modulo = 2**32
    lgw = 5

    B = (B + s[0]) % modulo
    D = (D + s[1]) % modulo
    for i in range(1, r+1):
        t = ROL((B * (2*B + 1)) % modulo, lgw, 32)
        u = ROL((D * (2*D + 1)) % modulo, lgw, 32)
        A = (ROL(A ^ t, u % 32, 32) + s[2*i]) % modulo
        C = (ROL(C ^ u, t % 32, 32) + s[2*i+1]) % modulo
        A, B, C, D = B, C, D, A
    A = (A + s[2*r+2]) % modulo
    C = (C + s[2*r+3]) % modulo

    return [A, B, C, D]

def encrypt(text, s):
    text = pad(text)  # PKCS7 padding
    ciphertext_blocks = []
    for i in range(0, len(text), 16):  # process 16-byte blocks
        block = text[i:i+16]
        cipher_block = encrypt_block(block, s)
        # convert integers -> bytes
        for val in cipher_block:
            ciphertext_blocks.append(val.to_bytes(4, 'big'))
    return b''.join(ciphertext_blocks).hex()

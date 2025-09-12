# #!/usr/bin/env python

# # A Python implementation of the block cipher IDEA

# # Copyright (c) 2015 Bo Zhu https://about.bozhu.me
# # MIT License


# def _mul(x, y):
#     assert 0 <= x <= 0xFFFF
#     assert 0 <= y <= 0xFFFF

#     if x == 0:
#         x = 0x10000
#     if y == 0:
#         y = 0x10000

#     r = (x * y) % 0x10001

#     if r == 0x10000:
#         r = 0

#     assert 0 <= r <= 0xFFFF
#     return r


# def _KA_layer(x1, x2, x3, x4, round_keys):
#     assert 0 <= x1 <= 0xFFFF
#     assert 0 <= x2 <= 0xFFFF
#     assert 0 <= x3 <= 0xFFFF
#     assert 0 <= x4 <= 0xFFFF
#     z1, z2, z3, z4 = round_keys[0:4]
#     assert 0 <= z1 <= 0xFFFF
#     assert 0 <= z2 <= 0xFFFF
#     assert 0 <= z3 <= 0xFFFF
#     assert 0 <= z4 <= 0xFFFF

#     y1 = _mul(x1, z1)
#     y2 = (x2 + z2) % 0x10000
#     y3 = (x3 + z3) % 0x10000
#     y4 = _mul(x4, z4)

#     return y1, y2, y3, y4


# def _MA_layer(y1, y2, y3, y4, round_keys):
#     assert 0 <= y1 <= 0xFFFF
#     assert 0 <= y2 <= 0xFFFF
#     assert 0 <= y3 <= 0xFFFF
#     assert 0 <= y4 <= 0xFFFF
#     z5, z6 = round_keys[4:6]
#     assert 0 <= z5 <= 0xFFFF
#     assert 0 <= z6 <= 0xFFFF

#     p = y1 ^ y3
#     q = y2 ^ y4

#     s = _mul(p, z5)
#     t = _mul((q + s) % 0x10000, z6)
#     u = (s + t) % 0x10000

#     x1 = y1 ^ t
#     x2 = y2 ^ u
#     x3 = y3 ^ t
#     x4 = y4 ^ u

#     return x1, x2, x3, x4


# class IDEA:
#     def __init__(self, key):
#         self._keys = None
#         self.change_key(key)

#     def change_key(self, key):
#         assert 0 <= key < (1 << 128)
#         modulus = 1 << 128

#         sub_keys = []
#         for i in range(9 * 6):
#             sub_keys.append((key >> (112 - 16 * (i % 8))) % 0x10000)
#             if i % 8 == 7:
#                 key = ((key << 25) | (key >> 103)) % modulus

#         keys = []
#         for i in range(9):
#             round_keys = sub_keys[6 * i: 6 * (i + 1)]
#             keys.append(tuple(round_keys))
#         self._keys = tuple(keys)

#     def encrypt(self, plaintext):
#         assert 0 <= plaintext < (1 << 64)
#         x1 = (plaintext >> 48) & 0xFFFF
#         x2 = (plaintext >> 32) & 0xFFFF
#         x3 = (plaintext >> 16) & 0xFFFF
#         x4 = plaintext & 0xFFFF

#         for i in range(8):
#             round_keys = self._keys[i]

#             y1, y2, y3, y4 = _KA_layer(x1, x2, x3, x4, round_keys)
#             x1, x2, x3, x4 = _MA_layer(y1, y2, y3, y4, round_keys)

#             x2, x3 = x3, x2

#         # Note: The words x2 and x3 are not permuted in the last round
#         # So here we use x1, x3, x2, x4 as input instead of x1, x2, x3, x4
#         # in order to cancel the last permutation x2, x3 = x3, x2
#         y1, y2, y3, y4 = _KA_layer(x1, x3, x2, x4, self._keys[8])

#         ciphertext = (y1 << 48) | (y2 << 32) | (y3 << 16) | y4
#         return ciphertext

#!/usr/bin/env python
# A Python implementation of the block cipher IDEA with wrapper
# Core by Bo Zhu (MIT License), Wrapper by [your project]

def _mul(x, y):
    assert 0 <= x <= 0xFFFF
    assert 0 <= y <= 0xFFFF

    if x == 0:
        x = 0x10000
    if y == 0:
        y = 0x10000

    r = (x * y) % 0x10001
    if r == 0x10000:
        r = 0

    return r


def _KA_layer(x1, x2, x3, x4, round_keys):
    z1, z2, z3, z4 = round_keys[0:4]

    y1 = _mul(x1, z1)
    y2 = (x2 + z2) % 0x10000
    y3 = (x3 + z3) % 0x10000
    y4 = _mul(x4, z4)

    return y1, y2, y3, y4


def _MA_layer(y1, y2, y3, y4, round_keys):
    z5, z6 = round_keys[4:6]

    p = y1 ^ y3
    q = y2 ^ y4

    s = _mul(p, z5)
    t = _mul((q + s) % 0x10000, z6)
    u = (s + t) % 0x10000

    x1 = y1 ^ t
    x2 = y2 ^ u
    x3 = y3 ^ t
    x4 = y4 ^ u

    return x1, x2, x3, x4


class IDEA:
    def __init__(self, key: int):
        self._keys = None
        self.change_key(key)

    def change_key(self, key: int):
        assert 0 <= key < (1 << 128)
        modulus = 1 << 128

        sub_keys = []
        for i in range(9 * 6):
            sub_keys.append((key >> (112 - 16 * (i % 8))) % 0x10000)
            if i % 8 == 7:
                key = ((key << 25) | (key >> 103)) % modulus

        keys = []
        for i in range(9):
            round_keys = sub_keys[6 * i: 6 * (i + 1)]
            keys.append(tuple(round_keys))
        self._keys = tuple(keys)

    def encrypt(self, plaintext: int) -> int:
        """Encrypt a 64-bit block (as integer)."""
        assert 0 <= plaintext < (1 << 64)
        x1 = (plaintext >> 48) & 0xFFFF
        x2 = (plaintext >> 32) & 0xFFFF
        x3 = (plaintext >> 16) & 0xFFFF
        x4 = plaintext & 0xFFFF

        for i in range(8):
            round_keys = self._keys[i]
            y1, y2, y3, y4 = _KA_layer(x1, x2, x3, x4, round_keys)
            x1, x2, x3, x4 = _MA_layer(y1, y2, y3, y4, round_keys)
            x2, x3 = x3, x2

        y1, y2, y3, y4 = _KA_layer(x1, x3, x2, x4, self._keys[8])
        ciphertext = (y1 << 48) | (y2 << 32) | (y3 << 16) | y4
        return ciphertext


# =====================================================
# Wrapper for handling bytes like AES/DES
# =====================================================
class IDEAWrapper:
    block_size = 8  # 64-bit blocks

    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("IDEA key must be 16 bytes (128 bits)")
        self.cipher = IDEA(int.from_bytes(key, "big"))

    def _pad(self, data: bytes) -> bytes:
        """PKCS#7 padding."""
        pad_len = self.block_size - (len(data) % self.block_size)
        return data + bytes([pad_len]) * pad_len

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt arbitrary-length plaintext (bytes)."""
        data = self._pad(data)
        ciphertext = b""
        for i in range(0, len(data), self.block_size):
            block = int.from_bytes(data[i:i+self.block_size], "big")
            enc_block = self.cipher.encrypt(block)
            ciphertext += enc_block.to_bytes(self.block_size, "big")
        return ciphertext





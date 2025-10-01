# import math
# import numpy as np
# import zlib
# from collections import Counter
# from scipy.stats import norm

# def feature_monobit_pvalue(bitstream: str) -> float:
#     """Approximate NIST monobit test p-value."""
#     if len(bitstream) == 0:
#         return 0
#     n = len(bitstream)
#     count_ones = bitstream.count('1')
#     s_obs = abs(count_ones - (n / 2)) / math.sqrt(n / 4)
#     p_value = 2 * (1 - norm.cdf(s_obs))
#     return p_value

# def feature_byte_pattern_freq(data: bytes, pattern: bytes) -> float:
#     """Frequency of a specific byte pattern in data"""
#     pattern_len = len(pattern)
#     if len(data) < pattern_len:
#         return 0
#     count = sum(1 for i in range(len(data) - pattern_len + 1) if data[i:i+pattern_len] == pattern)
#     return count / (len(data) - pattern_len + 1)


# # -----------------------
# # Helper: Decode Ciphertext (hex string → bytes)
# # -----------------------
# def decode_ciphertext(ciphertext: str) -> bytes:
#     """
#     Convert ciphertext from hex/base64/etc. into raw bytes.
#     Here we assume hex.
#     """
#     return bytes.fromhex(ciphertext)


# # -----------------------
# # Entropy Measures
# # -----------------------
# def feature_entropy(data: bytes) -> float:
#     """ Shannon entropy """
#     if len(data) == 0:
#         return 0
#     counts = Counter(data)
#     probs = [c / len(data) for c in counts.values()]
#     return -sum(p * math.log2(p) for p in probs)

# def feature_renyi(data: bytes, alpha=2) -> float:
#     """ Rényi entropy of order α (default α=2) """
#     if len(data) == 0:
#         return 0
#     counts = Counter(data)
#     probs = [c / len(data) for c in counts.values()]
#     return 1 / (1 - alpha) * math.log2(sum(p ** alpha for p in probs))

# def feature_minentropy(data: bytes) -> float:
#     """ Min-entropy: -log2(max probability) """
#     if len(data) == 0:
#         return 0
#     counts = Counter(data)
#     probs = [c / len(data) for c in counts.values()]
#     return -math.log2(max(probs))


# # -----------------------
# # Frequency & Chi-square
# # -----------------------
# def feature_chisquare(data: bytes) -> float:
#     """ Chi-square statistic for uniformity """
#     if len(data) == 0:
#         return 0
#     expected = len(data) / 256
#     counts = np.bincount(list(data), minlength=256)
#     return float(np.sum((counts - expected) ** 2 / expected))


# # -----------------------
# # Bit-Level Features
# # -----------------------
# def feature_runs(bitstream: str) -> int:
#     """ Count runs of consecutive bits """
#     if len(bitstream) == 0:
#         return 0
#     runs = 1
#     for i in range(1, len(bitstream)):
#         if bitstream[i] != bitstream[i - 1]:
#             runs += 1
#     return runs

# def feature_longest_run(bitstream: str) -> int:
#     """ Longest run of 1s or 0s """
#     if len(bitstream) == 0:
#         return 0
#     longest, current = 1, 1
#     for i in range(1, len(bitstream)):
#         if bitstream[i] == bitstream[i - 1]:
#             current += 1
#             longest = max(longest, current)
#         else:
#             current = 1
#     return longest

# def feature_serial_corr(bitstream: str) -> float:
#     """ Serial correlation of bits (lag=1) """
#     if len(bitstream) < 2:
#         return 0
#     bits = np.array([int(b) for b in bitstream])
#     return float(np.corrcoef(bits[:-1], bits[1:])[0, 1])


# # -----------------------
# # Compression-based Feature
# # -----------------------
# def feature_compression(data: bytes) -> float:
#     """ Compression ratio using zlib """
#     if len(data) == 0:
#         return 1.0
#     compressed = zlib.compress(data, level=9)
#     return len(compressed) / len(data)


# # -----------------------
# # Classical Crypto Stats
# # -----------------------
# def feature_ic(data: bytes) -> float:
#     """ Index of coincidence (IC) """
#     if len(data) == 0:
#         return 0
#     counts = Counter(data)
#     N = len(data)
#     numerator = sum(c * (c - 1) for c in counts.values())
#     denominator = N * (N - 1) if N > 1 else 1
#     return numerator / denominator

# def feature_autocorr(data: bytes, lag=1) -> float:
#     """ Byte-level autocorrelation with given lag """
#     if len(data) <= lag:
#         return 0
#     arr = np.frombuffer(data, dtype=np.uint8)
#     return float(np.corrcoef(arr[:-lag], arr[lag:])[0, 1])


# # -----------------------
# # Main Feature Extractor
# # -----------------------
# def extract_all_features(ciphertext: str) -> dict:
#     data = decode_ciphertext(ciphertext)
#     bitstream = ''.join(format(b, '08b') for b in data)
    
#     return {
#         # Structural
#         "Length": len(data),
#         "UniqueBytes": len(set(data)),
        
#         # Entropy
#         "Entropy": feature_entropy(data),
#         "RenyiEntropy": feature_renyi(data),
#         "MinEntropy": feature_minentropy(data),
        
#         # Frequency
#         "ChiSquare": feature_chisquare(data),
#         "ByteFreqVar": np.var(np.bincount(list(data), minlength=256)),
        
#         # Bit-level
#         "BitZeroFreq": bitstream.count("0") / len(bitstream) if len(bitstream) > 0 else 0,
#         "BitOneFreq": bitstream.count("1") / len(bitstream) if len(bitstream) > 0 else 0,
#         "Runs": feature_runs(bitstream),
#         "LongestRun": feature_longest_run(bitstream),
#         "SerialCorr": feature_serial_corr(bitstream),
        
#         # Compression
#         "ZlibRatio": feature_compression(data),
        
#         # Classical
#         "IndexCoincidence": feature_ic(data),
#         "Autocorr1": feature_autocorr(data, lag=1),
#         "Autocorr2": feature_autocorr(data, lag=2),

#         "MonobitPValue": feature_monobit_pvalue(bitstream),
#         "Freq_0x00": feature_byte_pattern_freq(data, b'\x00'),
#         "Freq_0xFFFF": feature_byte_pattern_freq(data, b'\xFF\xFF'),

#     }


# if __name__ == "__main__":
#     # Example ciphertext (hex string)
#     # You can replace this with your own ciphertext
#     sample_ciphertext = "6a2f9d1b8e5f4c2a7d9f3b1c"

#     # Extract features
#     features = extract_all_features(sample_ciphertext)

#     # Print all feature values with labels
#     print("\n=== Feature Extraction Results ===\n")
#     for k, v in features.items():
#         print(f"{k:20s}: {v}")


import math
import numpy as np
import zlib
from collections import Counter
from scipy.stats import norm
from numpy.fft import fft

# -----------------------
# Helper: Decode Ciphertext (hex string → bytes)
# -----------------------
def decode_ciphertext(ciphertext: str) -> bytes:
    """Convert ciphertext from hex into raw bytes."""
    return bytes.fromhex(ciphertext)

# -----------------------
# Entropy Measures
# -----------------------
def feature_entropy(data: bytes) -> float:
    if len(data) == 0: return 0
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def feature_renyi(data: bytes, alpha=2) -> float:
    if len(data) == 0: return 0
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return 1 / (1 - alpha) * math.log2(sum(p ** alpha for p in probs))

def feature_minentropy(data: bytes) -> float:
    if len(data) == 0: return 0
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return -math.log2(max(probs))

# -----------------------
# Frequency & Chi-square
# -----------------------
def feature_chisquare(data: bytes) -> float:
    if len(data) == 0: return 0
    expected = len(data) / 256
    counts = np.bincount(list(data), minlength=256)
    return float(np.sum((counts - expected) ** 2 / expected))

# -----------------------
# Bit-Level Features
# -----------------------
def feature_runs(bitstream: str) -> int:
    if len(bitstream) == 0: return 0
    runs = 1
    for i in range(1, len(bitstream)):
        if bitstream[i] != bitstream[i - 1]:
            runs += 1
    return runs

def feature_longest_run(bitstream: str) -> int:
    if len(bitstream) == 0: return 0
    longest, current = 1, 1
    for i in range(1, len(bitstream)):
        if bitstream[i] == bitstream[i - 1]:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest

def feature_serial_corr(bitstream: str) -> float:
    if len(bitstream) < 2: return 0
    bits = np.array([int(b) for b in bitstream])
    return float(np.corrcoef(bits[:-1], bits[1:])[0, 1])

# -----------------------
# Compression-based Feature
# -----------------------
def feature_compression(data: bytes) -> float:
    if len(data) == 0: return 1.0
    compressed = zlib.compress(data, level=9)
    return len(compressed) / len(data)

# -----------------------
# Classical Crypto Stats
# -----------------------
def feature_ic(data: bytes) -> float:
    if len(data) == 0: return 0
    counts = Counter(data)
    N = len(data)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = N * (N - 1) if N > 1 else 1
    return numerator / denominator

def feature_autocorr(data: bytes, lag=1) -> float:
    if len(data) <= lag: return 0
    arr = np.frombuffer(data, dtype=np.uint8)
    return float(np.corrcoef(arr[:-lag], arr[lag:])[0, 1])

# -----------------------
# NIST-style extra features
# -----------------------
def feature_monobit_pvalue(bitstream: str) -> float:
    if len(bitstream) == 0: return 0
    n = len(bitstream)
    count_ones = bitstream.count('1')
    s_obs = abs(count_ones - (n / 2)) / math.sqrt(n / 4)
    return 2 * (1 - norm.cdf(s_obs))

def feature_byte_pattern_freq(data: bytes, pattern: bytes) -> float:
    pattern_len = len(pattern)
    if len(data) < pattern_len: return 0
    count = sum(1 for i in range(len(data) - pattern_len + 1)
                if data[i:i+pattern_len] == pattern)
    return count / (len(data) - pattern_len + 1)

# -----------------------
# New Features
# -----------------------
def feature_repeated_blocks(data: bytes, block_size=16) -> float:
    """Fraction of repeated blocks (useful to detect ECB or small block ciphers)."""
    if len(data) < block_size: return 0
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    return 1 - len(set(blocks)) / len(blocks)

def feature_sliding_entropy(data: bytes, window=256) -> float:
    """Average entropy across sliding windows."""
    if len(data) < window: return feature_entropy(data)
    entropies = []
    for i in range(0, len(data) - window + 1, window):
        entropies.append(feature_entropy(data[i:i+window]))
    return float(np.mean(entropies))

def feature_fft_spectrum(bitstream: str, top_k=5) -> float:
    """FFT peak ratio (strong periodicity → higher value)."""
    if len(bitstream) < 32: return 0
    bits = np.array([int(b) for b in bitstream])
    spectrum = np.abs(fft(bits - np.mean(bits)))
    peaks = np.sort(spectrum[1:])[-top_k:]
    return float(np.mean(peaks) / np.mean(spectrum))

# -----------------------
# Main Feature Extractor
# -----------------------
def extract_all_features(ciphertext: str) -> dict:
    data = decode_ciphertext(ciphertext)
    bitstream = ''.join(format(b, '08b') for b in data)

    return {
        # Structural
        "Length": len(data),
        "UniqueBytes": len(set(data)),

        # Entropy
        "Entropy": feature_entropy(data),
        "RenyiEntropy": feature_renyi(data),
        "MinEntropy": feature_minentropy(data),

        # Frequency
        "ChiSquare": feature_chisquare(data),
        "ByteFreqVar": np.var(np.bincount(list(data), minlength=256)),

        # Bit-level
        "BitZeroFreq": bitstream.count("0") / len(bitstream) if len(bitstream) > 0 else 0,
        "BitOneFreq": bitstream.count("1") / len(bitstream) if len(bitstream) > 0 else 0,
        "Runs": feature_runs(bitstream),
        "LongestRun": feature_longest_run(bitstream),
        "SerialCorr": feature_serial_corr(bitstream),

        # Compression
        "ZlibRatio": feature_compression(data),

        # Classical
        "IndexCoincidence": feature_ic(data),
        "Autocorr1": feature_autocorr(data, lag=1),
        "Autocorr2": feature_autocorr(data, lag=2),

        # NIST-like
        "MonobitPValue": feature_monobit_pvalue(bitstream),
        "Freq_0x00": feature_byte_pattern_freq(data, b'\x00'),
        "Freq_0xFFFF": feature_byte_pattern_freq(data, b'\xFF\xFF'),

        # NEW Features
        "RepeatedBlocks16": feature_repeated_blocks(data, block_size=16),
        "RepeatedBlocks8": feature_repeated_blocks(data, block_size=8),
        "SlidingEntropy": feature_sliding_entropy(data, window=256),
        "FFTPeakRatio": feature_fft_spectrum(bitstream),
    }

# -----------------------
# Testing
# -----------------------
if __name__ == "__main__":
    sample_ciphertext = "6a2f9d1b8e5f4c2a7d9f3b1c"  # example hex string
    features = extract_all_features(sample_ciphertext)

    print("\n=== Extended Feature Extraction Results ===\n")
    for k, v in features.items():
        print(f"{k:20s}: {v}")

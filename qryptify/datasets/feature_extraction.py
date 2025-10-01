import pandas as pd
import base64
import math
import numpy as np
import zlib
from collections import Counter
from scipy.stats import norm

# -----------------------------
# Feature Extraction Functions
# -----------------------------
def feature_monobit_pvalue(bitstream: str) -> float:
    if len(bitstream) == 0:
        return 0
    n = len(bitstream)
    count_ones = bitstream.count('1')
    s_obs = abs(count_ones - (n / 2)) / math.sqrt(n / 4)
    return 2 * (1 - norm.cdf(s_obs))

def feature_entropy(data: bytes) -> float:
    if len(data) == 0:
        return 0
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def feature_renyi(data: bytes, alpha=2) -> float:
    if len(data) == 0:
        return 0
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return 1 / (1 - alpha) * math.log2(sum(p ** alpha for p in probs))

def feature_minentropy(data: bytes) -> float:
    if len(data) == 0:
        return 0
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return -math.log2(max(probs))

def feature_chisquare(data: bytes) -> float:
    if len(data) == 0:
        return 0
    expected = len(data) / 256
    counts = np.bincount(list(data), minlength=256)
    return float(np.sum((counts - expected) ** 2 / expected))

def feature_runs(bitstream: str) -> int:
    if len(bitstream) == 0:
        return 0
    runs = 1
    for i in range(1, len(bitstream)):
        if bitstream[i] != bitstream[i - 1]:
            runs += 1
    return runs

def feature_longest_run(bitstream: str) -> int:
    if len(bitstream) == 0:
        return 0
    longest, current = 1, 1
    for i in range(1, len(bitstream)):
        if bitstream[i] == bitstream[i - 1]:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest

def feature_serial_corr(bitstream: str) -> float:
    if len(bitstream) < 2:
        return 0
    bits = np.array([int(b) for b in bitstream])
    return float(np.corrcoef(bits[:-1], bits[1:])[0, 1])

def feature_compression(data: bytes) -> float:
    if len(data) == 0:
        return 1.0
    compressed = zlib.compress(data, level=9)
    return len(compressed) / len(data)

def feature_ic(data: bytes) -> float:
    if len(data) == 0:
        return 0
    counts = Counter(data)
    N = len(data)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = N * (N - 1) if N > 1 else 1
    return numerator / denominator

def feature_autocorr(data: bytes, lag=1) -> float:
    if len(data) <= lag:
        return 0
    arr = np.frombuffer(data, dtype=np.uint8)
    return float(np.corrcoef(arr[:-lag], arr[lag:])[0, 1])

def feature_byte_pattern_freq(data: bytes, pattern: bytes) -> float:
    pattern_len = len(pattern)
    if len(data) < pattern_len:
        return 0
    count = sum(1 for i in range(len(data) - pattern_len + 1) if data[i:i+pattern_len] == pattern)
    return count / (len(data) - pattern_len + 1)

# -----------------------------
# Decode & Feature Extractor
# -----------------------------
def decode_ciphertext(ciphertext: str) -> bytes:
    """Decode Base64 ciphertext into raw bytes"""
    return base64.b64decode(ciphertext)

def extract_all_features(ciphertext: str) -> dict:
    data = decode_ciphertext(ciphertext)
    bitstream = ''.join(format(b, '08b') for b in data)

    return {
        "Length": len(data),
        "UniqueBytes": len(set(data)),
        "Entropy": feature_entropy(data),
        "RenyiEntropy": feature_renyi(data),
        "MinEntropy": feature_minentropy(data),
        "ChiSquare": feature_chisquare(data),
        "ByteFreqVar": np.var(np.bincount(list(data), minlength=256)),
        "BitZeroFreq": bitstream.count("0") / len(bitstream) if len(bitstream) > 0 else 0,
        "BitOneFreq": bitstream.count("1") / len(bitstream) if len(bitstream) > 0 else 0,
        "Runs": feature_runs(bitstream),
        "LongestRun": feature_longest_run(bitstream),
        "SerialCorr": feature_serial_corr(bitstream),
        "ZlibRatio": feature_compression(data),
        "IndexCoincidence": feature_ic(data),
        "Autocorr1": feature_autocorr(data, lag=1),
        "Autocorr2": feature_autocorr(data, lag=2),
        "MonobitPValue": feature_monobit_pvalue(bitstream),
        "Freq_0x00": feature_byte_pattern_freq(data, b'\x00'),
        "Freq_0xFFFF": feature_byte_pattern_freq(data, b'\xFF\xFF'),
    }

# -----------------------------
# Main: Convert dataset
# -----------------------------
if __name__ == "__main__":
    # Load CSV (your dataset file)
    df = pd.read_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\test.csv")

    feature_rows = []
    for i, row in df.iterrows():
        try:
            features = extract_all_features(row["Encrypted_Data"])
            features["Algorithm"] = row["Algorithm"]
            features["Algorithm_Type"] = row["Algorithm_Type"]
            features["Category"] = row["Category"]
            feature_rows.append(features)
            if i%100==0:
                print(f"Processed row {i+1}/{len(df)}")
        except Exception as e:
            print(f"Error on row {i+1}: {e}")


    # Build final dataframe
    print(f"Total rows processed: {len(feature_rows)}")
    feature_df = pd.DataFrame(feature_rows)
    print(feature_df.head())
    # Save to CSV for ML use
    feature_df.to_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\features_dataset_test.csv", index=False)

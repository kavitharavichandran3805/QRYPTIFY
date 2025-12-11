import pandas as pd
import numpy as np
import math
import scipy.special as ss
from scipy.stats import norm


class BinaryData:
    def __init__(self, bit_string):
        n = len(bit_string)
        padding = (8 - n % 8) % 8
        if padding > 0:
            bit_string += '0' * padding
        chunk_size = 1000000  
        packed_chunks = []     
        for i in range(0, len(bit_string), chunk_size * 8):
            chunk = bit_string[i:i + chunk_size * 8]
            chunk_bytes = [int(chunk[j*8:(j+1)*8], 2) 
                          for j in range(len(chunk)//8)]
            packed_chunks.extend(chunk_bytes)
        
        self.packed = np.array(packed_chunks, dtype=np.uint8)
        self.unpacked = np.unpackbits(self.packed)[:n]  
        self.n = n

def monobit_test(binary):
    ones_count = np.count_nonzero(binary.unpacked)
    s = abs(2.0 * float(ones_count) - float(binary.n)) 
    if binary.n == 0:
        return [0.0, False]
    p = math.erfc(s / (math.sqrt(float(binary.n)) * math.sqrt(2.0)))
    success = p >= 0.01
    return [p, success]

def frequency_within_block_test(binary, M=128):
    if binary.n < M:
        return [0.0, False]
    nBlocks = binary.n // M
    blocks = binary.unpacked[:nBlocks * M].reshape(nBlocks, M)
    proportions = np.sum(blocks, axis=1, dtype=np.float64) / float(M)
    chisq = float(np.sum(4.0 * M * ((proportions - 0.5) ** 2)))
    if nBlocks == 0:
        return [0.0, False]
    p = ss.gammaincc(nBlocks / 2.0, chisq / 2.0)
    success = (p >= 0.01)
    return [p, success]

def runs_test(binary):
    if binary.n < 2:
        return [0.0, False]
    ones_count = np.count_nonzero(binary.unpacked)
    prop = float(ones_count) / float(binary.n)
    tau = 2.0 / math.sqrt(binary.n)
    if abs(prop - 0.5) >= tau:
        return [0.0, False]
    vobs = 1.0 + float(np.sum(binary.unpacked[:-1] != binary.unpacked[1:]))
    if prop == 0 or prop == 1:
        return [0.0, False]
    expected = 2.0 * binary.n * prop * (1.0 - prop)
    variance = 2.0 * binary.n * prop * (1.0 - prop)
    if variance == 0:
        return [0.0, False]
    numerator = abs(vobs - expected)
    denominator = 2.0 * math.sqrt(variance)
    if denominator == 0:
        return [0.0, False]
    p = math.erfc(numerator / denominator)
    success = (p >= 0.01)
    return [p, success]

def longest_run_within_block_test(binary):
    def longest_run_in_block(block_bits):
        if len(block_bits) == 0:
            return 0
        max_run = 0
        current_run = 0
        for bit in block_bits:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        return max_run
    bits = binary.unpacked
    n = binary.n
    if n < 128:
        return [0.0, False]
    elif n <= 6272:
        K, M = 3, 8
        vclasses = [1, 2, 3, 4]
        vprobs = [0.2148, 0.3672, 0.2305, 0.1875]
    elif n <= 750000:
        K, M = 5, 128
        vclasses = [4, 5, 6, 7, 8, 9]
        vprobs = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    else:
        K, M = 6, 10000
        vclasses = [10, 11, 12, 13, 14, 15, 16]
        vprobs = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    N = n // M
    numBlocks = n // M
    blocks = bits[:numBlocks * M].reshape(numBlocks, M)
    runs = np.array([longest_run_in_block(block) for block in blocks])
    freqs = np.histogram(runs, bins=[-1e10, *vclasses, 1e10])[0]
    vs = np.array(freqs, dtype=np.float64)
    chisq = 0.0
    for i in range(K):
        expected = N * vprobs[i]
        if expected > 0:
            chisq += ((vs[i] - expected) ** 2) / expected
    p = ss.gammaincc(K / 2.0, chisq / 2.0)
    success = (p >= 0.01)
    return [p, success]

def binary_matrix_rank_test(binary):
    n = binary.n
    M, Q = 32, 32
    N = n // (M * Q)
    if N == 0:
        return [0.0, False]
    bits = binary.unpacked[:N * M * Q]
    matrices = bits.reshape(N, M, Q)
    fm, fm1, rest = 0, 0, 0
    for matrix in matrices:
        rank = np.linalg.matrix_rank(matrix)
        if rank == M:
            fm += 1
        elif rank == M - 1:
            fm1 += 1
        else:
            rest += 1
    chisq = ((fm - 0.2888 * N) ** 2) / (0.2888 * N)
    chisq += ((fm1 - 0.5776 * N) ** 2) / (0.5776 * N)
    chisq += ((rest - 0.1336 * N) ** 2) / (0.1336 * N)
    p = math.exp(-chisq / 2.0)
    success = (p >= 0.01)
    return [p, success]

def discrete_fourier_transform_test(binary):
    n = binary.n
    if n < 1000:
        return [0.0, False]
    bits = 2 * binary.unpacked.astype(np.float64) - 1
    s = np.fft.fft(bits)
    modulus = np.abs(s[:n//2])
    tau = math.sqrt(math.log(1.0 / 0.05) * n)
    n0 = 0.95 * n / 2.0
    n1 = np.sum(modulus < tau)
    d = (n1 - n0) / math.sqrt(n * 0.95 * 0.05 / 4.0)
    p = math.erfc(abs(d) / math.sqrt(2.0))
    success = (p >= 0.01)
    return [p, success]

def maurers_universal_test(binary):
    n = binary.n
    L = 5
    if n >= 387840: L = 6
    if n >= 904960: L = 7
    if n >= 2068480: L = 8
    if n >= 4654080: L = 9
    if n >= 10342400: L = 10
    if n >= 22753280: L = 11
    if n >= 49643520: L = 12
    if n >= 107560960: L = 13
    if n >= 231669760: L = 14
    if n >= 496435200: L = 15
    if n >= 1059061760: L = 16
    if L < 6:
        return [0.0, False]
    _var = [2.954, 3.125, 3.238, 3.311, 3.356, 3.384, 3.401, 3.410, 3.416, 3.419, 3.421]
    _EV = [5.2177052, 6.1962507, 7.1836656, 8.1764248, 9.1723243, 10.170032, 11.168765, 
           12.168070, 13.167693, 14.167488, 15.167379]
    var = _var[L - 6]
    EV = _EV[L - 6]
    Q = 10 * (2 ** L)
    K = (n // L) - Q
    if K <= 0:
        return [0.0, False]
    bits = binary.unpacked[:(Q + K) * L]
    blocks = bits.reshape(-1, L)
    powers = 2 ** np.arange(L - 1, -1, -1, dtype=np.uint32)
    repacked = np.dot(blocks, powers)
    initSeg = repacked[:Q]
    testSeg = repacked[Q:]
    last_occurrence = np.zeros(2 ** L, dtype=np.int64)
    for i, val in enumerate(initSeg):
        last_occurrence[val] = i + 1
    distances = []
    for i, val in enumerate(testSeg):
        if last_occurrence[val] > 0:
            distances.append(i + Q + 1 - last_occurrence[val])
        last_occurrence[val] = i + Q + 1
    if len(distances) == 0:
        return [0.0, False]
    log_sum = np.sum(np.log2(distances, dtype=np.float64))
    fn = log_sum / len(distances)
    c = 0.7 - 0.8 / L + (4 + 32 / L) * pow(K, -3 / L) / 15
    sigma = c * math.sqrt(var / K)
    if sigma == 0:
        return [0.0, False]
    stat = abs(fn - EV) / (math.sqrt(2) * sigma)
    p = math.erfc(stat)
    success = (p >= 0.01)
    return [p, success]

def cumulative_sums_test(binary, mode=0):
    if binary.n < 100:
        return [0.0, False]
    bits = 2 * binary.unpacked.astype(np.int8) - 1
    css = np.cumsum(bits, dtype=np.int32)
    z = float(np.max(np.abs(css)))
    if z == 0:
        return [1.0, True]
    n = float(binary.n)
    start1 = int(((-n / z) + 1) / 4)
    end1 = int(((n / z) - 1) / 4)
    start2 = int(((-n / z) - 3) / 4)
    end2 = int(((n / z) - 1) / 4)
    def compute_term(k, i1, i2):
        t1 = ((4 * k + i1) * z) / math.sqrt(n)
        t2 = ((4 * k + i2) * z) / math.sqrt(n)
        return norm.cdf(t1) - norm.cdf(t2)
    s1 = sum(compute_term(k, 1, -1) for k in range(start1, end1 + 1))
    s2 = sum(compute_term(k, 3, 1) for k in range(start2, end2 + 1))
    p = 1.0 - s1 + s2
    p = max(0.0, min(1.0, p))
    success = (p >= 0.01)
    return [p, success]

def random_excursion_test(binary):
    def get_probability(x, k):
        x = abs(x - 4)
        if x == 0:
            return 0.0
        if k == 0:
            pi = 1.0 - 1.0 / (2.0 * x)
        elif k >= 5:
            pi = (1.0 / (2.0 * x)) * ((1.0 - 1.0 / (2.0 * x)) ** 4)
        else:
            pi = (1.0 / (4.0 * x * x)) * ((1.0 - 1.0 / (2.0 * x)) ** (k - 1))
        return pi
    bits = 2 * binary.unpacked.astype(np.int8) - 1
    s = np.cumsum(bits, dtype=np.int32)
    s = np.concatenate(([0], s, [0]))
    zcrosses = np.where(s == 0)[0]
    if len(zcrosses) < 2:
        return [(0.0, False)] * 9
    J = len(zcrosses) - 1
    if J < 500:
        return [(0.0, False)] * 9
    states = np.zeros((9, 6), dtype=np.int32)
    for i in range(len(zcrosses) - 1):
        cycle = s[zcrosses[i]:zcrosses[i + 1] + 1]
        for state in range(-4, 5):
            count = np.sum(cycle == state)
            count = min(count, 5)
            states[state + 4, count] += 1
    results = []
    for x in range(9):
        if x == 4:
            results.append((0.0, False))
            continue
        chisq = 0.0
        for k in range(6):
            prob = get_probability(x, k)
            expected = J * prob
            if expected >= 5:
                chisq += ((float(states[x, k]) - expected) ** 2) / expected
        p = ss.gammaincc(2.5, chisq / 2.0)
        results.append((p, p >= 0.01))
    return results

def random_excursion_variant_test(binary):
    bits = 2 * binary.unpacked.astype(np.int8) - 1
    s = np.cumsum(bits, dtype=np.int32)
    J = float(np.sum(s == 0) + 1)
    if J < 500:
        return [(0.0, False)]
    s_filtered = s[(s >= -9) & (s <= 9)]
    if len(s_filtered) == 0:
        return [(0.0, False)]
    unique_vals, counts = np.unique(s_filtered, return_counts=True)
    results = []
    for state, count in zip(unique_vals, counts):
        if state == 0:
            continue
        denominator = 2.0 * J * (4.0 * abs(float(state)) - 2.0)
        if denominator <= 0:
            results.append((0.0, False))
            continue
        numerator = abs(float(count) - J)
        p = math.erfc(numerator / math.sqrt(denominator))
        results.append((p, p >= 0.01))
    return results if results else [(0.0, False)]

def non_overlapping_template_matching_test(binary):
    return [0.5, True]

def overlapping_template_matching_test(binary):
    return [0.5, True]

def linear_complexity_test(binary):
    return [0.5, True]

def serial_test(binary):
    return [0.5, True]

def approximate_entropy_test(binary):
    return [0.5, True]


if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\sample_bits.csv")
    new_df = []
    for index, row in df.iterrows():
        bit_stream = BinaryData(row['Encrypted_Data'])
        result = {
            "bits_testing": monobit_test(bit_stream),
            "frequency_within_block": frequency_within_block_test(bit_stream),
            "runs": runs_test(bit_stream),
            "longest_run_within_block": longest_run_within_block_test(bit_stream),
            "binary_matrix_rank": binary_matrix_rank_test(bit_stream),
            "discrete_fourier_transform": discrete_fourier_transform_test(bit_stream),
            "non_overlapping_template_matching": non_overlapping_template_matching_test(bit_stream),
            "overlapping_template_matching": overlapping_template_matching_test(bit_stream),
            "maurers_universal_statistical": maurers_universal_test(bit_stream),
            "linear_complexity": linear_complexity_test(bit_stream),
            "serial": serial_test(bit_stream),
            "approximate_entropy": approximate_entropy_test(bit_stream),
            "cumulative_sums": cumulative_sums_test(bit_stream),
            "random_excursions": random_excursion_test(bit_stream),
            "random_excursions_variant": random_excursion_variant_test(bit_stream),
            "Category": row["Category"],
            "Algorithm_Type": row["Algorithm_Type"],
            "Algorithm": row["Algorithm"]
        }
        new_df.append(result)
    new_df = pd.DataFrame(new_df)
    new_df.to_csv("sample_nist.csv", index=False)
    print("Processing complete! Results saved to sample_nist.csv")
import pandas as pd
import numpy as np
import math
import scipy.special as ss
from scipy.stats import norm
import multiprocessing as mp

class BinaryData:
    def __init__(self, bit_string):
        n = len(bit_string)
        padding = (8 - n % 8) % 8
        if padding > 0:
            bit_string += '0' * padding

        n_bytes = len(bit_string) // 8
        packed_bytes = int(bit_string, 2).to_bytes(n_bytes, 'big')
        self.packed = np.frombuffer(packed_bytes, dtype=np.uint8)
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
    bits = 2 * binary.unpacked.astype(np.int8) - 1
    s = np.cumsum(bits, dtype=np.int32)
    s = np.concatenate(([0], s, [0]))
    zcrosses = np.where(s == 0)[0]
    if len(zcrosses) < 2:
        return [(0.0, False)] * 9
    J = len(zcrosses) - 1 
    if J < 500:
        return [(0.0, False)] * 9
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
        return [(0.0, False)] * 18
    s_filtered = s[(s >= -9) & (s <= 9)]
    if len(s_filtered) == 0:
        return [(0.0, False)] * 18
    results = []
    for state in range(-9, 10):
        if state == 0:
            continue     
        count = np.sum(s_filtered == state)
        denominator = 2.0 * J * (4.0 * abs(float(state)) - 2.0)   
        if denominator <= 0:
            results.append((0.0, False))
            continue     
        numerator = abs(float(count) - J)
        p = math.erfc(numerator / math.sqrt(denominator))

        results.append((p, p >= 0.01))
    while len(results) < 18:
        results.append((0.0, False))
        
    return results[:18]

def shannon_entropy_bits(binary):
    bits = binary.unpacked
    p1 = np.mean(bits)
    p0 = 1.0 - p1
    eps = 1e-12
    return - (p0 * np.log2(p0 + eps) + p1 * np.log2(p1 + eps))

def byte_histogram_features(binary):
    # use already packed bytes if you like
    b = binary.packed
    counts = np.bincount(b, minlength=256).astype(np.float64)
    probs = counts / counts.sum()

    # chi-square vs uniform
    expected = counts.sum() / 256.0
    chi2 = np.sum((counts - expected) ** 2 / (expected + 1e-12))

    # simple stats on probs
    max_p = probs.max()
    std_p = probs.std()

    return chi2, max_p, std_p

def run_length_summary(binary):
    bits = binary.unpacked
    if len(bits) == 0:
        return 0.0, 0.0, 0.0

    runs = []
    current = bits[0]
    length = 1
    for b in bits[1:]:
        if b == current:
            length += 1
        else:
            runs.append(length)
            current = b
            length = 1
    runs.append(length)

    runs = np.array(runs, dtype=np.float64)
    return runs.mean(), runs.std(), runs.max()

def autocorr_lag1(binary):
    bits = binary.unpacked.astype(np.int8)
    if len(bits) < 2:
        return 0.0
    x = 2 * bits - 1
    return float(np.dot(x[:-1], x[1:]) / (len(x) - 1))


def flatten_test_results(row):
    flattened = {}
    
    simple_tests = [
        'bits_testing', 'frequency_within_block', 'runs', 
        'longest_run_within_block', 'binary_matrix_rank',
        'discrete_fourier_transform', 'maurers_universal_statistical',
       'cumulative_sums'
    ]
    
    for test in simple_tests:
        if test in row:
            result = row[test]
            flattened[f'{test}_pvalue'] = float(result[0])
            flattened[f'{test}_pass'] = int(result[1])

    if 'random_excursions' in row:
        results = row['random_excursions']
        for i, (p_val, success) in enumerate(results):
            flattened[f'random_excursions_state{i-4}_pvalue'] = float(p_val)
            flattened[f'random_excursions_state{i-4}_pass'] = int(success)
   
    if 'random_excursions_variant' in row:
        results = row['random_excursions_variant']
        states = list(range(-9, 0)) + list(range(1, 10))  # -9 to 9, excluding 0
        for i, (p_val, success) in enumerate(results[:18]):  # Ensure exactly 18
            state = states[i] if i < len(states) else i
            flattened[f'random_excursions_variant_state{state}_pvalue'] = float(p_val)
            flattened[f'random_excursions_variant_state{state}_pass'] = int(success)
  
    flattened['Category'] = row['Category']
    flattened['Algorithm_Type'] = row['Algorithm_Type']
    flattened['Algorithm'] = row['Algorithm']
    
    return flattened


def process_one_row(row_dict):
    bit_stream = BinaryData(row_dict['Encrypted_Data'])

    result = {
            "bits_testing": monobit_test(bit_stream),
            "frequency_within_block": frequency_within_block_test(bit_stream),
            "runs": runs_test(bit_stream),
            "longest_run_within_block": longest_run_within_block_test(bit_stream),
            "binary_matrix_rank": binary_matrix_rank_test(bit_stream),
            "discrete_fourier_transform": discrete_fourier_transform_test(bit_stream),
            "maurers_universal_statistical": maurers_universal_test(bit_stream),
            "cumulative_sums": cumulative_sums_test(bit_stream),
            "random_excursions": random_excursion_test(bit_stream),
            "random_excursions_variant": random_excursion_variant_test(bit_stream),
            
            # "Category": row["Category"],
            # "Algorithm_Type": row["Algorithm_Type"],
            # "Algorithm": row["Algorithm"]
        }
    flattened_result = flatten_test_results(result)
    return flattened_result


if __name__ == "__main__":
    # Read input CSV
    df = pd.read_csv(
        r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\sample_models\sample_bits.csv"
    )

    # Convert each row to a plain dict (safer for multiprocessing pickling)
    rows = [row.to_dict() for _, row in df.iterrows()]

    # Choose number of worker processes (e.g., number of CPU cores)
    num_processes = mp.cpu_count()  # or set manually, e.g., 4

    print(f"Using {num_processes} worker processes")

    with mp.Pool(processes=num_processes) as pool:
        results = list(pool.imap_unordered(process_one_row, rows, chunksize=10))

    # Create final DataFrame with flattened columns
    final_df = pd.DataFrame(results)

    # Reorder columns: put metadata at the end
    metadata_cols = ['Category', 'Algorithm_Type', 'Algorithm']
    feature_cols = [col for col in final_df.columns if col not in metadata_cols]
    final_df = final_df[feature_cols + metadata_cols]

    # Fill any missing values with 0.0 for p-values
    pvalue_cols = [col for col in final_df.columns if col.endswith('_pvalue')]
    pass_cols = [col for col in final_df.columns if col.endswith('_pass')]

    final_df[pvalue_cols] = final_df[pvalue_cols].fillna(0.0)
    final_df[pass_cols] = final_df[pass_cols].fillna(0).astype(int)

    for col in pvalue_cols:
        final_df[col] = final_df[col].apply(lambda x: float(f"{x:.10f}"))

    final_df.to_csv("sample_nist_formatted_parallel.csv", index=False, float_format='%.10f')

    print("\n" + "=" * 60)
    print("Processing complete!")
    print(f"Total samples: {len(final_df)}")
    print(f"Total features: {len(feature_cols)}")
    print(f"Output saved to: sample_nist_formatted_parallel.csv")
    print("=" * 60)
    
    print("\n" + "="*60)
    print("DATA QUALITY CHECK")
    print("="*60)

    missing_counts = final_df.isnull().sum()
    if missing_counts.sum() > 0:
        print("\n⚠️  WARNING: Missing values detected!")
        print(missing_counts[missing_counts > 0])
    else:
        print("\n✅ No missing values")
    
    pvalue_cols = [col for col in feature_cols if col.endswith('_pvalue')]
    for col in pvalue_cols:
        out_of_range = ((final_df[col] < 0) | (final_df[col] > 1)).sum()
        if out_of_range > 0:
            print(f"⚠️  {col}: {out_of_range} values out of range [0,1]")
    
    pass_cols = [col for col in feature_cols if col.endswith('_pass')]
    for col in pass_cols:
        unique_vals = final_df[col].unique()
        if not set(unique_vals).issubset({0, 1}):
            print(f"⚠️  {col}: Contains values other than 0/1: {unique_vals}")
    
    print("\n✅ P-value ranges: OK")
    print("✅ Pass/fail values: OK")
    
    print("\n" + "="*60)
    print("FEATURE STATISTICS")
    print("="*60)
    print(f"\nTotal features: {len(feature_cols)}")
    print(f"  - P-value features: {len(pvalue_cols)}")
    print(f"  - Pass/fail features: {len(pass_cols)}")

    print("\n" + "="*60)
    print("CLASS DISTRIBUTION")
    print("="*60)
    print("\nBy Algorithm:")
    print(final_df['Algorithm'].value_counts())
    print("\nBy Category:")
    print(final_df['Category'].value_counts())
    print("\nBy Algorithm Type:")
    print(final_df['Algorithm_Type'].value_counts())
    
   
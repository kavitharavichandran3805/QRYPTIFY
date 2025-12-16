import pandas as pd
import numpy as np
import math
import scipy.special as ss
from scipy.stats import norm, entropy
import multiprocessing as mp
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# UTILITY CLASS (Optimized)
# ============================================================================

class BinaryData:
    """Optimized binary data handler with caching"""
    def __init__(self, bit_string):
        n = len(bit_string)
        padding = (8 - n % 8) % 8
        if padding > 0:
            bit_string += '0' * padding

        # pack bits to bytes efficiently
        n_bytes = len(bit_string) // 8
        packed_bytes = int(bit_string, 2).to_bytes(n_bytes, 'big')
        self.packed = np.frombuffer(packed_bytes, dtype=np.uint8)
        self.unpacked = np.unpackbits(self.packed)[:n]
        self.n = n

        # Cache commonly used values
        self._ones_count = None
        self._byte_counts = None

    @property
    def ones_count(self):
        if self._ones_count is None:
            self._ones_count = np.count_nonzero(self.unpacked)
        return self._ones_count

    @property
    def byte_counts(self):
        if self._byte_counts is None:
            self._byte_counts = np.bincount(self.packed, minlength=256)
        return self._byte_counts

# ============================================================================
# NIST STATISTICAL TESTS (Optimized)
# ============================================================================

def monobit_test(binary):
    """Optimized monobit test using cached ones_count"""
    if binary.n == 0:
        return [0.0, False]
    s = abs(2.0 * float(binary.ones_count) - float(binary.n))
    p = math.erfc(s / (math.sqrt(float(binary.n)) * math.sqrt(2.0)))
    return [p, p >= 0.01]

def frequency_within_block_test(binary, M=128):
    if binary.n < M:
        return [0.0, False]
    nBlocks = binary.n // M
    blocks = binary.unpacked[:nBlocks * M].reshape(nBlocks, M)
    proportions = np.sum(blocks, axis=1, dtype=np.float64) / float(M)
    chisq = float(np.sum(4.0 * M * ((proportions - 0.5) ** 2)))
    p = ss.gammaincc(nBlocks / 2.0, chisq / 2.0)
    return [p, p >= 0.01]

def runs_test(binary):
    if binary.n < 2:
        return [0.0, False]
    prop = float(binary.ones_count) / float(binary.n)
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
    return [p, p >= 0.01]

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
    return [p, p >= 0.01]

def binary_matrix_rank_test(binary):
    n = binary.n
    M, Q = 32, 32
    N = n // (M * Q)
    if N == 0:
        return [0.0, False]
    bits = binary.unpacked[:N * M * Q]
    matrices = bits.reshape(N, M, Q)

    ranks = np.array([np.linalg.matrix_rank(matrix) for matrix in matrices])
    fm = np.sum(ranks == M)
    fm1 = np.sum(ranks == M - 1)
    rest = N - fm - fm1

    chisq = ((fm - 0.2888 * N) ** 2) / (0.2888 * N)
    chisq += ((fm1 - 0.5776 * N) ** 2) / (0.5776 * N)
    chisq += ((rest - 0.1336 * N) ** 2) / (0.1336 * N)
    p = math.exp(-chisq / 2.0)
    return [p, p >= 0.01]

def discrete_fourier_transform_test(binary):
    n = binary.n
    if n < 1000:
        return [0.0, False]
    bits = 2 * binary.unpacked.astype(np.float64) - 1
    s = np.fft.fft(bits)
    modulus = np.abs(s[:n // 2])
    tau = math.sqrt(math.log(1.0 / 0.05) * n)
    n0 = 0.95 * n / 2.0
    n1 = np.sum(modulus < tau)
    d = (n1 - n0) / math.sqrt(n * 0.95 * 0.05 / 4.0)
    p = math.erfc(abs(d) / math.sqrt(2.0))
    return [p, p >= 0.01]

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
    return [p, p >= 0.01]

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
    return [p, p >= 0.01]

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
    """Shannon entropy of bit distribution"""
    if binary.n == 0:
        return 0.0
    p1 = binary.ones_count / binary.n
    p0 = 1.0 - p1
    eps = 1e-12
    H = 0.0
    if p0 > eps:
        H -= p0 * np.log2(p0)
    if p1 > eps:
        H -= p1 * np.log2(p1)
    return H

def byte_entropy(binary):
    """Shannon entropy of byte distribution"""
    if len(binary.packed) == 0:
        return 0.0
    counts = binary.byte_counts[binary.byte_counts > 0]
    probs = counts / counts.sum()
    return entropy(probs, base=2)

def byte_histogram_features(binary):
    """Statistical features from byte distribution"""
    if len(binary.packed) == 0:
        return 0.0, 0.0, 0.0, 0.0

    counts = binary.byte_counts.astype(np.float64)
    probs = counts / counts.sum()

    expected = counts.sum() / 256.0
    chi2 = np.sum((counts - expected) ** 2 / (expected + 1e-12))

    max_p = probs.max()
    std_p = probs.std()
    mean_p = probs.mean()
    cv = std_p / (mean_p + 1e-12)

    return chi2, max_p, std_p, cv

def run_length_features(binary):
    """Enhanced run length statistics"""
    bits = binary.unpacked
    if len(bits) == 0:
        return 0.0, 0.0, 0.0, 0.0

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

    run_mean = runs.mean()
    run_std = runs.std()
    run_max = runs.max()
    run_cv = run_std / (run_mean + 1e-12)

    return run_mean, run_std, run_max, run_cv

def autocorrelation_features(binary):
    """Multiple autocorrelation lags"""
    bits = binary.unpacked.astype(np.int8)
    if len(bits) < 10:
        return 0.0, 0.0, 0.0, 0.0

    x = 2 * bits - 1
    lags = [1, 2, 4, 8]
    acf_values = []

    for lag in lags:
        if len(x) <= lag:
            acf_values.append(0.0)
        else:
            acf = np.dot(x[:-lag], x[lag:]) / (len(x) - lag)
            acf_values.append(float(acf))

    return tuple(acf_values)

def complexity_features(binary):
    """Approximate complexity features"""
    bits = binary.unpacked
    if len(bits) == 0:
        return 0.0, 0.0

    n = len(bits)
    complexity = 0
    i = 0
    prefix_dict = set()

    while i < n:
        for j in range(i + 1, min(i + 100, n + 1)):
            substring = tuple(bits[i:j])
            if substring not in prefix_dict:
                prefix_dict.add(substring)
                complexity += 1
                i = j
                break
        else:
            i += 1

    lz_complexity = complexity / (n / np.log2(n + 1) + 1e-12)

    if n >= 8:
        patterns = set()
        for i in range(n - 7):
            pattern = tuple(bits[i:i+8])
            patterns.add(pattern)
        compression_ratio = len(patterns) / (n - 7)
    else:
        compression_ratio = 1.0

    return lz_complexity, compression_ratio

def bit_transition_features(binary):
    """Bit transition patterns"""
    bits = binary.unpacked
    if len(bits) < 2:
        return 0.0, 0.0, 0.0

    transitions = np.diff(bits.astype(np.int8))
    zero_to_one = np.sum(transitions == 1)
    one_to_zero = np.sum(transitions == -1)

    total_trans = zero_to_one + one_to_zero
    transition_rate = total_trans / (len(bits) - 1)
    transition_balance = abs(zero_to_one - one_to_zero) / (total_trans + 1e-12)

    p = binary.ones_count / binary.n
    expected_transitions = 2 * p * (1 - p) * (binary.n - 1)
    transition_deviation = abs(total_trans - expected_transitions) / (expected_transitions + 1e-12)

    return transition_rate, transition_balance, transition_deviation

def spectral_features(binary):
    """Frequency domain features"""
    bits = binary.unpacked
    if len(bits) < 100:
        return 0.0, 0.0, 0.0

    x = 2 * bits.astype(np.float64) - 1
    fft_vals = np.fft.fft(x)
    power_spectrum = np.abs(fft_vals[:len(fft_vals)//2])**2

    ps_norm = power_spectrum / (power_spectrum.sum() + 1e-12)
    spectral_entropy = entropy(ps_norm + 1e-12, base=2)

    max_power = power_spectrum.max()
    mean_power = power_spectrum.mean()
    dominant_freq_ratio = max_power / (mean_power + 1e-12)

    geometric_mean = np.exp(np.mean(np.log(power_spectrum + 1e-12)))
    arithmetic_mean = np.mean(power_spectrum)
    spectral_flatness = geometric_mean / (arithmetic_mean + 1e-12)

    return spectral_entropy, dominant_freq_ratio, spectral_flatness

def local_randomness_features(binary):
    """Block-wise randomness assessment"""
    bits = binary.unpacked
    n = len(bits)

    if n < 1000:
        return 0.0, 0.0

    block_size = min(500, n // 10)
    n_blocks = n // block_size

    block_entropies = []
    block_ones_ratios = []

    for i in range(n_blocks):
        block = bits[i*block_size:(i+1)*block_size]
        ones = np.sum(block)
        p1 = ones / len(block)
        p0 = 1 - p1
        if 0 < p0 < 1:
            H = -(p0 * np.log2(p0) + p1 * np.log2(p1))
        else:
            H = 0.0
        block_entropies.append(H)
        block_ones_ratios.append(p1)

    entropy_variance = np.var(block_entropies)
    ones_ratio_variance = np.var(block_ones_ratios)

    return entropy_variance, ones_ratio_variance

# ============================================================================
# FLATTENING FUNCTION
# ============================================================================

def flatten_test_results(row):
    """Flatten all test results into separate columns"""
    flattened = {}

    # 1. NIST tests (simple)
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

    # 2. Random excursion tests
    if 'random_excursions' in row:
        results = row['random_excursions']
        for i, (p_val, success) in enumerate(results):
            flattened[f'random_excursions_state{i-4}_pvalue'] = float(p_val)
            flattened[f'random_excursions_state{i-4}_pass'] = int(success)

    if 'random_excursions_variant' in row:
        results = row['random_excursions_variant']
        states = list(range(-9, 0)) + list(range(1, 10))
        for i, (p_val, success) in enumerate(results[:18]):
            state = states[i]
            flattened[f'random_excursions_variant_state{state}_pvalue'] = float(p_val)
            flattened[f'random_excursions_variant_state{state}_pass'] = int(success)

    # 3. Enhanced features (scalar)
    feature_mapping = {
        'entropy_bits': 'entropy_bits',
        'entropy_bytes': 'entropy_bytes',
        'chi2_bytes': 'chi2_bytes',
        'max_p_byte': 'max_p_byte',
        'std_p_byte': 'std_p_byte',
        'cv_byte': 'cv_byte',
        'run_mean': 'run_mean',
        'run_std': 'run_std',
        'run_max': 'run_max',
        'run_cv': 'run_cv',
        'acf_lag1': 'acf_lag1',
        'acf_lag2': 'acf_lag2',
        'acf_lag4': 'acf_lag4',
        'acf_lag8': 'acf_lag8',
        'lz_complexity': 'lz_complexity',
        'compression_ratio': 'compression_ratio',
        'transition_rate': 'transition_rate',
        'transition_balance': 'transition_balance',
        'transition_deviation': 'transition_deviation',
        'spectral_entropy': 'spectral_entropy',
        'dominant_freq_ratio': 'dominant_freq_ratio',
        'spectral_flatness': 'spectral_flatness',
        'entropy_variance': 'entropy_variance',
        'ones_ratio_variance': 'ones_ratio_variance'
    }

    for key, col_name in feature_mapping.items():
        if key in row:
            flattened[col_name] = float(row[key])

    # 4. Metadata
    flattened['Category'] = row['Category']
    flattened['Algorithm_Type'] = row['Algorithm_Type']
    flattened['Algorithm'] = row['Algorithm']

    return flattened

# ============================================================================
# PROCESSING FUNCTION
# ============================================================================

def process_one_row(row_dict):
    """Process a single row with all tests and features"""
    try:
        bit_stream = BinaryData(row_dict['Encrypted_Data'])

        # NIST Tests
        nist_results = {
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
        }

        # Enhanced Features
        H_bits = shannon_entropy_bits(bit_stream)
        H_bytes = byte_entropy(bit_stream)
        chi2_bytes, max_p_byte, std_p_byte, cv_byte = byte_histogram_features(bit_stream)
        run_mean, run_std, run_max, run_cv = run_length_features(bit_stream)
        acf1, acf2, acf4, acf8 = autocorrelation_features(bit_stream)
        lz_complexity, compression_ratio = complexity_features(bit_stream)
        trans_rate, trans_balance, trans_dev = bit_transition_features(bit_stream)
        spec_entropy, dom_freq_ratio, spec_flatness = spectral_features(bit_stream)
        ent_var, ones_var = local_randomness_features(bit_stream)

        result = {
            **nist_results,
            "entropy_bits": H_bits,
            "entropy_bytes": H_bytes,
            "chi2_bytes": chi2_bytes,
            "max_p_byte": max_p_byte,
            "std_p_byte": std_p_byte,
            "cv_byte": cv_byte,
            "run_mean": run_mean,
            "run_std": run_std,
            "run_max": run_max,
            "run_cv": run_cv,
            "acf_lag1": acf1,
            "acf_lag2": acf2,
            "acf_lag4": acf4,
            "acf_lag8": acf8,
            "lz_complexity": lz_complexity,
            "compression_ratio": compression_ratio,
            "transition_rate": trans_rate,
            "transition_balance": trans_balance,
            "transition_deviation": trans_dev,
            "spectral_entropy": spec_entropy,
            "dominant_freq_ratio": dom_freq_ratio,
            "spectral_flatness": spec_flatness,
            "entropy_variance": ent_var,
            "ones_ratio_variance": ones_var,
            "Category": row_dict["Category"],
            "Algorithm_Type": row_dict["Algorithm_Type"],
            "Algorithm": row_dict["Algorithm"]
        }

        return flatten_test_results(result)

    except Exception as e:
        # Return minimal info to keep shapes consistent
        return {
            "error": str(e),
            "Category": row_dict.get("Category", "Unknown"),
            "Algorithm_Type": row_dict.get("Algorithm_Type", "Unknown"),
            "Algorithm": row_dict.get("Algorithm", "Unknown")
        }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import time

    INPUT_FILE = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\sample_models\sample_bits.csv"
    OUTPUT_FILE = "nistest1.csv"

    print("=" * 80)
    print("ENHANCED NIST TEST PROCESSOR WITH PARALLEL PROCESSING")
    print("=" * 80)

    start_time = time.time()

    # Read input CSV
    print(f"\n📂 Reading input file: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    total_rows = len(df)
    print(f"✅ Loaded {total_rows} samples")

    rows = [row.to_dict() for _, row in df.iterrows()]

    num_processes = max(1, mp.cpu_count() - 1)
    print(f"\n🚀 Using {num_processes} parallel workers")

    # Process in parallel with simple progress
    print("\n⚙️  Processing samples...")
    results = []
    processed = 0
    log_every = max(1, total_rows // 20)  # log about 20 times

    with mp.Pool(processes=num_processes) as pool:
        for res in pool.imap(process_one_row, rows, chunksize=5):
            results.append(res)
            processed += 1
            if processed % log_every == 0 or processed == total_rows:
                print(f"   ➤ Processed {processed} / {total_rows} rows")

    processing_time = time.time() - start_time

    print("\n📊 Creating final DataFrame...")
    final_df = pd.DataFrame(results)

    # Remove error rows if any
    if 'error' in final_df.columns:
        error_count = final_df['error'].notna().sum()
        if error_count > 0:
            print(f"⚠️  {error_count} rows had errors and were removed")
            final_df = final_df[final_df['error'].isna()].drop('error', axis=1)

    metadata_cols = ['Category', 'Algorithm_Type', 'Algorithm']
    feature_cols = [col for col in final_df.columns if col not in metadata_cols]
    final_df = final_df[feature_cols + metadata_cols]

    pvalue_cols = [col for col in final_df.columns if col.endswith('_pvalue')]
    pass_cols = [col for col in final_df.columns if col.endswith('_pass')]
    enhanced_feature_cols = [
        col for col in feature_cols
        if not (col.endswith('_pvalue') or col.endswith('_pass'))
    ]

    print("\n🔧 Cleaning data...")
    if pvalue_cols:
        final_df[pvalue_cols] = final_df[pvalue_cols].fillna(0.0)
    if pass_cols:
        final_df[pass_cols] = final_df[pass_cols].fillna(0).astype(int)
    if enhanced_feature_cols:
        final_df[enhanced_feature_cols] = final_df[enhanced_feature_cols].fillna(0.0)

    print(f"\n💾 Saving to: {OUTPUT_FILE}")
    final_df.to_csv(OUTPUT_FILE, index=False, float_format='%.10f')

    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"⏱️  Total time: {processing_time:.2f} seconds")
    print(f"⚡ Speed: {len(final_df) / processing_time:.2f} samples/second")
    print(f"📦 Total samples: {len(final_df)}")

    # recompute feature_cols after dropping errors
    feature_cols = [col for col in final_df.columns if col not in metadata_cols]
    pvalue_cols = [col for col in final_df.columns if col.endswith('_pvalue')]
    pass_cols = [col for col in final_df.columns if col.endswith('_pass')]
    enhanced_feature_cols = [
        col for col in feature_cols
        if not (col.endswith('_pvalue') or col.endswith('_pass'))
    ]

    print(f"📊 Total features: {len(feature_cols)}")
    print(f"   - NIST p-values: {len(pvalue_cols)}")
    print(f"   - NIST pass/fail: {len(pass_cols)}")
    print(f"   - Enhanced features: {len(enhanced_feature_cols)}")

    print("\n" + "=" * 80)
    print("DATA QUALITY CHECK")
    print("=" * 80)

    missing_counts = final_df.isnull().sum()
    if missing_counts.sum() > 0:
        print("\n⚠️  WARNING: Missing values detected!")
        print(missing_counts[missing_counts > 0])
    else:
        print("\n✅ No missing values")

    out_of_range_count = 0
    for col in pvalue_cols:
        out_of_range = ((final_df[col] < 0) | (final_df[col] > 1)).sum()
        if out_of_range > 0:
            print(f"⚠️  {col}: {out_of_range} values out of range [0,1]")
            out_of_range_count += out_of_range
    if out_of_range_count == 0:
        print("✅ All p-values in valid range [0,1]")

    invalid_pass_count = 0
    for col in pass_cols:
        unique_vals = final_df[col].unique()
        if not set(unique_vals).issubset({0, 1}):
            print(f"⚠️  {col}: Contains values other than 0/1: {unique_vals}")
            invalid_pass_count += 1
    if invalid_pass_count == 0:
        print("✅ All pass/fail values valid (0 or 1)")

    print("\n" + "=" * 80)
    print("CLASS DISTRIBUTION")
    print("=" * 80)
    print("\n📌 By Algorithm:")
    print(final_df['Algorithm'].value_counts())
    print("\n📌 By Category:")
    print(final_df['Category'].value_counts())
    print("\n📌 By Algorithm Type:")
    print(final_df['Algorithm_Type'].value_counts())

    print("\n" + "=" * 80)
    print("ENHANCED FEATURE SUMMARY")
    print("=" * 80)

    stats_features = [f for f in enhanced_feature_cols if any(x in f for x in ['entropy', 'chi2', 'byte'])]
    print("\n🔬 Statistical Features:")
    print(f"   {len(stats_features)} features: {', '.join(stats_features[:5])}...")

    run_features = [f for f in enhanced_feature_cols if 'run' in f]
    print("\n🏃 Run Length Features:")
    print(f"   {len(run_features)} features: {', '.join(run_features)}")

    temporal_features = [f for f in enhanced_feature_cols if any(x in f for x in ['acf', 'transition'])]
    print("\n📈 Temporal Features:")
    print(f"   {len(temporal_features)} features: {', '.join(temporal_features)}")

    spectral_feat = [f for f in enhanced_feature_cols if 'spectral' in f or 'freq' in f]
    print("\n🌊 Spectral Features:")
    print(f"   {len(spectral_feat)} features: {', '.join(spectral_feat)}")

    complexity_feat = [f for f in enhanced_feature_cols if any(x in f for x in ['complexity', 'compression'])]
    print("\n🧮 Complexity Features:")
    print(f"   {len(complexity_feat)} features: {', '.join(complexity_feat)}")

    print("\n" + "=" * 80)
    print("✨ READY FOR MODEL TRAINING!")
    print("=" * 80)

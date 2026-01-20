import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")


def bits_string_to_bytes(bits_str):
    bits_str = str(bits_str).strip().replace('\n', '').replace(' ', '')
    if not all(c in '01' for c in bits_str):
        return np.zeros(128, dtype=np.uint8)
    remainder = len(bits_str) % 8
    if remainder != 0:
        bits_str += '0' * (8 - remainder)
    num_bytes = len(bits_str) // 8
    bytes_array = np.zeros(num_bytes, dtype=np.uint8)
    for i in range(num_bytes):
        byte_bits = bits_str[i*8:(i+1)*8]
        bytes_array[i] = int(byte_bits, 2)  
    return bytes_array


def calculate_entropy(data):
    if len(data) == 0:
        return 0
    
    if isinstance(data, bytes):
        data = np.frombuffer(data, dtype=np.uint8)
    
    byte_counts = np.bincount(data, minlength=256)
    probabilities = byte_counts / len(data)
    entropy = -np.sum([p * np.log2(p) for p in probabilities if p > 0])
    return entropy


def extract_block_cipher_features(ciphertext, block_size=16):
    features = {}
    if isinstance(ciphertext, bytes):
        ciphertext = np.frombuffer(ciphertext, dtype=np.uint8)
    blocks = [tuple(ciphertext[i:i+block_size]) 
              for i in range(0, len(ciphertext), block_size)
              if len(ciphertext[i:i+block_size]) == block_size]
    if len(blocks) > 0:
        unique_blocks = len(set(blocks))
        total_blocks = len(blocks)
        features['block_uniqueness_ratio'] = unique_blocks / total_blocks
    else:
        features['block_uniqueness_ratio'] = 0
    if len(ciphertext) >= block_size and len(ciphertext) % block_size == 0:
        last_byte = ciphertext[-1]
        
        if 0 < last_byte <= block_size:
            padding_bytes = ciphertext[-last_byte:]
            features['potential_padding_value'] = last_byte
            features['padding_consistency'] = (
                np.sum(padding_bytes == last_byte) / last_byte
            )
        else:
            features['potential_padding_value'] = 0
            features['padding_consistency'] = 0
    else:
        features['potential_padding_value'] = 0
        features['padding_consistency'] = 0
    if len(blocks) > 1:
        correlations = []
        for i in range(len(blocks) - 1):
            block1 = np.array(blocks[i])
            block2 = np.array(blocks[i+1])
            xor_result = np.bitwise_xor(block1, block2)
            correlation_score = np.sum(xor_result) / (block_size * 255)
            correlations.append(correlation_score)
        
        features['mean_block_correlation'] = np.mean(correlations)
        features['std_block_correlation'] = np.std(correlations)
    else:
        features['mean_block_correlation'] = 0
        features['std_block_correlation'] = 0
    features['length_mod_blocksize'] = len(ciphertext) % block_size
    if len(ciphertext) >= block_size:
        last_block = ciphertext[-block_size:]
        features['last_block_entropy'] = calculate_entropy(last_block)
    else:
        features['last_block_entropy'] = 0
    if len(ciphertext) >= block_size:
        first_block = ciphertext[:block_size]
        features['first_block_entropy'] = calculate_entropy(first_block)
    else:
        features['first_block_entropy'] = 0
    return features


def extract_stream_cipher_features(ciphertext):
    features = {}
    if isinstance(ciphertext, bytes):
        ciphertext = np.frombuffer(ciphertext, dtype=np.uint8)
    if len(ciphertext) >= 256:
        prefix = ciphertext[:256]
        features['prefix_bias_score'] = abs(np.mean(prefix) - 127.5)
        features['prefix_std'] = np.std(prefix)
        features['first_byte_is_zero'] = 1 if prefix[0] == 0 else 0
        features['byte_255_value'] = int(prefix[255]) if len(prefix) > 255 else 0
    else:
        features['prefix_bias_score'] = 0
        features['prefix_std'] = 0
        features['first_byte_is_zero'] = 0
        features['byte_255_value'] = 0
    chunk_size = 64
    chunks_64 = [ciphertext[i:i+chunk_size] 
                 for i in range(0, len(ciphertext), chunk_size)
                 if len(ciphertext[i:i+chunk_size]) == chunk_size]
    
    if len(chunks_64) > 1:
        chunk_entropies = [calculate_entropy(chunk) for chunk in chunks_64]
        features['chunk64_entropy_mean'] = np.mean(chunk_entropies)
        features['chunk64_entropy_std'] = np.std(chunk_entropies)
    else:
        features['chunk64_entropy_mean'] = 0
        features['chunk64_entropy_std'] = 0
    if len(ciphertext) > 0:
        byte_counts = np.bincount(ciphertext, minlength=256)
        byte_freq = byte_counts / len(ciphertext)
        
        features['max_byte_freq'] = np.max(byte_freq)
        features['min_byte_freq'] = np.min(byte_freq[byte_freq > 0]) if np.any(byte_freq > 0) else 0
        features['byte_freq_range'] = features['max_byte_freq'] - features['min_byte_freq']
        
        expected_freq = 1 / 256
        tolerance = 0.001
        features['unusual_byte_count'] = int(np.sum(np.abs(byte_freq - expected_freq) > tolerance))
    else:
        features['max_byte_freq'] = 0
        features['min_byte_freq'] = 0
        features['byte_freq_range'] = 0
        features['unusual_byte_count'] = 0
    if len(ciphertext) > 0:
        high_bit_count = np.sum(ciphertext >= 128)
        features['high_bit_ratio'] = high_bit_count / len(ciphertext)
        
        low_bit_count = np.sum(ciphertext % 2 == 1)
        features['low_bit_ratio'] = low_bit_count / len(ciphertext)
    else:
        features['high_bit_ratio'] = 0
        features['low_bit_ratio'] = 0
    if len(ciphertext) > 1:
        runs = 0
        current_run = 1
        for i in range(1, len(ciphertext)):
            if ciphertext[i] > ciphertext[i-1]:
                current_run += 1
            else:
                if current_run >= 3:
                    runs += 1
                current_run = 1
        features['long_run_count'] = runs
    else:
        features['long_run_count'] = 0
    
    return features


def extract_hybrid_features(ciphertext):
    features = {}
    if isinstance(ciphertext, bytes):
        ciphertext = np.frombuffer(ciphertext, dtype=np.uint8)
    features['ciphertext_length'] = len(ciphertext)
    if len(ciphertext) < 500:
        features['length_category'] = 0
    elif 500 <= len(ciphertext) < 1000:
        features['length_category'] = 1
    elif 1000 <= len(ciphertext) < 5000:
        features['length_category'] = 2
    else:
        features['length_category'] = 3
    
    features['length_bucket'] = len(ciphertext) // 100
    split_points = [256, 512, 768, 1024, 2048]
    
    for split in split_points:
        if len(ciphertext) > split:
            first_part = ciphertext[:split]
            second_part = ciphertext[split:]
            
            first_entropy = calculate_entropy(first_part)
            second_entropy = calculate_entropy(second_part)
            
            features[f'entropy_split_{split}_first'] = first_entropy
            features[f'entropy_split_{split}_second'] = second_entropy
            features[f'entropy_split_{split}_ratio'] = (
                first_entropy / (second_entropy + 1e-6)
            )
        else:
            features[f'entropy_split_{split}_first'] = 0
            features[f'entropy_split_{split}_second'] = 0
            features[f'entropy_split_{split}_ratio'] = 0
    if len(ciphertext) > 1024:
        split = min(1024, len(ciphertext) // 2)
        first_part = ciphertext[:split]
        second_part = ciphertext[split:]
        
        first_freq = np.bincount(first_part, minlength=256) / len(first_part)
        second_freq = np.bincount(second_part, minlength=256) / len(second_part)
        
        kl_divergence = np.sum(
            first_freq * np.log((first_freq + 1e-10) / (second_freq + 1e-10))
        )
        features['kl_divergence_first_second'] = kl_divergence
        
        chi_square = np.sum(
            (first_freq - second_freq) ** 2 / (second_freq + 1e-10)
        )
        features['chi_square_first_second'] = chi_square
    else:
        features['kl_divergence_first_second'] = 0
        features['chi_square_first_second'] = 0
    if len(ciphertext) >= 16:
        first_16 = ciphertext[:16]
        features['first_16_zero_count'] = int(np.sum(first_16 == 0))
        features['has_asn1_marker'] = 1 if first_16[0] == 0x30 else 0
        features['first_16_entropy'] = calculate_entropy(first_16)
    else:
        features['first_16_zero_count'] = 0
        features['has_asn1_marker'] = 0
        features['first_16_entropy'] = 0
    if len(ciphertext) >= 256:
        first_chunk = int.from_bytes(ciphertext[:256].tobytes(), 'big')
        
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        features['divisible_by_small_primes'] = sum(
            1 for p in small_primes if first_chunk % p == 0
        )
        
        bit_count = bin(first_chunk).count('1')
        features['first_chunk_bit_density'] = bit_count / 2048
    else:
        features['divisible_by_small_primes'] = 0
        features['first_chunk_bit_density'] = 0
    features['length_mod_16'] = len(ciphertext) % 16
    features['length_mod_32'] = len(ciphertext) % 32
    features['length_mod_64'] = len(ciphertext) % 64
    return features


def extract_all_features(ciphertext_bytes):
    try:
        features = {}
        features.update(extract_block_cipher_features(ciphertext_bytes))
        features.update(extract_stream_cipher_features(ciphertext_bytes))
        features.update(extract_hybrid_features(ciphertext_bytes))
        return features
    
    except Exception as e:
        print(f"Error extracting features: {e}")
        return get_empty_features()


def get_empty_features():
    dummy_ciphertext = np.zeros(2048, dtype=np.uint8)
    features = extract_all_features(dummy_ciphertext)
    return {k: 0 for k in features.keys()}

def process_csv_with_bits(csv_path, bits_column='Encrypted_Data'):
    print(f"\n[Processing] {os.path.basename(csv_path)}")
    df = pd.read_csv(csv_path)
    
    if bits_column not in df.columns:
        raise ValueError(f"Column '{bits_column}' not found in CSV!")
    
    print(f"✓ Found {len(df)} rows with '{bits_column}' column")

    print(f"Extracting enhanced features...")
    enhanced_features = []
    
    for idx, bits_str in tqdm(enumerate(df[bits_column]), total=len(df), desc="Processing"):
        ciphertext_bytes = bits_string_to_bytes(bits_str)
        features = extract_all_features(ciphertext_bytes)
        enhanced_features.append(features)
    df_features = pd.DataFrame(enhanced_features)
    
    print(f"✓ Extracted {len(df_features.columns)} features")
    
    return df_features



if __name__ == "__main__":
    print("=" * 80)
    print("ENHANCED FEATURE EXTRACTION + NIST MERGE (SINGLE ALGORITHM)")
    print("=" * 80)
    NIST_CSV_PATH = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\sample_models\sample_nist_formatted.csv"
    BITS_CSV_PATH = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\sample_models\sample_bits.csv"
    BITS_COLUMN = "Encrypted_Data"
    OUTPUT_MERGED_PATH = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\datasets\sample_models\sample_nist_new.csv"
    if not os.path.exists(NIST_CSV_PATH):
        raise FileNotFoundError(f"NIST file not found: {NIST_CSV_PATH}")

    df_nist = pd.read_csv(NIST_CSV_PATH)
    print(f"✓ NIST features loaded: {df_nist.shape}")
    if not os.path.exists(BITS_CSV_PATH):
        raise FileNotFoundError(f"Bits file not found: {BITS_CSV_PATH}")

    df_enhanced = process_csv_with_bits(BITS_CSV_PATH, BITS_COLUMN)
    print(f"✓ Enhanced features extracted: {df_enhanced.shape}")

    if len(df_nist) != len(df_enhanced):
        raise ValueError(
            f"Row mismatch:\n"
            f"  NIST rows     = {len(df_nist)}\n"
            f"  Enhanced rows = {len(df_enhanced)}"
        )

    df_merged = pd.concat(
        [df_nist.reset_index(drop=True),
         df_enhanced.reset_index(drop=True)],
        axis=1
    )

    print(f"✓ Final merged shape: {df_merged.shape}")

    df_merged.to_csv(OUTPUT_MERGED_PATH, index=False)

    print("\n" + "=" * 80)
    print("FEATURE EXTRACTION COMPLETE FOR THIS ALGORITHM")
    print("=" * 80)

    print(f"\nOutput saved to: {OUTPUT_MERGED_PATH}")
    print(f"Samples: {len(df_merged)}")
    print(f"Total features: {len(df_merged.columns)}")

    print("\nNext step:")
    print("  Repeat this script for the next algorithm")

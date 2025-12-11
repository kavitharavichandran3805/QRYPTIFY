# import pandas as pd
# import numpy as np
# import os
# from nistrng import run_all_battery

# def run_nist_tests_on_dataset(file_path: str, min_bits: int = 1000):
    
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"File not found: {file_path}")

#     print(f"\n🔹 Processing file: {os.path.basename(file_path)}")

    
#     df = pd.read_csv(file_path)

#     if "Encrypted_Data" not in df.columns:
#         raise ValueError("The file does not contain an 'Encrypted_Data' column.")

#     total_rows = len(df)
#     print(f"   Total rows: {total_rows}")

#     nist_test_names = [
#         "Frequency",
#         "BlockFrequency",
#         "CumulativeSums",
#         "Runs",
#         "LongestRun",
#         "Rank",
#         "FFT",
#         "NonOverlappingTemplate",
#         "OverlappingTemplate",
#         "Universal",
#         "ApproximateEntropy",
#         "RandomExcursions",
#         "RandomExcursionsVariant",
#         "Serial",
#         "LinearComplexity"
#     ]

#     for test in nist_test_names:
#         df[test] = np.nan

#     success_count = 0
#     fail_count = 0

#     for i, bits in enumerate(df["Encrypted_Data"]):
#         if i % 50 == 0:
#             print(f"   ✅ Processing row {i}/{total_rows}...")

#         try:
#             bit_string = str(bits).strip()
#             bit_array = [int(b) for b in bit_string if b in ['0', '1']]

#             if len(bit_array) < min_bits:
#                 print(f"   ⚠️ Row {i}: Not enough bits ({len(bit_array)} < {min_bits})")
#                 fail_count += 1
#                 continue

#             sequence = np.array(bit_array, dtype=np.uint8)

#             results = run_all_battery(sequence, 'sts')
#             pvalues = {}
#             for test_result in results:
#                 test_name = test_result.name

#                 if hasattr(test_result, 'p_value') and test_result.p_value is not None:
#                     pvalues[test_name] = test_result.p_value

#                 elif hasattr(test_result, 'results') and test_result.results:
#                     all_pvals = [
#                         sub.p_value for sub in test_result.results
#                         if hasattr(sub, 'p_value') and sub.p_value is not None
#                     ]
#                     if all_pvals:
#                         pvalues[test_name] = float(np.mean(all_pvals))
#                     else:
#                         pvalues[test_name] = np.nan
#                 else:
#                     pvalues[test_name] = np.nan

#             for test in nist_test_names:
#                 df.at[i, test] = pvalues.get(test, np.nan)

#             success_count += 1

#         except Exception as e:
#             print(f"   ⚠️ Row {i} failed: {str(e)}")
#             fail_count += 1
#             for test in nist_test_names:
#                 df.at[i, test] = np.nan

#     df_result = df.drop(columns=["Encrypted_Data"])

#     base_name = os.path.splitext(file_path)[0]
#     new_path = f"{base_name}_nist_results.csv"
#     df_result.to_csv(new_path, index=False)

#     print(f"\n✅ Processing complete!")
#     print(f"   Successful: {success_count}/{total_rows}")
#     print(f"   Failed: {fail_count}/{total_rows}")
#     print(f"📄 Results saved to: {new_path}")

#     return new_path

# if __name__ == "__main__":
#     file_path = r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\large_encrypted_dataset\aes_ctr_bits.csv" 
#     try:
#         result_file = run_nist_tests_on_dataset(file_path, min_bits=1000)
#     except Exception as e:
#         print(f"❌ Error: {str(e)}")


# import pandas as pd
# import numpy as np
# import os
# from nistrng import *

# def run_nist_tests_on_dataset(file_path: str, min_bits: int = 1000):
#     """
#     Runs NIST statistical tests (via nistrng) on each bitstring in 'Encrypted_Data' column.
#     Stores p-values for 15 tests in the output CSV.
#     """

#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"File not found: {file_path}")

#     print(f"\n🔹 Processing file: {os.path.basename(file_path)}")

#     df = pd.read_csv(file_path)

#     if "Encrypted_Data" not in df.columns:
#         raise ValueError("The file does not contain an 'Encrypted_Data' column.")

#     total_rows = len(df)
#     print(f"   Total rows: {total_rows}")

#     nist_test_names = [
#         "Frequency",
#         "BlockFrequency",
#         "CumulativeSums",
#         "Runs",
#         "LongestRun",
#         "Rank",
#         "FFT",
#         "NonOverlappingTemplate",
#         "OverlappingTemplate",
#         "Universal",
#         "ApproximateEntropy",
#         "RandomExcursions",
#         "RandomExcursionsVariant",
#         "Serial",
#         "LinearComplexity"
#     ]

#     for test in nist_test_names:
#         df[test] = np.nan

#     success_count = 0
#     fail_count = 0

#     for i, bits in enumerate(df["Encrypted_Data"]):
#         if i % 50 == 0:
#             print(f"   ✅ Processing row {i}/{total_rows}...")

#         try:
#             bit_string = str(bits).strip()
#             bit_array = [int(b) for b in bit_string if b in ['0', '1']]

#             if len(bit_array) < min_bits:
#                 print(f"   ⚠️ Row {i}: Not enough bits ({len(bit_array)} < {min_bits})")
#                 fail_count += 1
#                 continue

#             sequence = np.array(bit_array, dtype=np.uint8)
#             eligibility = check_eligibility_all_ones(sequence)  # ✅ FIXED

#             pvalues = {}

#             try:
#                 result = monobit_test(sequence, eligibility)
#                 pvalues["Frequency"] = result.score if result else np.nan
#             except:
#                 pvalues["Frequency"] = np.nan

#             try:
#                 result = frequency_within_block_test(sequence, eligibility)
#                 pvalues["BlockFrequency"] = result.score if result else np.nan
#             except:
#                 pvalues["BlockFrequency"] = np.nan

#             try:
#                 results_list = cumulative_sums_test(sequence, eligibility)
#                 pvals = [r.score for r in results_list if hasattr(r, "score")]
#                 pvalues["CumulativeSums"] = np.mean(pvals) if pvals else np.nan
#             except:
#                 pvalues["CumulativeSums"] = np.nan

#             try:
#                 result = runs_test(sequence, eligibility)
#                 pvalues["Runs"] = result.score if result else np.nan
#             except:
#                 pvalues["Runs"] = np.nan

#             try:
#                 result = longest_run_ones_in_a_block_test(sequence, eligibility)
#                 pvalues["LongestRun"] = result.score if result else np.nan
#             except:
#                 pvalues["LongestRun"] = np.nan

#             try:
#                 result = binary_matrix_rank_test(sequence, eligibility)
#                 pvalues["Rank"] = result.score if result else np.nan
#             except:
#                 pvalues["Rank"] = np.nan

#             try:
#                 result = dft_test(sequence, eligibility)
#                 pvalues["FFT"] = result.score if result else np.nan
#             except:
#                 pvalues["FFT"] = np.nan

#             try:
#                 results_list = non_overlapping_template_matching_test(sequence, eligibility)
#                 pvals = [r.score for r in results_list if hasattr(r, "score")]
#                 pvalues["NonOverlappingTemplate"] = np.mean(pvals) if pvals else np.nan
#             except:
#                 pvalues["NonOverlappingTemplate"] = np.nan

#             try:
#                 result = overlapping_template_matching_test(sequence, eligibility)
#                 pvalues["OverlappingTemplate"] = result.score if result else np.nan
#             except:
#                 pvalues["OverlappingTemplate"] = np.nan

#             try:
#                 result = maurers_universal_test(sequence, eligibility)
#                 pvalues["Universal"] = result.score if result else np.nan
#             except:
#                 pvalues["Universal"] = np.nan

#             try:
#                 result = approximate_entropy_test(sequence, eligibility)
#                 pvalues["ApproximateEntropy"] = result.score if result else np.nan
#             except:
#                 pvalues["ApproximateEntropy"] = np.nan

#             try:
#                 results_list = random_excursion_test(sequence, eligibility)
#                 pvals = [r.score for r in results_list if hasattr(r, "score")]
#                 pvalues["RandomExcursions"] = np.mean(pvals) if pvals else np.nan
#             except:
#                 pvalues["RandomExcursions"] = np.nan

#             try:
#                 results_list = random_excursion_variant_test(sequence, eligibility)
#                 pvals = [r.score for r in results_list if hasattr(r, "score")]
#                 pvalues["RandomExcursionsVariant"] = np.mean(pvals) if pvals else np.nan
#             except:
#                 pvalues["RandomExcursionsVariant"] = np.nan

#             try:
#                 results_list = serial_test(sequence, eligibility)
#                 pvals = [r.score for r in results_list if hasattr(r, "score")]
#                 pvalues["Serial"] = np.mean(pvals) if pvals else np.nan
#             except:
#                 pvalues["Serial"] = np.nan

#             try:
#                 result = linear_complexity_test(sequence, eligibility)
#                 pvalues["LinearComplexity"] = result.score if result else np.nan
#             except:
#                 pvalues["LinearComplexity"] = np.nan

#             for test in nist_test_names:
#                 df.at[i, test] = pvalues.get(test, np.nan)

#             success_count += 1

#         except Exception as e:
#             print(f"   ⚠️ Row {i} failed: {str(e)}")
#             fail_count += 1
#             for test in nist_test_names:
#                 df.at[i, test] = np.nan

#     df_result = df.drop(columns=["Encrypted_Data"])
#     new_path = os.path.splitext(file_path)[0] + "_nist_results.csv"
#     df_result.to_csv(new_path, index=False)

#     print(f"\n✅ Processing complete!")
#     print(f"   Successful: {success_count}/{total_rows}")
#     print(f"   Failed: {fail_count}/{total_rows}")
#     print(f"📄 Results saved to: {new_path}")

#     return new_path


# if __name__ == "__main__":
#     file_path = "/content/aes_ctr_bits.csv"
#     run_nist_tests_on_dataset(file_path)

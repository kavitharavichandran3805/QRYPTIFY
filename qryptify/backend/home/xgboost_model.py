import pandas as pd


def feed_nist_data(nist_test_df: pd.DataFrame) -> dict:
    df=nist_test_df
    print(df.head())
    return {
        "status":True,
        "predicted_algorithm":"AES",
        "predicted_algorithm_confidence_score":"94"
    }
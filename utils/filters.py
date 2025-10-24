import pandas as pd

def filter_by_confidence(df, min_confidence=10):
    """
    Filters wildfire DataFrame to include only entries
    with confidence >= min_confidence or labeled 'nominal'/'high'.
    """
    if df.empty:
        return df

    if "confidence" in df.columns:
        try:
            df["conf_num"] = pd.to_numeric(df["confidence"], errors="coerce")
            df_num = df[df["conf_num"].fillna(0) >= min_confidence]
            df_txt = df[df["confidence"].isin(["n","l","h"])]
            df = pd.concat([df_num, df_txt]).drop_duplicates()
        except Exception:
            df = df[df["confidence"].isin(["n","l","h"])]
    return df

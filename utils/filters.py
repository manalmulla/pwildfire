import pandas as pd

def filter_by_confidence(df, min_confidence=30):
    """
    Filters wildfire DataFrame to include only entries
    with confidence >= min_confidence.
    Handles both numeric and text-based confidence values.
    """
    if df.empty:
        return df

    if "confidence" in df.columns:
        try:
            df["conf_num"] = pd.to_numeric(df["confidence"], errors="coerce")
            df = df[df["conf_num"].fillna(0) >= min_confidence]
        except Exception:
            df = df[df["confidence"].isin(["nominal", "high", "h"])]
    return df

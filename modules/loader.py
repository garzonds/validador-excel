import pandas as pd

def load_excel(filepath: str) -> pd.DataFrame:
    """Lee el Excel y retorna un DataFrame limpio."""
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    return df

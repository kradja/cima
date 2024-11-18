import pandas as pd
import pyarrow as pa
from pathlib import Path
from matplotlib import pyplot as plt

if __name__ == "__main__":
    data = Path("./prob_solv")
    breast = data.glob("BRCA*")
    lung = data.glob("LUAD*")
    concat_breast = data.parent / "concat_breast_df.pkl"
    concat_lung= data.parent / "concat_lung_df.pkl"
    if concat_breast.exists():
        bdf = pd.read_pickle(concat_breast)
    else:
        breast_df = [pd.read_excel(f,dtype_backend = 'pyarrow',engine='openpyxl') for f in breast]
        bdf = pd.concat(breast_df)
        bdf.to_csv("concat_breast_df.csv")
        bdf.to_pickle("concat_breast_df.pkl")
        bdf.to_parquet("concat_breast_df.parquet")
    if concat_lung.exists():
        ldf = pd.read_pickle(concat_lung)
    else:
        lung_df = [pd.read_excel(f,dtype_backend = 'pyarrow',engine='openpyxl') for f in lung]
        ldf = pd.concat(lung_df)
        ldf.to_csv("concat_lung_df.csv")
        ldf.to_pickle("concat_lung_df.pkl")
        ldf.to_parquet("concat_lung_df.parquet")
    print("End")



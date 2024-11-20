import pandas as pd
import pyarrow as pa
from pathlib import Path
from matplotlib import pyplot as plt

if __name__ == "__main__":
    data = Path(__file__).parents[1] / "data"
    raw_data = data / "raw_data"
    breast = list(raw_data.glob("BRCA*"))
    lung = list(raw_data.glob("LUAD*"))
    concat_breast = data / "concat_breast_df_patient.pkl"
    concat_lung= data / "concat_lung_df_patient.pkl"
    if concat_breast.exists():
        bdf = pd.read_pickle(concat_breast)
    else:
        file_stem = [f.stem for f in breast]
        breast_df = [pd.read_excel(f,dtype_backend = 'pyarrow',engine='openpyxl') for f in breast]
        bdf = pd.concat(breast_df, keys=file_stem)
        bdf.to_csv(data / "concat_breast_df_patient.csv")
        bdf.to_pickle(data / "concat_breast_df_patient.pkl")
        bdf.to_parquet(data / "concat_breast_df_patient.parquet")
    if concat_lung.exists():
        ldf = pd.read_pickle(concat_lung)
    else:
        file_stem = [f.stem for f in lung]
        lung_df = [pd.read_excel(f,dtype_backend = 'pyarrow',engine='openpyxl') for f in lung]
        ldf = pd.concat(lung_df, keys=file_stem)
        ldf.to_csv(data / "concat_lung_df_patient.csv")
        ldf.to_pickle(data / "concat_lung_df_patient.pkl")
        ldf.to_parquet(data / "concat_lung_df_patient.parquet")
    print("End")



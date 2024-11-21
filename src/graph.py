import pandas as pd
import pyarrow as pa
from pathlib import Path
from matplotlib import pyplot as plt
from typing import Generator

def file_search(input_dir: Path, search_str: str):
    return input_dir.glob(search_str)

def load_or_concat(output_dir: Path, file_gen: Generator, file_name: str):
    output_file = output_dir / file_name
    if output_file.exists():
        return pd.read_pickle(output_file)
    else:
        return concat_excel_files(file_gen, output_file)

def concat_excel_files(file_gen: Generator, output_file: Path):
    read_files = [(f.stem, pd.read_excel(f,dtype_backend = 'pyarrow',engine='openpyxl')) for f in file_gen]
    file_stem, df = zip(*read_files)
    df = pd.concat(df, keys=file_stem)
    df.to_csv(output_file.with_suffix(".csv"))
    df.to_pickle(output_file.with_suffix(".pkl"))
    df.to_parquet(output_file.with_suffix(".parquet"))

if __name__ == "__main__":
    data = Path(__file__).parents[1] / "data"
    raw_data = data / "raw_data"
    breast = file_search(raw_data, "BRCA*")
    lung = file_search(raw_data, "LUAD*")
    concat_breast = data / "concat_breast_df_patient2"
    concat_lung = data / "concat_lung_df_patient2"
    bdf = load_or_concat(data, breast, "concat_breast_df_patient2")
    ldf = load_or_concat(data, lung, "concat_lung_df_patient2")
    

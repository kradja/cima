import pandas as pd
import pyarrow as pa
from pathlib import Path
from matplotlib import pyplot as plt
from typing import Generator
from inspect import isfunction

def file_search(input_dir: Path, search_str: str):
    """ Search for files in a directory based on a search string
    """
    return input_dir.glob(search_str)

def pandas_read_write_types(suffix: str):
    if suffix == ".csv":
        return pd.read_csv, "to_csv"
    elif suffix == ".pkl":
        return pd.read_pickle, pd.to_pickle
    elif suffix == ".parquet":
        return pd.read_parquet, "to_parquet"
    else:
        raise ValueError("Suffix not supported")

def load_or_concat(file_gen: Generator, output_file: Path, suffix: str = ".csv") -> pd.DataFrame:
    """ Load DataFrame from file if it exists, otherwise concatenate excel files
    """
    outfile = output_file.with_suffix(suffix)
    if outfile.exists():
        toread, _ = pandas_read_write_types(suffix)
        return toread(outfile)
    else:
        out_df = concat_excel_files(file_gen)
        write_df(out_df, output_file, [".csv", ".pkl", ".parquet"])

def write_df(df: pd.DataFrame, output_file: Path, suffix_list: list) -> pd.DataFrame:
    """ Write DataFrame to file with multiple suffixes
    """
    for suffix in suffix_list:
        outfile = output_file.with_suffix(suffix)
        if not outfile.exists():
            _, to_write = pandas_read_write_types(suffix)
            if isfunction(to_write): #type(to_write) == function:
                to_write(df, outfile)
            else:
                df.__getattr__(to_write)(outfile)

def concat_excel_files(file_gen: Generator):
    """ Concatenate excel files into a single DataFrame, engine is openpyxl
    """
    read_files = [(f.stem, pd.read_excel(f,dtype_backend = 'pyarrow',engine='openpyxl')) for f in file_gen]
    file_stem, df = zip(*read_files)
    return pd.concat(df, keys=file_stem)

def til_criteria(input_df: pd.DataFrame):
    """ Filter TILs based on the following criteria:
        Nucleus: Area >= 38.45 and <= 78.5
        Nucleus: Hematoxylin OD mean >= 0.75
    """
    filt_input_df = input_df[input_df["Nucleus: Area"] >= 38.45]
    filt_input_df = filt_input_df[filt_input_df["Nucleus: Area"] <= 78.5]
    filt_input_df = filt_input_df[filt_input_df["Nucleus: Hematoxylin OD mean"] >= 0.75]
    return filt_input_df

def process_raw_files(data: Path, raw_data: Path):
    breast = file_search(raw_data, "BRCA*")
    lung = file_search(raw_data, "LUAD*")
    concat_breast = data / "concat_breast_df_patient"
    concat_lung = data / "concat_lung_df_patient"
    bdf = load_or_concat(breast, concat_breast,".pkl")
    ldf = load_or_concat(lung, concat_lung,".pkl")
    return bdf, ldf

def filter_tils(bdf: pd.DataFrame, ldf: pd.DataFrame):
    tils_concat_breast = data / "lung_filtered_tils_patient"
    tils_concat_lung = data / "breast_filtered_tils_patient"
    filt_bdf = til_criteria(bdf)
    filt_ldf = til_criteria(ldf)
    write_df(filt_bdf, tils_concat_breast, [".csv",".pkl"])
    write_df(filt_ldf, tils_concat_lung, [".csv",".pkl"])
    return filt_bdf, filt_ldf

if __name__ == "__main__":
    data = Path(__file__).parents[1] / "data"
    raw_data = data / "raw_data"
    bdf, ldf = process_raw_files(data, raw_data)
    filt_bdf, filt_ldf = filter_tils(bdf, ldf)

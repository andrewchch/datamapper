import pandas as pd
import re
import shutil
import argparse
import os
import sys
from tqdm import tqdm

clean_re = re.compile('[\\[\\]\\:\\/\\?\\*]')
MULTIVALUE_COLUMN_DELIM = '[\\[\\]\:]+'
SUBROWS_RE = re.compile('\\[(.*?)\\]')
FIELD_DELIM_RE = re.compile('(?<!\s):(?!\s)')
multivalue_column_delim_re = re.compile(MULTIVALUE_COLUMN_DELIM)


# Load Excel file into pandas dataframe
def load_excel_to_dataframe(file_path):
    return pd.read_excel(file_path, engine='openpyxl')


# Get describe() results for each column
def get_describe_results(dataframe):
    _describe_results = {}
    for column in tqdm(dataframe.columns, desc="Getting describes for each column", unit="item"):
        _describe_results[column] = dataframe[column].describe()

    return _describe_results


def make_copy_name(filename):
    base_name = os.path.splitext(filename)[0]  # get the file name without extension
    extension = os.path.splitext(filename)[1]  # get the file extension
    new_filename = f"{base_name}_out{extension}"
    return new_filename


# Add new sheets to Excel file for each describe() result
def add_describe_sheets(file_path, _describe_results):
    writer = pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay')

    # Add two sheets for numeric and object fields
    all_rows = []

    for column in tqdm(sorted(_describe_results.keys()), desc="Building describe results", unit="item"):
        results = _describe_results[column]
        all_rows.append(results)

    merged_df = pd.DataFrame(all_rows)

    merged_df.to_excel(writer, sheet_name='merged fields')

    writer.close()


def parse_col(row, col):
    if pd.isna(row[col]):
        return None

    # Find all bracketed text matches in the column
    matches = SUBROWS_RE.findall(row[col])
    # Split each match on ':' and convert to DataFrame
    new_df = pd.DataFrame([FIELD_DELIM_RE.split(m) for m in matches])
    # Assign column names based on the original column name
    col_matches = SUBROWS_RE.split(col)
    sub_cols = FIELD_DELIM_RE.split(col_matches[1])
    col_prefix = col_matches[0].strip()
    new_df.columns = ['%s_%s' % (col_prefix, x) for x in sub_cols]
    return new_df


def main():
    parser = argparse.ArgumentParser(description="Process some file.")
    parser.add_argument('filename', type=str, help='The name of the file to process.')

    args = parser.parse_args()
    src = args.filename
    tgt = make_copy_name(src)

    # Create a working copy from the backup file
    shutil.copyfile(src, tgt)

    # Process the file
    sys.stdout.write('Loading file..')
    df = load_excel_to_dataframe(tgt)

    # Further split columns that contain delimited values into additional
    # Iterate over columns to find ones with bracketed sub-column names
    for col in tqdm(df.columns, desc="Expanding delimited columns", unit="column"):
        if ' [' in col and ':' in col and ']' in col:
            # Parse this column into a list of DataFrames
            dfs = []
            for _, row in df.iterrows():
                _new_df = parse_col(row, col)
                if _new_df is not None:
                    dfs.append(_new_df)

            # Concatenate these DataFrames into one
            if len(dfs) > 0:
                parsed_df = pd.concat(dfs)
                # Reset the index
                parsed_df.reset_index(drop=True, inplace=True)
                # Add the parsed DataFrame to the original DataFrame, dropping the original column
                df = pd.concat([df, parsed_df], axis=1).drop(columns=col)

    sys.stdout.write('Getting describe results..')
    describe_results = get_describe_results(df)

    sys.stdout.write('Writing describe results..')
    add_describe_sheets(tgt, describe_results)


if __name__ == "__main__":
    main()

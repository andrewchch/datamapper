import pandas as pd
import re
import shutil
import argparse
import os
import sys
from tqdm import tqdm

clean_re = re.compile('[\\[\\]\\:\\/\\?\\*]')


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

    for column, results in tqdm(_describe_results.items(), desc="Building describe results", unit="item"):
        all_rows.append(results)

    merged_df = pd.DataFrame(all_rows)

    merged_df.to_excel(writer, sheet_name='merged fields')

    writer.close()


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

    sys.stdout.write('Getting describe results..')
    describe_results = get_describe_results(df)

    sys.stdout.write('Writing describe results..')
    add_describe_sheets(tgt, describe_results)


if __name__ == "__main__":
    main()

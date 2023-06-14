import pandas as pd
import re
import shutil
import argparse
import os
import sys
import logging

from tqdm import tqdm

# Create a custom logger
logger = logging.getLogger()

# Create handlers
c_handler = logging.StreamHandler()

# Create formatters and add it to handlers
c_format = logging.Formatter('%(levelname)s: %(message)s')
c_handler.setFormatter(c_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.setLevel(logging.INFO)  # Set level to DEBUG, INFO, WARNING, ERROR, CRITICAL as needed

sheets = [
    'Programme Definition',
    'Subject',
    'Prog Outcome (Award)',
    'Prog Intake',
    'Course Definition',
    'Course Outcome',
    'Course Occurrence'
]


# Load Excel file into pandas dataframe
def load_excel_to_dataframe(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')


def main():
    parser = argparse.ArgumentParser(description="Process some file.")
    parser.add_argument('filename', type=str, help='The name of the file to process.')

    args = parser.parse_args()
    src = args.filename

    # Create a working copy from the backup file
    # shutil.copyfile(src, tgt)

    # Process the file
    sys.stdout.write('Loading file..')
    sheet_dfs = []

    for sheet in sheets:
        df = pd.read_excel(src, sheet_name=sheet, engine='openpyxl')
        df['sheet'] = sheet
        df['Jade Location'] = df['Jade Location'].replace('Details', sheet)
        second_column_name = df.columns[1]
        df.rename(columns={second_column_name: 'FieldName'}, inplace=True)

        sheet_dfs.append(df)

    combined_df = pd.concat(sheet_dfs, ignore_index=True)

    combined_df[['sheet', 'FieldName', 'Jade Location']].to_csv('attributes.csv', sep='|', index=False)


if __name__ == "__main__":
    main()

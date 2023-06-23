import pandas as pd
import numpy as np
import argparse
import sys
import logging

from tqdm import tqdm

MIGRATION_STATUS_COL = 'Suggestion for future state CDM (include, exclude, combine, modify)'
SUGGESTED_FUTURE_ENTITY_COL = 'Data defined in relation to future state curriculum entity Level 1:'
POPULATED_COL = 'Field populated for live/pending curriculum'

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
    'Prog Definition',
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


def strip_trailing_spaces(value):
    if pd.isna(value):
        return np.nan
    elif isinstance(value, str):
        return value.rstrip()
    else:
        return value


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
        df['Jade Location'] = df['Jade Location'].replace('Details', sheet).replace('Programme Details', 'Prog Definition')
        second_column_name = df.columns[1]
        df.rename(columns={second_column_name: 'FieldName'}, inplace=True)

        df['FieldName'] = df['FieldName'].str.rstrip()
        df['Data type'] = df['Data type'].apply(strip_trailing_spaces)

        filtered_df = df[
                            (~df[MIGRATION_STATUS_COL].str.contains('Exclude', na=True) | pd.isna(df[MIGRATION_STATUS_COL])) &
                            ((df[POPULATED_COL].astype(float) == 1.0) | pd.isna(df[POPULATED_COL]))
                         ]

        sheet_dfs.append(filtered_df)

    combined_df = pd.concat(sheet_dfs, ignore_index=True)

    combined_df[['sheet', 'FieldName', 'Data type', 'Maxlength', 'Jade Location']].to_csv('attributes.csv', sep='|', index=False)


if __name__ == "__main__":
    main()

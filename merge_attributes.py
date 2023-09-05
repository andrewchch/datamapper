"""
Merge all attributes from JADE and CIS workbooks into a single workbook to make processing it easier
"""

import pandas as pd
import numpy as np
import sys
import logging
import os
import glob

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

workbooks = {
    'Course Maintenance-CIS data assessment_CM Project 2023.xlsx': {
        'sheets': [
            'Data fields'
        ],
        'fields': {
            'target_entity': 'CISRepl Table',
            'field_name_col': 4,
            'data_type': 'Field Type',
        }
    },
    'Jade Academic Model attributes_CM Project analysis.xlsx': {
        'sheets': [
            'Prog Definition',
            'Subject',
            'Prog Outcome (Award)',
            'Prog Intake',
            'Course Definition',
            'Course Outcome',
            'Course Occurrence'
        ],
        'fields': {
            'target_entity': 'Jade Location',
            'field_name_col': 1,
            'data_type': 'Data type',
            'migration_status_col': 'Suggestion for future state CDM (include, exclude, combine, modify)',
            'suggested_future_entity_col': 'Data defined in relation to future state curriculum entity Level 1:',
            'populated_col': 'Field populated for live/pending curriculum'
        }
    }
}


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


def process_file(src):
    sheet_dfs = []

    workbook_filename = os.path.basename(src)
    details = workbooks[workbook_filename]
    print('Loading file: %s' % workbook_filename)

    for sheet in details['sheets']:
        df = pd.read_excel(src, sheet_name=sheet, engine='openpyxl')

        df['workbook'] = workbook_filename
        df['sheet'] = sheet

        if 'Maxlength' not in df.columns:
            df['Maxlength'] = np.nan

        target = details['fields']['target_entity']
        field_name_col = details['fields']['field_name_col']
        data_type = details['fields']['data_type']

        df[target] = df[target].replace('Details', sheet).replace('Programme Details', 'Programme')

        # Rename the specified column in this sheet to "FieldName"
        df.rename(columns={list(df.columns)[field_name_col]: 'FieldName'}, inplace=True)

        df.rename(columns={data_type: 'DataType'}, inplace=True)
        df.rename(columns={target: 'TargetEntity'}, inplace=True)

        df['FieldName'] = df['FieldName'].str.rstrip()
        df['DataType'] = df['DataType'].apply(strip_trailing_spaces)

        sheet_dfs.append(df)

    combined_df = pd.concat(sheet_dfs, ignore_index=True)
    return combined_df


def main():
    # find all *.xlsx files in the "workbooks" subdirectory of the current directory and call process_file() on each
    workbook_dfs = []
    for src in glob.glob(os.path.join('workbooks', '*.xlsx')):
        workbook_dfs.append(process_file(src))

    combined_df = pd.concat(workbook_dfs, ignore_index=True)

    combined_df.to_excel('merged_attributes.xlsx', index=False)


if __name__ == "__main__":
    main()

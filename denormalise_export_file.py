import pandas as pd
import re
import argparse
import sys
import logging
import html
import os
import pickle

from tqdm import tqdm
from courseoutcome import parse_fixed_fields_input

# Create a custom logger
logger = logging.getLogger()

# Create handlers
c_handler = logging.StreamHandler()

# Create formatters and add it to handlers
c_format = logging.Formatter('%(levelname)s: %(message)s')
c_handler.setFormatter(c_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.setLevel(logging.DEBUG)  # Set level to DEBUG, INFO, WARNING, ERROR, CRITICAL as needed

clean_re = re.compile('[\\[\\]\\:\\/\\?\\*]')
MULTIVALUE_COLUMN_DELIM = '[\\[\\]\:]+'
SUBROWS_RE = re.compile('\\[(.*?)\\]')
FIELD_DELIM_RE = re.compile('(?<!\s):(?!\s)')
SUBCOL_NAME_DELIM = ':'
multivalue_column_delim_re = re.compile(MULTIVALUE_COLUMN_DELIM)
oid_delim_re = re.compile(';')

def get_pickle_path(_file_name):
    _pickle_name = os.path.splitext(_file_name)[0]
    _pickle_path = os.path.join('data', 'denormalise_export_file', _pickle_name + '.pkl')

    return _pickle_path

def utf8_to_ascii_and_trim(s):
    if isinstance(s, str):
        ascii_str = ''
        for char in s:
            if ord(char) < 128:
                ascii_str += char
            else:
                ascii_str += html.escape(char)
            if len(ascii_str) > 255:
                break
        return ascii_str[:255]

    return s


# Load Excel file into pandas dataframe
def load_excel_to_dataframe(file_path, row_key):
    return pd.read_excel(file_path, engine='openpyxl', dtype={row_key: str})


def parse_col(series, col):
    try:
        dfs = []
        for idx, val in series.items():
            if pd.isna(val):
                continue

            # Special case: OIDs delimited by a semicolon
            if col.rfind('[OID]') > 0:
                matches = [m for m in oid_delim_re.split(val) if len(m) > 0]
                new_df = pd.DataFrame(matches)
            else:
                # Find all bracketed text matches in the column
                matches = SUBROWS_RE.findall(val)

                # If no matches (and we suspect this is delimited column) it might be a single value missing brackets so
                # try using the whole value instead
                # Split each match on ':' and convert to DataFrame
                if len(matches) == 0:
                    matches = [val]

                # Special case: Course outcome - outcome groups
                if col == 'Outcome groups[OID:Code:Valid from:Valid to]':
                    vals = [parse_fixed_fields_input(m) for m in matches]
                else:
                    vals = [FIELD_DELIM_RE.split(m) for m in matches]

                new_df = pd.DataFrame(vals)

            # Set the index name and values
            new_df.index = [idx] * len(new_df)
            new_df.index.name = 'OID'

            # Assign column names based on the original column name
            col_matches = SUBROWS_RE.split(col)
            sub_cols = col_matches[1].split(SUBCOL_NAME_DELIM)
            col_prefix = col_matches[0].strip()

            # If the number of sub-columns is greater than the number of values, log the rejected row and continue
            if len(sub_cols) != len(new_df.columns):
                logger.debug('Reject column: %s, idx: %s, value: %s, reason: %s' % (col, idx, val, 'Number of sub-columns is not equal to the number of values'))
                continue

            new_df.columns = ['%s_%s' % (col_prefix, x.strip()) for x in sub_cols]

            # Apply utf8_to_ascii function to all string columns
            for _col in new_df.select_dtypes(include=['object']).columns:
                new_df[_col] = new_df[_col].apply(utf8_to_ascii_and_trim)

            # Prefix the OID value with a string so that when we import into SQL Server it will be a string
            for _col in new_df.columns:
                if _col.rfind('OID') > 0:
                    # find the index of the OID column
                    new_df[_col] = new_df[_col].apply(lambda x: 'OID_%s' % x)

            dfs.append(new_df)

        # Concatenate these DataFrames into one
        combined_df = None
        if len(dfs) > 0:
            combined_df = pd.concat(dfs)

        return combined_df
    except Exception as e:
        logger.debug('Reject column: %s, reason: %s' % (col, str(e)))
        return None


def main():
    parser = argparse.ArgumentParser(description="Process some file.")
    parser.add_argument('filename', type=str, help='The name of the file to process.')
    parser.add_argument('key', type=str, help='The column to use as a unique row key')
    parser.add_argument('output_format', type=str, help='EXCEL or CSV (defaults to EXCEL)', nargs='?', default='EXCEL')

    args = parser.parse_args()
    src = args.filename
    row_key = args.key
    output_format = args.output_format

    # load the dataframe from a pickle
    _pickle_path = get_pickle_path(src)

    if os.path.exists(_pickle_path):
        sys.stdout.write('Loading from pickle..')
        with open(_pickle_path, 'rb') as f:
            df, linked_dfs = pickle.load(f)
        sys.stdout.write('Done.\n')
    else:
        # Process the file
        sys.stdout.write('Loading file..')
        df = load_excel_to_dataframe(src, row_key)

        # Prefix the key value with a string so that when we import into SQL Server it will be a string
        df[args.key] = df[args.key].apply(lambda x: 'OID_%s' % x)

        # Set the row key as index
        df.set_index([row_key], inplace=True)

        # Further split columns that contain delimited values into additional denormalised tables
        # Iterate over columns to find ones with bracketed sub-column names
        linked_dfs = {}
        cols_to_drop = []

        for col in tqdm(df.columns, desc="Expanding delimited columns", unit="column"):
            if '[' in col and ':' in col and ']' in col:
                # Collect these for later dropping from the combined dataframe
                cols_to_drop.append(col)

                # Parse this column into a list of (index, expanded columns) dataframes
                linked_dfs[col] = parse_col(df[col], col)
            elif col.rfind('[OID]') > 0:
                # Collect these for later dropping from the combined dataframe
                cols_to_drop.append(col)

                # Parse this column into a list of (index, expanded columns) dataframes
                linked_dfs[col] = parse_col(df[col], col)

        sys.stdout.write('Done.\n')

        # Drop the original columns
        df.drop(columns=cols_to_drop, inplace=True)

        # Save the dataframe to a pickle
        sys.stdout.write('Saving to pickle..')
        with open(_pickle_path, 'wb') as f:
            pickle.dump((df, linked_dfs), f)
        sys.stdout.write('Done.\n')

    # At this point we have:
    # - a series of linked dataframes that contain the same row key as the core dataframe and expanded columns
    # - a core dataframe with the expanded columns removed

    # Apply utf8_to_ascii function to all string columns
    for _col in df.columns:
        df[_col] = df[_col].apply(utf8_to_ascii_and_trim)

        # Prefix the OID value with a string so that when we import into SQL Server it will be a string
        if _col.rfind('OID') > 0:
            # find the index of the OID column
            df[_col] = df[_col].apply(lambda x: 'OID_%s' % x)

    # For each key and value in linked_dfs, write the value to a new sheet in an Excel file, where the sheet is named after the key
    # Create a new Excel file
    sys.stdout.write('Writing output..')

    # Write each linked_dfs dataframe to a CSV file if an optional output_form argument = "CSV" is provided to the script
    if output_format == 'CSV':
        # Write the core dataframe to the first sheet
        file_path = os.path.join('data', os.path.splitext(os.path.basename(src))[0], 'denormalised.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        df.to_csv(file_path, index=True, sep='|')

        for key, value in linked_dfs.items():
            if value is not None:
                sheet_name = key.split('[')[0].strip()
                # Create a file path: "data" / {source file without extension} / {sheet name}.csv and create the folders if they don't exist
                file_path = os.path.join('data', os.path.splitext(os.path.basename(src))[0], sheet_name[:31] + '.csv')
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                value.to_csv(file_path, index=True, sep='|')
    else:
        with pd.ExcelWriter('denormalised.xlsx') as writer:
            # Write the core dataframe to the first sheet
            df.to_excel(writer, sheet_name='core')

            # Write each linked dataframe to a separate sheet
            for key, value in linked_dfs.items():
                if value is not None:
                    sheet_name = key.split('[')[0].strip()
                    value.to_excel(writer, sheet_name=sheet_name[:31])

    sys.stdout.write('Done.\n')


if __name__ == "__main__":
    main()

import os
import glob
import pandas as pd


def process_file(src):
    workbook_filename = os.path.basename(src)
    df = None

    try:
        df = pd.read_excel(src, sheet_name='merged fields', engine='openpyxl')
        print('Loaded file: %s' % workbook_filename)
    except Exception as e:
        pass

    return df


def main():
    # find all *.xlsx files in the "workbooks" subdirectory of the current directory and call process_file() on each
    workbook_dfs = []
    for src in glob.glob('*_out.xlsx'):
        _df = process_file(src)
        if _df is not None:
            workbook_dfs.append(_df)

    combined_df = pd.concat(workbook_dfs, ignore_index=True)

    combined_df.to_csv('combined_fields.csv', sep='|', index=False)


if __name__ == "__main__":
    main()

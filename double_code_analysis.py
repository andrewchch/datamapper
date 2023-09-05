import pandas as pd

# Get a subset of the dataframe including columns with names starting with "Double"


def get_double_columns(dataframe):
    double_columns = ['Code']
    for column in dataframe.columns:
        if column.startswith('Double'):
            double_columns.append(column)

    return dataframe[double_columns]


# WRite this dataframe to an Excel file
def write_dataframe_to_excel(dataframe, file_path):
    dataframe.to_excel(file_path, index=False)


# Function to extract the alias code (up to the first space)
def extract_alias(code):
    return code.split(" ")[0] if pd.notnull(code) else None


# Function to find the cases where code A matches alias code B, but code B does not have code A as an alias
def find_mismatches(df, double_code_columns):
    mismatches = []
    for index, row in df.iterrows():
        code_A = row['Code']
        for col in double_code_columns:
            code_B = row[col]
            if pd.notnull(code_B):
                # Check if code B has code A as an alias
                code_B_row = df[df['Code'] == code_B]
                has_alias_A = any(code_B_row[col].apply(lambda x: x == code_A).any() for col in double_code_columns)
                if not has_alias_A:
                    mismatches.append((code_A, code_B))
    return mismatches

def main():
    df = pd.read_excel("Jade Course Outcomes data export 6.6.23.xlsx", engine='openpyxl')

    # Filter on the "Double coded course outcome (Double coding)" being equal to "TRUE"
    df = df[(df['Double coded course outcome (Double coding)'] is True) & (df['Status'] != 'Old')]
    doubles = get_double_columns(df)

    # Extracting the alias codes from the "DoubleCode" columns
    double_code_columns = [col for col in doubles.columns if col.startswith("DoubleCode")]

    # Applying the function to all the "DoubleCode" columns
    for col in double_code_columns:
        doubles[col] = doubles[col].apply(extract_alias)

    # Finding mismatches
    mismatches = find_mismatches(doubles, double_code_columns)
    mismatches_df = pd.DataFrame(mismatches, columns=['Code A', 'Code B'])

    # Save the mismatches to an Excel file
    output_path = "data\mismatches.xlsx"
    mismatches_df.to_excel(output_path, index=False)

if __name__ == "__main__":
    main()

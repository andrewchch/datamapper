import pandas as pd
import os
import pickle

from col_describe import parse_col
from tqdm import tqdm

"""
Orgs links to by entities:
"""


def safe_split(_row, _delim):
    r = str(_row)
    ret = []
    if len(r) > 0:
        ret = r.split(_delim)

    return ret


def get_pickle_path(_file_name):
    _pickle_name = os.path.splitext(_file_name)[0]
    _pickle_path = os.path.join('data', _pickle_name + '.pkl')

    return _pickle_path


def load_oids(_file_name):
    _pickle_name = '%s_oids.tmp' % os.path.splitext(_file_name)[0]
    _pickle_path = get_pickle_path(_pickle_name)
    _obj = None

    if os.path.exists(_pickle_path):
        with open(_pickle_path, 'rb') as f:
            _obj = pickle.load(f)

    return _obj


def save_oids(_file_name, _obj):
    _pickle_name = '%s_oids.tmp' % os.path.splitext(_file_name)[0]
    _pickle_path = get_pickle_path(_pickle_name)

    with open(_pickle_path, 'wb') as f:
        pickle.dump(_obj, f)

def load_excel(_file_name):
    # If a named pickle file exists, load it, otherwise load the excel file and save it as a pickle file
    # remove the .xlsx extension from the file name
    _pickle_path = get_pickle_path(_file_name)
    _df = None

    if os.path.exists(_pickle_path):
        _df = pd.read_pickle(_pickle_path)
    else:
        _df = pd.read_excel(_file_name, engine='openpyxl')
        _df.to_pickle(_pickle_path)

    return _df


def get_unique_oids(_file_name, file_data):
    # Get the dataframe for this file
    _df = load_excel(_file_name)
    unique_vals = set()

    for _column in file_data:
        _col_name = _column['column']
        _method = _column['method']

        if _method == 'delimited_oids':
            for _row in _df[_col_name]:
                unique_vals.update(safe_split(_row, _column['delimiter']))
        elif _method == 'grouped_orgs':
            _dfs = []

            # Parse each value in the target column for multiple delimited instances
            for _, _row in _df.iterrows():
                _new_df = parse_col(_row, _col_name)
                if _new_df is not None:
                    _dfs.append(_new_df)

            # Concatenate these expanded dataFrames into one, retaining only the OID column
            if len(_dfs) > 0:
                parsed_df = pd.concat(_dfs)
                # Reset the index
                parsed_df.reset_index(drop=True, inplace=True)
                # Add the unique values to the set
                unique_vals.update(parsed_df[parsed_df.columns[0]].unique())

        elif _method == 'org_name':
            # Look up an OrgUnitDesc in the jade_dataframe and return the OID value
            # val = jade_dataframe[jade_dataframe['Name'] == df[column]]['OID'].values[0]

            # Get the matching OID from the jade_dataframe dataset (using the OrgUnitDesc value) and add it to the set

            pass
        else:
            # no matching method
            pass

    return unique_vals


def main():
    # Load org units
    jade_dataframe = pd.read_excel(os.path.join("data", "jade_org_units.xlsx"), engine='openpyxl')
    ps_dataframe = pd.read_excel(os.path.join("data", "ps_org_units.xls"), sheet_name='OrganisationalUnit')

    # Compare the two dataframes on the OrgUnitDesc column in the ps_dataframe and the Name column in the jade_dataframe
    # and return the rows in jade_dataframe that do not have a matching row in ps_dataframe
    # missing_org_units = jade_dataframe[~jade_dataframe['Name'].isin(ps_dataframe['OrgUnitDesc'])]

    # Get unique OID values for each file
    file_org_unique_values = {}
    for file_name, fields in tqdm(file_org_fields.items(), desc='Loading files'):
        oids = load_oids(file_name)
        if oids is None:
            oids = get_unique_oids(file_name, fields)
            save_oids(file_name, oids)

        file_org_unique_values[file_name] = oids

    # Create a dictionary of all unique filename and column values in the file_org_unique_values dictionary across all files
    all_unique_values = set()
    for file_name, oids in file_org_unique_values.items():
        all_unique_values.update(oids)

    # Turns these strings into numbers
    all_unique_values = [float(x) for x in all_unique_values]

    # Build a dataframe of all rows in jade_dataframe with OID values that are in the all_unique_values set
    used_jade_org_units = jade_dataframe[jade_dataframe['OID'].isin(all_unique_values)]

    # Get all the unique OrgUnitDesc values from used_jade_org_units where the Name value is not in the ps_dataframe OrgUnitDesc column
    missing_jade_org_units = used_jade_org_units[~used_jade_org_units['Name'].isin(ps_dataframe['OrgUnitDesc'])]

    # Compare the unique values in the ps_dataframe to the unique values in the all_unique_values set
    # and return the rows in ps_dataframe that do not have a matching row in the file_org_unique_values dictionary
    missing_ps_org_units = ps_dataframe[~ps_dataframe['OrgUnitDesc'].isin(all_unique_values)]

    print(missing_ps_org_units)

"""
    'Jade Course Definitions data export 22.5.23.xlsx': [
        {
            'column': 'Deliverying organisational unit',
            'method': 'delimited_oids',
            'delimiter': ';'
        },
        {
            'column': 'Owning organisational unit',
            'method': 'delimited_oids',
            'delimiter': ';'
        },
        {
            'column': 'Security Relationships Associations',
            'method': 'delimited_oids',
            'delimiter': ';'
        },        
    ],
"""

file_org_fields = {
    'Jade Course Occurrence data export 9.6.23.xlsx': [
        {
            'column': 'Delivering Org Unit[OID:Delivering organisational unit:Associate from:Associate to]',
            'method': 'grouped_orgs'
        },
        {
            'column': 'Org Unit[OID:Owning organisational unit]',
            'method': 'grouped_orgs'
        },
        {
            'column': 'Security relationships[OID:College:School:Cell:SubCell:SubSubCell]',
            'method': 'grouped_orgs'
        },
    ],
    'Jade Course Outcomes data export 6.6.23.xlsx': [
        {
            'column': 'Org unit [OID:Owning organisational unit:Associate from:Associate to]',
            'method': 'grouped_orgs'
        },
        {
            'column': 'Security relationships[OID:College:School:Cell:SubCell:SubSubCell]',
            'method': 'grouped_orgs'
        },
    ],
    'Jade Programme definitions_0.5_WIP_Bo_18.5.23.xlsx': [
        {
            'column': 'Security relationships [OID:College:School:Cell:SubCell:SubSubCell]',
            'method': 'grouped_orgs'
        },
    ],
    'Jade Programme Intakes data export Bo 29.5.23.xlsx': [
        {
            'column': 'Org unit relationships [OID:College:School:Cell:SubCell:SubSubCell]',
            'method': 'grouped_orgs'
        },
    ],
    'Jade Programme Outcomes_0.5_Bo_19.5.23.xlsx': [
        {
            'column': 'Owning organisational unit',
            'method': 'org_name'
        },
    ],
    'Jade Subject_0.5_Bo_31.5.23.xlsx': [
        {
            'column': 'Org unit [OID:Owning organisational unit:Associate from:Associate to]',
            'method': 'grouped_orgs'
        },
    ]
}

if __name__ == "__main__":
    main()




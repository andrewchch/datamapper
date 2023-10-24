import os
import pandas as pd

# Load the data from the provided Excel file
data = pd.read_excel(os.path.join('data', 'PeopleSoft Departments export for Jade 18.4.23.xlsx'))

# Define a Level 1 parent called "UC"
level_1 = pd.DataFrame({
    'child_id': ['UCA'],
    'child_name': ['UC'],
    'child_level': [1],
    'parent_id': [None],
    'parent_name': [None]
})

# Create rows for Level 4 with Level 3 as parent
level_4 = pd.DataFrame({
    'child_id': data['Dept'],
    'child_name': data['Full Description'],
    'child_level': [4] * len(data),
    'parent_id': data['UC Dept'],
    'parent_name': data['UC Dept Descr']
}).drop_duplicates()

# Remove any level 4 rows where the Dept column equals the UC Dept column
level_4 = level_4[level_4['child_id'] != level_4['parent_id']]

# Create rows for Level 3 with Level 2 as parent
level_3 = pd.DataFrame({
    'child_id': data['UC Dept'],
    'child_name': data['UC Dept Descr'],
    'child_level': [3] * len(data['UC Dept']),
    'parent_id': data['College'],
    'parent_name': data['College Desc']
}).drop_duplicates()

# Remove any level 3 rows where the Dept column equals the UC Dept column
level_3 = level_3[level_3['child_id'] != level_3['parent_id']]

# Create rows for Level 2 with Level 1 ("UC") as parent
level_2 = pd.DataFrame({
    'child_id': data['College'],
    'child_name': data['College Desc'],
    'child_level': [2] * len(data['College']),
    'parent_id': ['UCA'] * len(data['College']),
    'parent_name': ['UC'] * len(data['College'])
}).drop_duplicates()

# Concatenate all levels together
restructured_data = pd.concat([level_1, level_4, level_3, level_2], axis=0).reset_index(drop=True).drop_duplicates()
restructured_data = restructured_data[restructured_data['child_id'] != restructured_data['parent_id']]

# Write the restructured data to an Excel file
restructured_data.to_excel(os.path.join('data', 'restructured_ps_org_units.xlsx'), index=False)

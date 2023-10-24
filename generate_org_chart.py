import os
import pandas as pd
import json
import argparse
from jinja2 import Template


config = {
    'cms_org_units.xls': {
        'child_id_field': 'OID',
        'child_name_field': 'Name',
        'child_code_field': 'Abbreviated name',
        'child_level_field': 'Org unit level',
        'parent_id_field': 'Parent school/section OID',
        'parent_name_field': 'Parent school/section',
        'course_counts': 'Course counts',
        'load_used_orgs': True
    },
    'restructured_ps_org_units.xlsx': {
        'child_id_field': 'child_id',
        'child_name_field': 'child_name',
        'child_code_field': 'child_code',
        'child_level_field': 'child_level',
        'parent_id_field': 'parent_id',
        'parent_name_field': 'parent_name',
        'load_used_orgs': False
    }
}


# Modify the build_tree function to recursively include all children, not just top-level nodes
def build_tree_recursive(full_df, file_config, _visited, _used_jade_orgs, parent_oid=None):
    tree = []

    subset = full_df[full_df[file_config['parent_id_field']] == parent_oid]

    for _, row in subset.iterrows():
        node_name = row[file_config['child_name_field']]
        node_id = row[file_config['child_id_field']]
        node_code = row[file_config['child_code_field']]

        if node_id in _visited:
            print('Skipping %s, ID: %s' % (node_name, node_id))
            continue
        _visited[node_id] = True

        if _used_jade_orgs is not None:
            used = str(node_id) in _used_jade_orgs
        else:
            used = True

        # Get the course counts for this org unit
        course_counts = 'course_counts' in file_config and row[file_config['course_counts']] or 0
        if pd.isna(course_counts):
            course_counts = 0

        # Build the tree of children
        children = build_tree_recursive(full_df, file_config, _visited, _used_jade_orgs, node_id)

        # Get the course counts for this and all child org units
        course_counts = course_counts + sum([c['course_counts'] for c in children])

        # print('children: %s' % len(children))
        node = {
            'name': node_name,
            'oid': node_id,
            'code': node_code,
            'level': str(row[file_config['child_level_field']])[-1:],
            'used': used and course_counts > 0,
            'course_counts': course_counts
        }
        if children:
            node['children'] = children

            # If any of the child nodes have used = True, set this node's used value to True
            if any([c['used'] for c in children]):
                node['used'] = True
        tree.append(node)

    return tree


def main():
    parser = argparse.ArgumentParser(description="Process an org hierarchy file.")
    parser.add_argument('filename', type=str, help='The name of the file to process.')

    args = parser.parse_args()
    src = args.filename

    # Load the Excel file into a DataFrame
    df = pd.read_excel(os.path.join('data', src))

    file_config = config[src]
    used_jade_orgs = None

    if file_config['load_used_orgs']:
        # Load the list of used org unit OIDs from the Excel file
        used_orgs_df = pd.read_excel(os.path.join('data', 'used_jade_orgs.xlsx'))
        # used_orgs_df['OID'] = used_orgs_df['OID'].str[4:]

        # create a dict from the keys in the used_orgs_df dataframe
        used_jade_orgs = dict.fromkeys(used_orgs_df['OID'])

    # If the file is "cms_org_units.xls", filter out any rows where the "Valid to" column is empty or earlier than today
    if src == 'cms_org_units.xls':
        df = df[df['Valid to'].isna() | (df['Valid to'] > pd.Timestamp.today())]

    # Create a forest data structure by identifying top-level nodes as those with "Org Unit Level2"
    visited = {}
    root = {
        'name': 'University of Canterbury',
        'oid': src == 'cms_org_units.xls' and 'OID_6078.1' or 'UCA',
        'code': 'UC',
        'level': '1',
        'used': True
    }

    forest_data = build_tree_recursive(df, file_config, visited, used_jade_orgs, root['oid'])
    root['children'] = forest_data

    # Define the D3.js HTML template as a string (escaped for Python multi-line string)
    # Load the D3.js HTML template from a file
    with open('d3_org_structure_template.template', 'r') as file:
        d3_template_str = file.read()

    # Use the modified template to generate the HTML file
    template = Template(d3_template_str)
    rendered_html = template.render(tree_data=json.dumps([root]))

    # Save the rendered HTML to a file
    output_file_path_forest = 'interactive_org_structure_forest.html'  # Replace with the desired output path
    with open(output_file_path_forest, 'w') as file:
        file.write(rendered_html)

    # Traverse forest_data and produce a flattened structure of the form: (child name, child level, parent name) using a recursive approach
    def traverse(node, parent_name, level):
        flattened_df.loc[len(flattened_df)] = [node['name'], node['code'], level, parent_name]
        if 'children' in node:
            for child in node['children']:
                if child['used']:
                    traverse(child, node['name'], level + 1)

    flattened_df = pd.DataFrame(columns=['Name', 'Code', 'Level', 'Parent'])
    traverse(root, None, 1)

    # Get any instances of the 'Code' value in flattened_df that are duplicated
    duplicated_codes = flattened_df[flattened_df.duplicated(['Code'])]['Code'].unique()

    # Create an excel file of the data in the format: name, code, level, parent
    output_file_path_excel = 'interactive_org_structure_excel.xlsx'  # Replace with the desired output path
    with pd.ExcelWriter(output_file_path_excel) as writer:
        pd.DataFrame(flattened_df).to_excel(writer, sheet_name='org_structure', index=False)


if __name__ == '__main__':
    main()


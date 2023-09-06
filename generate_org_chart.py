
import pandas as pd
import json
from jinja2 import Template


# Function to recursively build a tree from a DataFrame
def build_tree(_df, parent_column, child_column, level_column, level_value):
    tree = []
    subset = _df[_df[level_column] == level_value]
    for _, row in subset.iterrows():
        node_name = row[child_column]
        children = build_tree(_df[_df[parent_column] == node_name], parent_column, child_column, level_column, "Org Unit Level5")
        node = {'name': node_name}
        if children:
            node['children'] = children
        tree.append(node)
    return tree


# Modify the build_tree function to recursively include all children, not just top-level nodes
def build_tree_recursive(full_df, _visited, parent_name=None):
    tree = []
    print(parent_name)

    # The initial call to this function will have parent_name = None so the provided _df value will be the list of top level nodes
    if parent_name is None:
        subset = full_df[full_df['Parent school/section'] == 'University of Canterbury']
    else:
        subset = full_df[full_df['Parent faculty/division'] == parent_name]

    for _, row in subset.iterrows():
        node_name = row['Name']
        if node_name in _visited:
            print('Skipping %s' % node_name)
            continue
        visited[node_name] = True

        children = build_tree_recursive(full_df, visited, node_name)
        print('children: %s' % len(children))
        node = {'name': node_name}
        if children:
            node['children'] = children
        tree.append(node)

    return tree


# Load the Excel file into a DataFrame
file_path = 'cms_org_units.xls'  # Replace with the actual path to the Excel file
df = pd.read_excel(file_path)

# Create a forest data structure by identifying top-level nodes as those with "Org Unit Level2"
visited = {}
root = {
    'Name': 'University of Canterbury'
}
forest_data = build_tree_recursive(df, visited, None)
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

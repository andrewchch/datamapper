import os
import argparse
import xml.etree.ElementTree as ET

# Process each XML file in a specified directory
parser = argparse.ArgumentParser(description="Process each XML file in a specified directory.")
parser.add_argument('input_dir', help='The directory containing the XML files to process')
args = parser.parse_args()

# Get the current working directory
cwd = os.getcwd()

# Get the list of XML files in the input directory
files = [f for f in os.listdir(args.input_dir) if os.path.isfile(os.path.join(args.input_dir, f)) and f.endswith('.xml')]
pairs = []

# Process each file
for file in files:
    # Load the XML file and get the name of the root node
    tree = ET.parse(os.path.join(args.input_dir, file))
    root = tree.getroot()
    root_name = root.tag

    # Find the first "detail" node and extract the tag name and tag content of each child node
    detail = root.find('detail')
    children = [(child.tag, child.text) for child in detail]

    # Add the (root name, child name) pairs to a list
    for child_name, text in children:
        pairs.append((root_name, child_name, text))

# Write the list of pairs to a CSV file
with open(os.path.join(args.input_dir, 'fieldnames.csv'), 'w') as f:
    f.write('root,child,text\n')
    for pair in pairs:
        f.write('%s|%s|%s\n' % pair)




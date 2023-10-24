import argparse
import re
import os

from lxml import etree

MAXLENGTH = '255'
NS_PREFIXED_REGEX = re.compile(r'(\{(.*)\})?(.*)')


# Create a regular expression that splits a string of format "{namespace}element" into a tuple of (namespace, element)
def split_ns_prefixed_string(ns_prefixed_string):
    match = NS_PREFIXED_REGEX.match(ns_prefixed_string)
    if match:
        # We're ignoring the optional match.group(1) which is the namespace
        return match.group(2), match.group(3)
    else:
        return None, None


# Function to check if any ancestor has the 'DTS' namespace
def has_dts_ancestor(element, ns):
    while element is not None:
        if element.tag.startswith('{'+ns+'}'):
            return True
        element = element.getparent()
    return False


def update_length_attrib_iter(root, attribute_name, namespaces, prefix):
    ns = namespaces[prefix]
    elements_to_modify = []

    for element in root.iter():
        # Find either elements that have the NS or those with a parent containing the NS
        tag_prefix, tag = split_ns_prefixed_string(element.tag)
        if attribute_name in element.attrib:
            if tag_prefix is not None or has_dts_ancestor(element.getparent(), ns):
                elements_to_modify.append((element, attribute_name))
        else:
            # Fall back to searching each element's attributes for attribute_name matching part of the attribute name
            for attr in element.attrib:
                attr_ns_prefix, attr_name = split_ns_prefixed_string(attr)
                if attr_name == attribute_name:
                    elements_to_modify.append((element, attr))

        for el, attr_name in elements_to_modify:
            print('Modifying element: %s, attribute: %s' % (el.tag, attr_name))
            el.attrib[attr_name] = MAXLENGTH

def update_length_attrib(root, attribute_name, namespaces, prefix):
    ns = namespaces[prefix]

    # Find either elements that have the NS or those with a parent containing the NS
    elements_with_attr = root.xpath(".//*[@%s:%s]" % (prefix, attribute_name), namespaces=namespaces)
    elements_with_ancestors_with_ns = root.xpath(".//ancestor::%s:*[@%s]/.." % (prefix, attribute_name), namespaces=namespaces)

    # Combine the results
    elements_to_modify = elements_with_attr + elements_with_ancestors_with_ns

    # Update the elements
    for element in elements_to_modify:
        if '{%s}%s' % (ns, attribute_name) in element.attrib:
            element.attrib['{%s}%s' % (ns, attribute_name)] = '255'
        elif attribute_name in element.attrib:
            element.attrib[attribute_name] = '255'


def main():
    argparser = argparse.ArgumentParser(description="Process some file.")
    argparser.add_argument('filename', type=str, help='The name of the file to process.')

    args = argparser.parse_args()
    filename = args.filename

    # Load the .dtsx file
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(filename, parser)
    root = tree.getroot()

    namespaces = {'DTS': 'www.microsoft.com/SqlServer/Dts'}

    # Find the elements to modify
    update_length_attrib_iter(root, 'Length', namespaces, 'DTS')
    update_length_attrib_iter(root, 'MaximumWidth', namespaces, 'DTS')
    update_length_attrib_iter(root, 'cachedLength', namespaces, 'DTS')
    update_length_attrib_iter(root, 'length', namespaces, 'DTS')

    # Save the modified .dtsx file
    # get the filename using os.path splitting
    outfile = os.path.basename(filename)
    output_filename = filename.replace(outfile, 'modified_' + outfile)

    tree.write(output_filename, pretty_print=True, xml_declaration=True, encoding='UTF-8')


if __name__ == '__main__':
    main()



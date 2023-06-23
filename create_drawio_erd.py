import xml.etree.ElementTree as ET

# Input: Set of (entity, column, related_entity) tuples
input_data = [
    ('Person', 'id', None),
    ('Person', 'name', None),
    ('Person', 'address_id', 'Address'),
    ('Address', 'id', None),
    ('Address', 'street', None),
    ('Address', 'city', None)
]

# Create the base XML structure
mxfile = ET.Element('mxfile')
diagram = ET.SubElement(mxfile, 'diagram')
mxGraphModel = ET.SubElement(diagram, 'mxGraphModel')
root = ET.SubElement(mxGraphModel, 'root')

# Default parent
default_parent = ET.SubElement(root, 'mxCell', {'id': '0'})
default_parent_index = ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})

# Process entities
entities = {}
entity_counter = 2
for entity, column, related_entity in input_data:
    # Create entity if not created yet
    if entity not in entities:
        entity_element = ET.SubElement(root, 'mxCell', {
            'id': str(entity_counter),
            'value': '',
            'style': 'shape=table;tableName=' + entity,
            'vertex': '1',
            'parent': '1',
        })
        entity_counter += 1
        entities[entity] = entity_counter

    # Create column (as a child)
    ET.SubElement(root, 'mxCell', {
        'id': str(entity_counter),
        'value': column,
        'style': 'shape=table',
        'vertex': '1',
        'parent': str(entities[entity] - 1)
    })
    entity_counter += 1

# Second pass to create edges which relies on all entities having been created
for entity, column, related_entity in input_data:
    # Create relation if related_entity is not None
    if related_entity:
        ET.SubElement(root, 'mxCell', {
            'id': str(entity_counter),
            'value': '',
            'style': 'edgeStyle=entityRelationEdgeStyle',
            'edge': '1',
            'parent': '1',
            'source': str(entities[entity] - 1),
            'target': str(entities[related_entity] - 1)
        })
        entity_counter += 1

# Save the XML to a file
tree = ET.ElementTree(mxfile)
tree.write('output.drawio', encoding='utf-8', xml_declaration=True)
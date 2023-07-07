import csv
from graphviz import Digraph
from graphviz2drawio import graphviz2drawio

# Specify the file name
file_name = 'attributes.csv'
OUTPUT_NAME = 'EntityRelationshipDiagram'
output_filename_dot = '.'.join([OUTPUT_NAME, 'gv.dot'])
output_filename_drawio = '.'.join([OUTPUT_NAME, 'drawio'])
output_filename_gv = '.'.join([OUTPUT_NAME, 'gv'])

entity_mappings = {
    'Programmes': 'Programme',
    'Org Unit Relationships': 'Org Unit Relationship',
    'Co-requisites': 'Co-requisite',
    'Courses': 'Course',
    'Entry Criteria': 'Entry Criteria',
    'Restriction': 'Restriction',
    'Completion Rules': 'Completion Rule',
    '? Custom attributes': '',
    'Rules': 'Rule',
    'Additional Details': 'Additional Detail',
    'Programme': 'Programme',
    'Custom Attributes': 'Custom Attribute',
    'Re-entry Rule': 'Re-entry Rule',
    'Outcomes': 'Outcome',
    'Calendar': '',
    'Prog Definition': 'Programme',
    'Programme Outcome': 'Programme Outcome',
    'Outcome Groups': 'Outcome Groups',
    'Subject Options': 'Subject Options',
    'Composition': 'Composition',
    'Distributions': 'Distributions',
    'Subject URL': '',
    '?': '',
    'Banner': '',
    'Equivalent': 'Equivalent',
    'Parent/Child Relationship'
    'Org Unit Relationship': 'Org Unit Relationship',
    'Prog Intake': 'Programme Intake',
    'Fees': 'Fees',
    'Occurrence Groups': 'Occurrence Groups',
    'Prog Outcome (Award)': 'Programme Outcome',
    'Waitlist Template': 'Waitlist Template',
    'Course Outcome': 'Course Outcome',
    'Award Details': 'Programme Outcome',
    'Programme Intakes': 'Programme Intake',
    'Subjects': 'Subject',
    'Subject': 'Subject',
    'Calendar Details': '',
    'Course Definition': 'Course',
    'Downloadable Files': 'Downloadable Files',
    'Prerequisite': 'Prerequisite',
    'Course Occurrence': 'Course Occurrence',
    'Dissertattion/Theses': 'Dissertattion/Theses',
    'Enrolments': 'Enrolments'
}

# Initialize an empty list to store the tuples
_data = []

# Open the file
with open(file_name, 'r') as file:
    # Create a csv reader specifying the delimiter as '|'
    reader = csv.reader(file, delimiter='|')

    # This skips the first row of the CSV file.
    next(reader)

    # Loop through each row in the file
    for row in reader:
        # Convert the row to a tuple and append it to the list
        _data.append(tuple(row))


def generate_traditional_erd(data):
    # Create a Digraph object
    erd = Digraph(OUTPUT_NAME, node_attr={'shape': 'record'})

    # Keep track of entities and their attributes
    entities = {}

    # Loop through the data
    for entity_1, attribute, datatype, maxlength, related_entity in data:
        # Add attributes to entities
        if entity_1 not in entities:
            entities[entity_1] = []
        entities[entity_1].append(attribute)

        # Create an edge between entity and related entity
        erd.edge(entity_1, related_entity)

    # Add entities with attributes to the graph
    for entity, attributes in entities.items():
        label = '{' + entity + '|'
        label += '|'.join(attributes)
        label += '}'
        erd.node(entity, label=label)

    # Render the ERD to a file (creates 'EntityRelationshipDiagram.gv.pdf')
    erd.render(view=True)


def generate_erd_without_attributes(data):
    # Create a Digraph object
    erd = Digraph('EntityRelationshipDiagram', node_attr={'shape': 'box'}, engine='fdp')

    # Keep track of entities and connections already added
    entities = set()
    connections = set()

    # Map the degree to a color
    color_map = {1: 'lightblue', 2: 'lightgreen', 3: 'orange', 4: 'red'}
    MAX_COLOR = 'red'

    # Loop through the data
    for entity_1, attribute, datatype, maxlength, related_entity in data:
        entity_1 = entity_1.strip()
        attribute = attribute.strip()
        related_entity = related_entity.strip()

        # Find a canonical name, ignore if no matching name
        entity_1 = entity_mappings.get(entity_1, entity_1)
        related_entity = entity_mappings.get(related_entity, related_entity)

        if len(entity_1) == 0 or len(attribute) == 0 or len(related_entity) == 0:
            continue

        # If the entity is not already added, add it to the graph
        if entity_1 not in entities:
            erd.node(entity_1)
            entities.add(entity_1)

        # If the related entity is not already added, add it to the graph
        if related_entity not in entities:
            erd.node(related_entity)
            entities.add(related_entity)

        # Add an edge between entity and related entity if not already added
        if (entity_1, related_entity) not in connections and entity_1 != related_entity:
            erd.edge(entity_1, related_entity)
            connections.add((entity_1, related_entity))

    degree_count = {}
    for connection in connections:
        source, target = connection
        degree_count[source] = degree_count.get(source, 0) + 1
        degree_count[target] = degree_count.get(target, 0) + 1

    # Update node attributes based on the degree
    for node, degree in degree_count.items():
        color = color_map.get(degree, MAX_COLOR)
        erd.node(node, color=color, style='filled')

    # Render the ERD to a file
    erd.render(view=False, format='svg', engine='fdp')
    erd.render(view=False, format='dot', engine='fdp')

    # Convert the DOT format file to draw.io XML
    drawio_xml = graphviz2drawio.convert(output_filename_gv, layout_prog='fdp')

    # Write the draw.io XML to a file
    with open(output_filename_drawio, 'w') as _file:
        _file.write(drawio_xml)

    # Print the set of entities
    for entity in list(entities):
        print(entity)

    # Print the set of connections
    for c in connections:
        print(c)


# Generate the ERD
generate_erd_without_attributes(_data)

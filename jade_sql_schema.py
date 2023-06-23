import csv
import re

CLEANUP_RE = re.compile(r'[-\s\:\?\/\\)\(\'\+\]\[]')

# Specify the file name
file_name = 'attributes.csv'
OUTPUT_NAME = 'EntityRelationshipDiagram'
output_filename_dot = '.'.join([OUTPUT_NAME, 'gv.dot'])
output_filename_drawio = '.'.join([OUTPUT_NAME, 'drawio'])
output_filename_gv = '.'.join([OUTPUT_NAME, 'gv'])

ADD_ID_PK_TEMPLATE = """
IF EXISTS (SELECT * 
           FROM sys.columns 
           WHERE Name = N'ID' 
           AND Object_ID = Object_ID(N'[dbo].[{0}]'))
BEGIN
    ALTER TABLE [dbo].[{0}]
    DROP COLUMN [ID];
END
BEGIN
ALTER TABLE {0} add ID int identity (1,1) not null;
END
"""

ADD_PK_TEMPLATE = """
IF NOT EXISTS (SELECT * 
               FROM sys.key_constraints 
               WHERE type = 'PK' 
               AND parent_object_id = OBJECT_ID(N'[dbo].[{0}]'))
BEGIN
    ALTER TABLE [dbo].[{0}]
    ADD CONSTRAINT [PK_{0}] PRIMARY KEY ([ID]);
    PRINT 'Primary key constraint PK_{0} has been added.';
END
ELSE
BEGIN
    PRINT 'Primary key constraint PK_{0} already exists on the table.';
END
"""

PK_TEMPLATE = """int identity (1,1) not null primary key"""

FK_TEMPLATE = """
IF NOT EXISTS (SELECT * 
               FROM sys.foreign_keys 
               WHERE object_id = OBJECT_ID(N'[dbo].[{1}]') 
               AND parent_object_id = OBJECT_ID(N'[dbo].[{0}]'))
ALTER TABLE {0}
ADD CONSTRAINT {1}
FOREIGN KEY ({2}) REFERENCES {3}({4});
"""

CREATE_TABLE_TEMPLATE = """
IF NOT EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].{0}') AND type in (N'U'))
BEGIN
CREATE TABLE {0} (\n{1}\n);
END
"""

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


def get_data_type(attr):
    data_type = attr.get('type', None)

    data_type = data_type and data_type.lower()
    _maxlen = attr.get('maxlength', 0)
    ret = None

    if data_type == 'text' or _maxlen > 0:
        ret = 'varchar(%s)' % (_maxlen or 255)
    elif data_type in ['pick list', 'picklist', 'list']:
        ret = 'varchar(255)'
    elif data_type == 'tick box':
        ret = 'bit'
    elif data_type == 'num':
        ret = 'float'
    elif data_type == 'int':
        # We only have primary or foreign keys with this type
        ret = attr['key'] == 'pk' and PK_TEMPLATE or 'int'
    else:
        ret = 'varchar(255)'

    return ret


def get_attribute_def(attr):
    return '\t%s %s' % (
        re.sub(CLEANUP_RE, '_', attr['name']),
        get_data_type(attr)
    )


def generate_sql_schema(data):

    # Keep track of entities and their attributes
    entities = {}
    fks = {}

    # Loop through the data
    for entity_1, attribute, data_type, maxlength, related_entity in data:
        # Add attributes to entities
        try:
            maxlength = int(float(maxlength))
        except:
            maxlength = 0

        entity_1 = re.sub(CLEANUP_RE, '_', entity_1)
        related_entity = re.sub(CLEANUP_RE, '_', related_entity)

        # If the related entity has the same name as the entity, this is an attribute on the entity,
        # otherwise it's on the related entity
        attr = {
            'name': attribute,
            'type': data_type,
            'maxlength': maxlength
        }

        attribute_entity = (entity_1 == related_entity) and entity_1 or related_entity
        if attribute_entity not in entities:
            entities[attribute_entity] = {}
            entities[attribute_entity]['ID'] = {
                'name': 'ID',
                'type': 'int',
                'key': 'pk'
            }
        entities[attribute_entity][attribute] = attr

        # The primary entity needs a foreign key field
        if entity_1 != related_entity:
            if entity_1 not in entities:
                entities[entity_1] = {}

            fk_field = '%s_%s_FK' % (related_entity, entity_1)
            if fk_field not in entities[entity_1]:
                entities[entity_1][fk_field] = {
                    'entity': entity_1,
                    'name': fk_field,
                    'type': 'int',
                    'key': 'fk',
                    'related_entity': related_entity
                }

                # Store FKs for later alter table statements
                fks[fk_field] = entities[entity_1][fk_field];

    # Build the related entities first
    statements = {}

    for ent, attrs in entities.items():
        for attr in attrs.values():
            if attr.get('key', None) == 'fk':
                related_entity = attr.get('related_entity', None)
                if related_entity and related_entity not in statements:
                    related_attrs = entities[related_entity]
                    statements[related_entity] = CREATE_TABLE_TEMPLATE.format(
                        related_entity,
                        ',\n'.join([get_attribute_def(a) for a in related_attrs.values()])
                    )

    # Now the primary entities
    for ent, attrs in entities.items():
        if ent not in statements:
            if 'ID' not in attrs:
                attrs['ID'] = {
                    'name': 'ID',
                    'type': 'int',
                    'key': 'pk'
                }
            statements[ent] = CREATE_TABLE_TEMPLATE.format(
                ent,
                ',\n'.join([get_attribute_def(a) for a in attrs.values()])
            )

    # Add the FK constraints
    for fk, attrs in fks.items():
        statements[fk] = FK_TEMPLATE.format(
            attrs['entity'],
            '%s_constraint' % fk,
            fk,
            attrs['related_entity'],
            'ID'
        )

    # Add primary keys to existing tables
    #pks = []
    #for ent in entities.keys():
    #    pks.append(ADD_PK_TEMPLATE.format(ent))

    # Add primary keys to existing tables
    # id_stmts = []
    # for ent in entities.keys():
    #    id_stmts.append(ADD_ID_PK_TEMPLATE.format(ent))

    # Output
    #for stmt in statements.values():
    #    print(stmt)

    with open('jade_schema.sql', 'w') as _f:
        _f.writelines(statements.values())
        #_f.writelines(id_stmts)
        #_f.writelines(pks)

# Generate the ERD
generate_sql_schema(_data)

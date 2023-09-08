import re
import pandas as pd

# Define the primitive data types
primitive_data_types = ["string", "DateTime", "int", "float", "bool"]

# Paths to the uploaded C# files
file_paths = [
    "datahub_classes/eventhub_course.cs",
    "datahub_classes/eventhub_courseoccurrence.cs",
    "datahub_classes/eventhub_qualification.cs"
]

# Define the regex patterns for properties and json attributes
property_pattern = re.compile(r"public\s+([^\s]+)\s+([^\s]+)\s+{ get; set; }")
json_property_pattern = re.compile(r'\[JsonProperty\("([^"]+)"\)\]')

entities_data = []
non_primitive_tables = []

# Iterate through each file and extract attributes
for file_path in file_paths:
    with open(file_path, 'r') as f:
        content = f.read()

        # Extract properties using regex
        property_matches = property_pattern.findall(content)
        json_property_matches = json_property_pattern.findall(content)

        for i, (data_type, attribute_name) in enumerate(property_matches):
            entity_name = file_path.split("_")[-1].split(".")[0]

            # Check if the attribute is an array type
            is_array = data_type.endswith("[]")
            if is_array:
                data_type = data_type.rstrip("[]")  # Strip the array notation

            # If the data type is not a primitive type or if it's an array type,
            # add it to the non-primitive tables list
            if data_type not in primitive_data_types or is_array:
                non_primitive_tables.append(data_type)
                entities_data.append((entity_name, f"{data_type}ID", "int", True, json_property_matches[i]))
            else:
                entities_data.append((entity_name, attribute_name, data_type, False, json_property_matches[i]))

# Convert the extracted data to a DataFrame for easier processing
df = pd.DataFrame(entities_data, columns=["Entity", "Attribute", "Data Type", "Is Non-Primitive", "JSON Property"])

# Generate the SQL schema based on the DataFrame
sql_statements = []

# Create tables for non-primitive data types
for table in set(non_primitive_tables):
    sql_statements.append("CREATE TABLE {} (\n    {}ID INT PRIMARY KEY\n);".format(table, table))

# Create tables for main entities
for entity in df["Entity"].unique():
    entity_df = df[df["Entity"] == entity]
    columns = []
    for _, row in entity_df.iterrows():
        if row["Is Non-Primitive"]:
            columns.append("    {} INT REFERENCES {}({}ID)".format(row['Attribute'], row['Attribute'].rstrip('ID'),
                                                                   row['Attribute'].rstrip('ID')))
        else:
            sql_data_type = {
                "string": "VARCHAR(255)",
                "DateTime": "DATETIME",
                "int": "INT",
                "float": "FLOAT",
                "bool": "BIT"
            }.get(row["Data Type"], row["Data Type"])
            columns.append("    {} {}".format(row['Attribute'], sql_data_type))
    sql_statements.append("CREATE TABLE {} (\n{}\n);".format(entity, ',\n'.join(columns)))

# Combine all SQL statements
sql_schema = "\n\n".join(sql_statements)

# Write the SQL schema to a file
with open("datahub_curriculum_schema.sql", "w") as f:
    f.write(sql_schema)


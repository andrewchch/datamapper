import csv


def get_record_with_longest_field(filename):
    # Open the CSV file for reading
    with open(filename, 'r') as f:
        # Create a CSV reader object with the "|" delimiter
        reader = csv.reader(f, delimiter='|')

        # Read the headers from the CSV file
        headers = next(reader)

        # Initialize lists to store the maximum lengths and the records with the longest fields
        max_lengths = [0] * len(headers)
        records_with_longest_fields = [None] * len(headers)

        # Iterate over each row in the CSV file
        for row in reader:
            # For each field in the current row, compare its length with the current maximum
            for i, field in enumerate(row):
                # Update the maximum length and record for the current field, if necessary
                if len(field) > max_lengths[i]:
                    max_lengths[i] = len(field)
                    records_with_longest_fields[i] = row

        # Print out the records with the longest fields, prefixed by the field header
        for i, record in enumerate(records_with_longest_fields):
            if record:
                print(f"Field: {headers[i]}, max length: {max_lengths[i]}")
                print("|".join(record))
                print("-" * 50)


# Example usage
filename = "data\\Jade Course Outcomes data export 6.6.23\\outcome groups.csv"
print(get_record_with_longest_field(filename))

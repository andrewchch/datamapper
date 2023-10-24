import re
from datetime import datetime


def parse_fixed_fields_input(s):
    """
    Test:

    s = "2288.375452:CPSN: GENERIC UNDERGRAD:1/01/1873:31/12/2017"
    fixed_fields_parsed = parse_fixed_fields_input(s)
    print(fixed_fields_parsed)
    """
    # Split the string using ":" delimiter
    parts = s.split(':')

    # List to store parsed fields in order
    parsed_fields = []

    # Regex patterns for identifying decimals and dates
    decimal_pattern = r'^-?\d+(\.\d+)?$'
    date_pattern = r'^\d{1,2}/\d{1,2}/\d{4}$'

    for part in parts:
        part = part.strip()
        # Check if part is a decimal
        if re.match(decimal_pattern, part):
            parsed_fields.append(float(part))
        # Check if part is a date
        elif re.match(date_pattern, part):
            parsed_fields.append(datetime.strptime(part, '%d/%m/%Y').date())
        # Otherwise, it's a string
        else:
            parsed_fields.append(part)

    # If there are more than 4 parsed fields, combine string fields until we have 4 in total
    while len(parsed_fields) > 4:
        for i, field in enumerate(parsed_fields):
            if isinstance(field, str) and i + 1 < len(parsed_fields) and isinstance(parsed_fields[i + 1], str):
                parsed_fields[i] = ':'.join([parsed_fields[i], parsed_fields.pop(i + 1)])
                break

    return parsed_fields


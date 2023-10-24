"""
OID|Outcome groups_OID|Outcome groups_Code|Outcome groups_Valid from|Outcome groups_Valid to
OID_2522.2|OID_2288.375452|CPSN:GENERIC UNDERGRAD|1873-01-01|2017-12-31
OID_2522.2|OID_2288.78694|COMP:ALL COURSES|1980-01-01|
OID_2522.2|OID_2288.386684|MJ:AFIS|1980-01-01|2017-12-31
OID_2522.2|OID_2288.387251|CMP:SCHEDULE BCOM|1980-01-01|2017-12-31
"""

import re

# Define the regex pattern
pattern = r"^OID_\d+(\.\d+)?\|OID_\d+(\.\d+)?\|[^|]+\|\d{4}-\d{2}-\d{2}\|(\d{4}-\d{2}-\d{2})?$"
count = 0

with open('data\\Jade Course Outcomes data export 6.6.23\\outcome groups.csv', 'r') as f:
    while True:
        line = f.readline()
        count += 1
        if count % 1000 == 0:
            print('%s lines processed' % count)
        if not line:
            break
        matches = re.match(pattern, line)
        if matches is None:
            print(line)

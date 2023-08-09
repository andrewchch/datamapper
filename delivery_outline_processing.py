import csv
import argparse
import pandas as pd

from nltk.tokenize import sent_tokenize

# Get args
parser = argparse.ArgumentParser(description="Get unique delivery outline sentences")
parser.add_argument('filename', type=str, help='The name of the file to process.')

args = parser.parse_args()
src = args.filename

# Initialize an empty list to store the tuples
outlines = []
sentences = []

# Open the file
with open(src, 'r', encoding='utf-8') as file:
    # Create a csv reader specifying the delimiter as '|'
    reader = csv.reader(file, delimiter=',')
    next(reader)

    for row in reader:
        # Convert the row to a tuple and append it to the list
        if len(row) > 1 and len(row[1]) > 3:
            outlines.append(row[1])

        for sentence in sent_tokenize(row[1]):
            sentences.append(sentence)

print(len(outlines))
print(len(sentences))

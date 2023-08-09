import sys
import pandas as pd
import os
import argparse


# Get command args
def main():
    # Get args
    parser = argparse.ArgumentParser(description="Redact the contents of a file using a substitution list.")
    parser.add_argument('substitutions', type=str, help='The name of the file to fetch substitutions from.')

    args = parser.parse_args()
    subs_file = args.substitutions

    # Load the substitution list
    df = pd.read_excel(subs_file, index_col=0)
    substitutions = df.transpose().to_dict()

    # Invert the substitutions dictionary so that the key is the substitution value and the value is the key
    substitutions = {substitutions[key]['substitute']: key for key in substitutions if not pd.isna(substitutions[key]['substitute'])}

    # Get the content
    with sys.stdin as f:
        content = f.read()

    # For each key in substitutions, replace occurrences of the key with the substitution value in the content variable
    for key in substitutions:
        content = content.replace(key, substitutions[key])

    # Write the unredacted content to stdout
    with sys.stdout as f:
        f.write(content)


if __name__ == "__main__":
    main()





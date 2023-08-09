"""
Aim is to get some context from a file and redact it using a list of substitutions. This can then be passed through to
an LLM for summarising without compromising security of the information.
"""
import sys
import pandas as pd
import os
import PyPDF2
import argparse

from docx import Document

def extract_text(file_path):
    _, file_extension = os.path.splitext(file_path)
    text = ''

    if file_extension == '.docx':
        document = Document(file_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + '\n'

    elif file_extension == '.pdf':
        pdfFileObj = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdfFileObj)

        # Read and concatenate text from each page
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + '\n'
        pdfFileObj.close()

    else:
        print('Unsupported file type')

    return text


# Get command args
def main():
    # Get args
    parser = argparse.ArgumentParser(description="Redact the contents of a file using a substitution list.")
    parser.add_argument('filename', type=str, help='The name of the file to process.')
    parser.add_argument('substitutions', type=str, help='The name of the file to fetch substitutions from.')

    args = parser.parse_args()
    src = args.filename
    subs_file = args.substitutions

    # Load the substitution list
    df = pd.read_excel(subs_file, index_col=0)
    substitutions = df.transpose().to_dict()

    # Get the content
    content = extract_text(src)

    # Order the substitutions by length of the key, so we don't replace a substring of a longer key
    substitutions = {k: substitutions[k] for k in sorted(substitutions, key=len, reverse=True)}

    # For each key in substitutions, replace occurrences of the key with the substitution value in the content variable
    for key in substitutions:
        repl = substitutions[key]['substitute']
        if not pd.isna(repl) and len(repl) > 0:
            content = content.replace(key, substitutions[key]['substitute'])

    # Write the redacted content to stdout
    with sys.stdout as f:
        f.write(content)


if __name__ == "__main__":
    main()





import nltk
import re
import spacy
import random
import string
import pandas as pd

from collections import defaultdict
from tqdm import tqdm
from nltk.tokenize import sent_tokenize

import os
from docx import Document
import PyPDF2


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


def count_words(_sentence):
    # Regular expression pattern for matching words
    word_pattern = re.compile(r"\b[\w'-]+\b")
    # Find all words in the sentence
    words = word_pattern.findall(_sentence)
    # Return the count of words
    return len(words)


# Function to extract (subject, predicate, object) tuples
def extract_spo(_sentence):
    # Parse the sentence
    doc = nlp(_sentence)

    # Initialize subject, predicate and object
    subject = ""
    predicate = ""
    obj = ""

    # Extract subject, predicate, and object
    for token in doc:
        if "subj" in token.dep_:
            subject += token.text + " "
        if "obj" in token.dep_:
            obj += token.text + " "
        if "VERB" == token.pos_:
            predicate += token.text + " "

    # Return the tuple (subject, predicate, object)
    return subject.strip(), predicate.strip(), obj.strip()


# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Download the Punkt tokenizer used for sentence splitting
nltk.download("punkt")

# Get the content
content = extract_text('data\\Fees.docx')

sentences = sent_tokenize(content)

# Check and output grammatically correct sentences
char_count = 0
word_count = 0
valid_sentences = []

for sentence in tqdm(sentences, desc="Processing sentences", unit="sentence"):
    # We're ignoring any sentences with less than 3 words.
    wc = count_words(sentence)
    if wc <= 6:
        continue

    # Extract (subject, predicate, object) tuples
    spo_tuple = extract_spo(sentence)

    # valid_sentences.append((wc, sentence.replace('\n', ' '), spo_tuple))
    word_count += wc
    char_count += len(sentence)

    valid_sentences.append((wc, sentence.replace('\n', ' ')))

print('Words: %s' % word_count)
print('Characters: %s' % char_count)

# Analyze syntax
doc = nlp(content)
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
entities = defaultdict(dict)

for entity in doc.ents:
    entities[entity.text] = {'label': entity.label_, 'substitute': ''}

for entity_name in sorted(list(entities.keys()), key=str.lower):
    entity = entities[entity_name]
    entities[entity_name]['substitute'] = ''.join(random.choices(string.ascii_uppercase, k=4))
    if entity['label'] in ('ORG', 'PERSON', 'GPE'):
        print(entity_name, entity['label'])

# Export the list of entities to Excel, so we can quickly add mappings for them
df = pd.DataFrame(entities)
df = df.transpose()
df.to_excel('redacted_entities.xlsx', index=True)






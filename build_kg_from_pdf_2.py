import spacy
from docx import Document
from nltk.tokenize import sent_tokenize

def read_docx(file_path):
    document = Document(file_path)
    result = ''

    for paragraph in document.paragraphs:
        result += paragraph.text + '\n'

    return result

# specify the path to your .docx file
file_path = "data\\Fees.docx"

content = read_docx(file_path)
print(content)

# Load the English language model
nlp = spacy.load("en_core_web_sm")

sentences = sent_tokenize(content)

# Analyze syntax
doc = nlp(content)
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)




import PyPDF2
import nltk
import language_tool_python
import re
import spacy

from tqdm import tqdm
from nltk.tokenize import sent_tokenize


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

# Initialize the language tool for English
tool = language_tool_python.LanguageTool('en-US')

# Download the Punkt tokenizer used for sentence splitting
nltk.download("punkt")

# Open the PDF file
with open('Att13+GITF+CMS_Manual.pdf', 'rb') as file:

    # Create a PDF file reader
    pdf_reader = PyPDF2.PdfReader(file)

    # Read and concatenate text from each page
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    # Split text into sentences
    sentences = sent_tokenize(text)

# Check and output grammatically correct sentences
char_count = 0
word_count = 0
valid_sentences = []

for sentence in tqdm(sentences, desc="Processing sentences", unit="sentence"):
    # We're ignoring any sentences with less than 3 words.
    wc = count_words(sentence)
    # if wc <= 6:
    #    continue

    # Check for grammar errors in the sentence
    matches = tool.check(sentence)

    """
    # If there are no grammar errors, print the sentence
    if not matches:
        word_count += wc
        char_count += len(sentence)

        # Extract (subject, predicate, object) tuples
        spo_tuple = extract_spo(sentence)
    """

    # valid_sentences.append((wc, sentence.replace('\n', ' '), spo_tuple))
    word_count += wc
    char_count += len(sentence)

    valid_sentences.append((wc, sentence.replace('\n', ' ')))

print('Words: %s' % word_count)
print('Characters: %s' % char_count)

"""
sorted_list = sorted(valid_sentences, key=lambda x: x[0])

# Print the sorted list
print(sorted_list)
"""

with open('GITF_Manual.txt', 'w') as _out:
    _out.writelines(['%s\n' % s for _wc, s in valid_sentences])




import spacy
import sys


def get_complete_object(_token):
    """
    Given a token, this function returns a complete description of the object
    represented by the token, by traversing the token's dependency tree.
    """
    description = [_token.text]

    # Iterate over the token's children in the dependency tree
    for _child in _token.subtree:
        # If the child is a preposition, we add the preposition and its own children (which will be noun chunks)
        if _child.dep_ in ('prep', 'agent'):
            description.append(_child.text)
            description.extend([grandchild.text for grandchild in _child.children])

    return ' '.join(description)


# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Parse the sentence
doc = nlp("Mary Jones stole a pot of jam from Sam's house and hid it under her skirt")

"""
svg = spacy.displacy.render(doc, style='dep')

output_path = 'data/sentence.svg'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(svg)
"""

# Initialize an empty list to hold the triples
triples = []

# Iterate over the tokens

last_subject = ''  # to keep track of the last seen subject

for token in doc:
    if token.pos_ == 'VERB':
        subjects = []
        objects = []
        for child in token.children:
            if child.dep_ in ('nsubj', 'nsubjpass'):
                named_entity = [ent for ent in doc.ents if child in ent]
                if named_entity:
                    subjects.append(named_entity[0].text)
                else:
                    subjects.append(child.text)
                last_subject = subjects  # update the last seen subject
            elif child.dep_ in ('dobj', 'dative', 'attr', 'pobj'):  # added 'dative' and 'attr' for indirect objects
                objects.append(get_complete_object(child))  # using the function to get complete object description
            elif child.dep_ == 'prep':  # added to handle prepositions that are children of verbs
                for grandchild in child.children:
                    if grandchild.dep_ in ('pobj'):  # prepositions take 'pobj' as their objects
                        objects.append(get_complete_object(grandchild))
        if not subjects:  # if no subject was found for this verb, use the last seen subject
            subjects = last_subject
        if subjects and objects:
            triples.append((subjects, token.text, objects))

print(triples)

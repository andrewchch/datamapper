import textacy

from textacy import extract
from textacy import text_stats as ts

# Create a Spacy doc
text = (
"""
Many years later, as he faced the firing squad, Colonel Aureliano Buendía
was to remember that distant afternoon when his father took him to discover ice.
At that time Macondo was a village of twenty adobe houses, built on the bank
of a river of clear water that ran along a bed of polished stones, which were
white and enormous, like prehistoric eggs. The world was so recent
that many things lacked names, and in order to indicate them it was necessary to point.
"""
 )
doc = textacy.make_spacy_doc(text, lang="en_core_web_sm")

print(doc._.preview)

# Analyse it
print(list(extract.entities(doc, include_types={"PERSON", "LOCATION"})))
print(list(extract.subject_verb_object_triples(doc)))

print(ts.n_words(doc), ts.n_unique_words(doc))
print(ts.diversity.ttr(doc))
print(ts.flesch_kincaid_grade_level(doc))
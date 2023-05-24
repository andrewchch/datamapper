import pandas as pd
from transformers import pipeline

OPENAI_API_KEY = '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'

df = pd.read_csv('dataset.csv')

nlp = pipeline("question-answering")

context = df.to_string()

question = "What is the average age?"

result = nlp(question=question, context=context)

print(f"Answer: {result['answer']}")

from rdflib import Graph
import requests

# Create a new Graph
g = Graph()

# Parse in an RDF file
g.parse("test_proc.rdf")

# Convert the graph to N-Triples format, which is a format GraphDB accepts
data = g.serialize(format='nt')

# Specify the GraphDB repository URL
url = "http://localhost:7200/repositories/your_repository/statements"

# Specify the headers
# GraphDB expects data to be in text/plain when it's N-Triples
headers = {
    'Content-Type': 'text/plain',
}

# Post the data to GraphDB
response = requests.post(url, headers=headers, data=data)

# Print out the response to see if it's successful
print(response.text)

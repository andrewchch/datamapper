import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace, Literal, URIRef, BNode

# Create an RDF Graph
g = Graph()

# Define Namespaces
CMS = Namespace("http://example.org/cms/")
SCHEMA = Namespace("http://schema.org/")

# Add the main structure to the graph
cms = URIRef("http://example.org/cms/CMS")
programs = URIRef("http://example.org/cms/Programs")
courses = URIRef("http://example.org/cms/Courses")
classes = URIRef("http://example.org/cms/Classes")

g.add((cms, SCHEMA.hasPart, programs))
g.add((cms, SCHEMA.hasPart, courses))
g.add((cms, SCHEMA.hasPart, classes))

# Add details about Programs
g.add((programs, SCHEMA.description, Literal("Programs are the top tier and represent a structured sequence of study normally leading to the award of one or more degrees, diplomas or certificates.")))
g.add((programs, SCHEMA.name, Literal("Programs")))

# Add details about Courses
g.add((courses, SCHEMA.description, Literal("Courses represent the middle tier. They represent a subject of scholarly study taught in a connected series of lectures or demonstrations.")))
g.add((courses, SCHEMA.name, Literal("Courses")))

# Add details about Classes
g.add((classes, SCHEMA.description, Literal("Classes are an instance of a Course. A Class is created when a Course is scheduled, and resources are allocated for its delivery.")))
g.add((classes, SCHEMA.name, Literal("Classes")))

# Add subparts of Classes
class_schedule = BNode()
class_summary = BNode()

g.add((classes, SCHEMA.hasPart, class_schedule))
g.add((classes, SCHEMA.hasPart, class_summary))

g.add((class_schedule, SCHEMA.name, Literal("Class Schedule")))
g.add((class_schedule, SCHEMA.description, Literal("The key aspects of a Class associated with its scheduling. This typically includes: the Year and Semester(s) that the Class is to run, the Class number allocated, its Start and End dates, the Classes Census Date, the Last Date to Enrol, whether it is to be run online or on-site.")))

g.add((class_summary, SCHEMA.name, Literal("Class Summary")))
g.add((class_summary, SCHEMA.description, Literal("The detailed week by week schedule of activities; details of the assessment activities; the assigned lecturer and convenor. Class Summaries are usually provided to students at the start of a Class in order to give them an overview of the teaching activities.")))

# Create a directed graph for visualization
vis_graph = nx.DiGraph()

# Extract triples from RDF graph and add to visualization graph
edge_labels = {}
description_labels = {}
for s, p, o in g:
    if isinstance(o, Literal):
        # Add labels and descriptions
        if p == SCHEMA.name:
            vis_graph.add_node(s, label=o)
        if p == SCHEMA.description:
            description_labels[s] = str(o)
    else:
        # For non-literal objects, add nodes and edges
        vis_graph.add_edge(s, o)
        edge_labels[(s, o)] = p.split('/')[-1]  # Use last part of URI as label

# Position the nodes using a layout algorithm
pos = nx.spring_layout(vis_graph)

# Draw the nodes
labels = {node: data.get('label', node.split('/')[-1]) for node, data in vis_graph.nodes(data=True)}
nx.draw(vis_graph, pos, labels=labels, node_size=3000, node_color="skyblue")

# Draw the edges
nx.draw_networkx_edges(vis_graph, pos)

# Draw edge labels
nx.draw_networkx_edge_labels(vis_graph, pos, edge_labels=edge_labels)

# Annotate with description labels
for node, coords in pos.items():
    if node in description_labels:
        plt.annotate(description_labels[node], xy=coords, textcoords='offset points', xytext=(0, -25), ha='center', fontsize=8)

# Display the graph
plt.show()
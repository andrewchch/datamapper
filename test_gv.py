from pygraphviz import AGraph
from graphviz2drawio.models import SvgParser

graph = AGraph('test.dot')

svg_graph = graph.draw(prog='fdp', format="svg")
with open('test.svg', 'wb') as _file:
    _file.write(svg_graph)

nodes, edges = SvgParser(svg_graph).get_nodes_and_edges()

print(nodes)

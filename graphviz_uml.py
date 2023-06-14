from graphviz import Digraph
from graphviz2drawio import graphviz2drawio

uml = Digraph('UMLClassDiagram', node_attr={'shape': 'record', 'style': 'filled', 'fillcolor': 'lightyellow'})

# Define the Person class
person = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD COLSPAN="2" BGCOLOR="lightblue">Person</TD></TR>
        <TR><TD>- name: String</TD></TR>
        <TR><TD>- age: Integer</TD></TR>
        <TR><TD>+ get_name(): String</TD></TR>
        <TR><TD>+ get_age(): Integer</TD></TR>
    </TABLE>
>'''

# Define the Employee class
employee = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD COLSPAN="2" BGCOLOR="lightblue">Employee</TD></TR>
        <TR><TD>- employee_id: Integer</TD></TR>
        <TR><TD>+ get_employee_id(): Integer</TD></TR>
    </TABLE>
>'''

# Add classes to the diagram
uml.node('Person', label=person)
uml.node('Employee', label=employee)

# Add an inheritance relationship (Employee inherits from Person)
uml.edge('Employee', 'Person', label='inherits', dir='back', arrowtail='empty')

# Render the UML diagram to a file
uml.render('UMLClassDiagram.gv', view=True, format='svg')
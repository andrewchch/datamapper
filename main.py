"""
Idea is to build a langchain flow that:

- understands one or more data schema via sample data or an actual ERD (we know chatGPT 4 can build an ERD from a text description of entities,
so it may be able to do the same from some data).

I've tested chatGPT 4 on creating a SQL schema from a set of sample data and it does a really good job of it:
https://sharegpt.com/c/9Sjq9fY
"""


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

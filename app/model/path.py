# Paths are represented as a linked list of nodes with edges connecting them
#
# These nodes and edges can contain any items
class Path():
    # Starts a path with the given artist as the source
    def __init__(self, initial_node_obj):
        self.head = Node(initial_node_obj)
        self.end = self.head

    def add_node(self, new_edge, new_node):
        self.end.next = new_edge
        self.end.next.next = new_node
        self.end = new_node
        

class Node(object):
    def __init__(self, objectToAdd):
        self.val = objectToAdd




        







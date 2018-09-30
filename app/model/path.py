# Paths are represented as a linked list of nodes with edges connecting them
#
# These nodes and edges can contain any items
class Path():

    class Node(object):
        def __init__(self, value):
            self.val = value


    # Starts a path with the given artist as the source
    def __init__(self, initial_node_val):
        self.head = self.Node(initial_node_val)
        self.head.next = None
        self.end = self.head

    def add_edge_with_node(self, new_edge_val, new_node_val):
        self.end.next = self.Node(new_edge_val)
        self.end.next.next = self.Node(new_node_val)
        self.end = self.end.next.next
        self.end.next = None

    def __iter__(self):
        iter_node = self.head
        while iter_node is not None:
            yield iter_node.val
            iter_node = iter_node.next

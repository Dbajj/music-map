# A relationship describes the relation between the start and end nodes
# contained within the object. 
#
# The relationship is defined as FROM start TO end
# eg: A FEATURES B
class Relationship(object):
    def __init__(self, start, end, connection):
        self.start = start
        self.end = end
        self.connection = connection

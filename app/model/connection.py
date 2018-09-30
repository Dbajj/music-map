# A connection describes a way two nodes can be related. 
# It contains a string type, as well as a dictionary of additional keys
# containing extra information about the connection.
class Connection(object):
    def __init__(self, type_desc, extras = None):
        if type(type_desc) not str:
            raise TypeError("type_desc should be string")

        if type(extras) not dict:
            raise TypeError("extras should be dictionary")

        self.type = type_desc
        self.extras = extras

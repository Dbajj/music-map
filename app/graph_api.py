from py2neo import Graph, Node, Relationship, NodeMatcher
import pdb


class GraphAdapter():
    def __init__(self, uri, user, password):
        self._graph = Graph(uri)


    def get_artist_by_id(self,artist_id):
        """ 
        Return artist object from database corresponding to given id
        if no artist found, returns None
        """
        print("WE CALLING NOW")
        matcher = NodeMatcher(self._graph)
        artist = matcher.match(artist_id).first()
        return artist
            #artist_node = result[0]['n']
            #return Artist(artist_node.get('name'), artist_node.get('artistId'))

class Artist():
    def __init__(self, name, artist_id):
        self.name = name
        self.id = artist_id




from py2neo import Graph, Node, Relationship, NodeMatcher
from app.entity.artist import Artist
import pdb



class GraphAdapter():
    def __init__(self, uri, user, password):
        self._graph = Graph(uri,auth=(user,password))
        self._matcher = NodeMatcher(self._graph)


    def get_artist_by_id(self,artist_id: str) -> Artist:
        """get_artist_by_id

        :param artist_id: the artist id to look up
        :type artist_id: str
        :rtype: Artist
        """

        artist = self._matcher.match("Artist",artistId=artist_id).first()

        if artist is None:
            return None
        else:
            return Artist(artist['name'],artist['artistId'])

    # TODO figure out how to parse the returned Record (which contains one path
    # object) into some type of Relationship data structure
    def get_path_by_id(self, artist_id_one: str, artist_id_two: str):
        path_query_string = f"match(source:Artist {{ artistId:" \
            f"\"{artist_id_one}\"}}), (dest:Artist {{ artistId:" \
                f"\"{artist_id_two}\"}})," \
            "p=shortestPath((source)-[*]-(dest)) return p"
        path_cursor = self._graph.run(path_query_string)
        path = path_cursor.evaluate() 

        artist_nodes = []
        relationships_nodes = []

        toggle = True
        for element in path.__walk__():
            if toggle:
                artist_nodes.append(Artist(element.get('name'),element.get('artistId')))
            else:
                relationships_nodes.append(element)
            toggle = not toggle

        # TODO create a wrapper class for relationships, and then create  path
        # object using the generated objects, return that
        return path





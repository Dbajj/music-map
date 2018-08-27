from py2neo import Graph, Node, Relationship, NodeMatcher
from app.entity.artist import Artist
import pdb



class GraphAdapter():
    def __init__(self, uri, user, password):
        self._graph = Graph(uri,auth=(user,password))


    def get_artist_by_id(self,artist_id: int) -> Artist:
        """get_artist_by_id

        :param artist_id: the artist id to look up
        :type artist_id: int
        :rtype: Artist
        """

        matcher = NodeMatcher(self._graph)
        artist = matcher.match("Artist",artistId=artist_id).first()

        if artist is None:
            return None
        else:
            return Artist(artist['name'],artist['artistId'])



from py2neo import Graph, Node, Relationship, NodeMatcher
from app.model.artist import Artist
from app.model.path import Path
import pdb


class GraphRepository():
    def __init__(self, graph_adapter, graph_matcher):
        self._adapter = graph_adapter
        self._matcher = graph_matcher

    def get_artist_by_id(self, artist_id: str) -> Artist:
        """get_artist_by_id

        :param artist_id: the artist id to look up
        :type artist_id: str
        :rtype: Artist
        """

        artist_response = self._matcher.match("Artist", artistId=artist_id)

        if artist_response is None:
            return None
        else:
            return self._adapter.generate_artist(artist_response)

    def get_path_by_id(self, artist_id_one: str, artist_id_two: str) -> Path:
        """get_path_by_id

        returns the shortest path from artist_id_one to artist_id_two

        :type artist_id_one: str
        :type artist_id_two: str
        :rtype: Path
        """

        path_query_string = f"match(source:Artist {{ artistId:" \
            f"\"{artist_id_one}\"}}), (dest:Artist {{ artistId:" \
            f"\"{artist_id_two}\"}})," \
            "p=shortestPath((source)-[*]-(dest)) return p"

        path_response = self._matcher.graph.run(path_query_string)

        # TODO create a wrapper class for relationships, and then create  path
        # object using the generated objects, return that
        return self._adapter.generate_relationship_list(path_response)

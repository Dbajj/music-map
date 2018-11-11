from py2neo import Graph, Node, Relationship, NodeMatcher
from app.model.artist import Artist
from app.model.path import Path
from app.model.release import Release
from app.adapter import GraphAdapter
import pdb


class GraphRepository():
    def __init__(self, graph_adapter: GraphAdapter, graph_matcher: NodeMatcher):
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

    def get_artist_by_name(self, artist_name: str) -> Artist:
        """get_artist_by_name

        :param artist_name: name of the artist to search up
        :type artist_name: str
        :rtype: Artist
        """

        artist_response = self._matcher.match("Artist", name=artist_name)

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

        path_query_string = "match(source:Artist { artistId:" \
            "{artist_id_one} }), (dest:Artist { artistId:" \
            "{artist_id_two} })," \
            "p=shortestPath((source)-[*]-(dest)) return p"

        path_response = self._matcher.graph.run(path_query_string,
                                                artist_id_one=artist_id_one,
                                                artist_id_two=artist_id_two)

        return self._adapter.generate_relationship_list(path_response)

    def get_release_by_id(self, release_id: str) -> Release:
        """get_release_by_id
        
        :param release_id: The id of the release to be retrieved
        :type release_id: str
        :return: The release object represented by release_id
        :rtype: Release
        """
        release_response = self._matcher.match("Release", releaseId=release_id)

        if release_response is None:
            return None
        else:
            return self._adapter.generate_release(release_response)
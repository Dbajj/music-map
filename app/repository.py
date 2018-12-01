from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
from app.model.artist import Artist
from app.model.path import Path
from app.model.release import Release
from app.adapter import GraphAdapter
import pdb


class GraphRepository():
    def __init__(self, graph_adapter: GraphAdapter, node_matcher: NodeMatcher, rel_matcher: RelationshipMatcher):
        self._adapter = graph_adapter
        self._node_matcher = node_matcher
        self._rel_matcher = rel_matcher

    def get_artist_by_id(self, artist_id: str) -> Artist:
        """get_artist_by_id

        :param artist_id: the artist id to look up
        :type artist_id: str
        :rtype: Artist
        """

        artist_response = self._node_matcher.match("Artist", artistId=artist_id)

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

        artist_response = self._node_matcher.match("Artist", name=artist_name)

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

    # Used for auto-complete feature
    def get_artists_by_string(self, querystring: str) -> Artist:
        """get_artists_by_string

        returns the first 5 artists matching the querystring

        :param querystring: the string to match on database search
        :type querystring: str
        :rtype: List of Artist
        """

        artists_response = self._matcher.match("Artist").where("_.name =~ '{querystring}*'").order_by("_.name").limit(5)
        print("REPOSITORY TIME")
        print(artists_response)
        pdb.set_trace()
        if artists_response is None:
            return None
        else:
            #TODO ITERATE THROUGH THE ARTISTS RESPONSE
            #see neo4j docs for iter()
            return self._adapter.generate_artists_list(artists_response)

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

        path_response = self._node_matcher.graph.run(path_query_string,
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
        release_response = self._rel_matcher.match(masterId=release_id)

        if release_response is None:
            return None
        else:
            return self._adapter.generate_release(release_response)
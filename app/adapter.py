from app.model.artist import Artist
from app.model.path import Path
from app.model.relationship import Relationship
from app.model.connection import Connection
from functools import reduce
import py2neo
import pdb


# Purpose of this class is to convert entities obtained from Neo4j API into
# objects that are supported within this service
class GraphAdapter():
    def __init__(self):
        pass

    def generate_artist(self, artist_response) -> Artist:
        if type(artist_response) is py2neo.matching.NodeMatch:
            artist_dict = artist_response.first()
        else:
            artist_dict = artist_response

        if artist_dict is None:
            return None

        return Artist(artist_dict['name'], artist_dict['artistId'])

    # Converts a list of relationships to a linear path from the given source
    # name to the given destination name
    #
    # Assumes relationships are sorted in the desired order
    def relationship_list_to_path(self, rel_list: list, source, dest) -> Path:
        def combine_pair(rsf, second):
            pass
        pass

    # Converts a shortestPath neo4j query response into a list of relationships
    # containing a start node, relation and end node
    def generate_relationship_list(self, path_cursor) -> list:
        neo_path = path_cursor.evaluate()
        pdb.set_trace
        output_list = []

        for element in neo_path.relationships:
            cur_relation = self.generate_relationship(element)
            output_list.append(cur_relation)

        return output_list

    # Converts a neo4j relationship data node into a Relationship object
    def generate_relationship(self, relationship_response) -> Relationship:
        start_node = self.generate_artist(relationship_response.start_node)
        end_node = self.generate_artist(relationship_response.end_node)

        connection_type = list(relationship_response.types())
        connection_extras = dict(zip(relationship_response.keys(),
                                     relationship_response.values()))

        if len(connection_type) != 1:
            raise ValueError("Expected only one connection type from neo4j \
                    relationship response")
        else:
            return Relationship(start_node, end_node,
                                Connection(connection_type[0],
                                           connection_extras))

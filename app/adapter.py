from app.model.artist import Artist
from app.model.path import Path
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
        return Artist(artist_dict['name'], artist_dict['artistId'])

    # Converts a list of relationships to a linear path from the given source
    # name to the given destination name
    def relationship_list_to_path(self, path, source, dest) -> Path:
        pass


    # Converts a shortestPath neo4j query response into a list of relationships
    # containing a start node, relation and end node
    def generate_relationship_list(self, path_cursor) -> list:
        neo_path = path_cursor.evaluate()
        output_list = []

        for element in neo_path.relationships:
            cur_relation = self.generate_relationship(element)
            output_list.append(cur_relation)

        return output_list


    # Converts a neo4j relationship data node into a Relationship object
    def generate_relationship(self, relationship_response):
        pass

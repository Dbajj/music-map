from neo4j.v1 import GraphDatabase
import pdb

class GraphAdapter():
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri)



    def close(self):
        self._driver.close()


    def get_artist_by_id(self,artist_id):
        """ 
        Return artist object from database corresponding to given id
        if no artist found, returns None
        """
            #artist_node = result[0]['n']
            #return Artist(artist_node.get('name'), artist_node.get('artistId'))

class Artist():
    def __init__(self, name, artist_id):
        self.name = name
        self.id = artist_id




from neo4j.v1 import GraphDatabase

class GraphAdapter():
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()


    
    def get_artist_by_id(self,artist_id):
        """ 
        Return artist object from database corresponding to given id
        if no artist found, returns None
        """
        with self._driver.session() as session:
            result = list(session.run(f"MATCH(n:Artist {{artistId: \"{artist_id}\"}}) return(n)"))
            if len(result) == 0:
                return None
            else:
                artist_node = result[0]['n']
                return Artist(artist_node.get('name'), artist_node.get('artistId'))



class Artist():
    def __init__(self, name, artist_id):
        self.name = name
        self.id = artist_id
            



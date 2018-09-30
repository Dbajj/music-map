from app.entity.artist import Artist, Path
import pdb


# Purpose of this class is to convert entities obtained from Neo4j API into
# objects that are supported within this service
class GraphAdapter():
    def __init__(self):
        pass

    def generate_artist(self, artist_response) -> Artist:
        return Artist(artist_response['name'], artist_response['artistId'])

    def generate_path(self, path_cursor) -> Path:
        neo_path = path_cursor.evaluate()
        pdb.set_trace()

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






class Artist():
    def __init__(self, name, artist_id):
        self.name = name
        self.id = artist_id

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id




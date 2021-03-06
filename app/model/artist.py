from flask_restful import fields

class Artist():
    def __init__(self, name, artist_id):
        self.name = name
        self.id = artist_id

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id

    def __str__(self):
        return f"{self.name}"

    fields = {
        'name': fields.String,
        'id': fields.String
    }

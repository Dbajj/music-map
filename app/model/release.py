from app.model.artist import Artist

class Release():
    def __init__(self, id: str, title: str, year: str, author: Artist = None):
        self.id = id
        self.title = title
        self.year = year
        self.author = author

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.id}-{self.title}-{self.year}"
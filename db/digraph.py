from sqlalchemy import Column, Integer, String,ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Node(Base):
    __tablename__ = 'artist'

    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)

    def higher_neighbors(self):
        return [x.higher_node for x in self.lower_edges]

    def lower_neighbors(self):
        return [x.lower_node for x in self.higher_edges]


class Edge(Base):
    __tablename__ = 'edge'

    lower_id = Column(
        Integer,
        ForeignKey('artist.artist_id'),
        primary_key=True)

    higher_id = Column(
        Integer,
        ForeignKey('artist.artist_id'),
        primary_key=True)

    lower_node = relationship(
        Node,
        primaryjoin=lower_id == Node.artist_id,
        backref='lower_edges')

    higher_node = relationship(
        Node,
        primaryjoin=higher_id == Node.artist_id,
        backref='higher_edges')

    def __init__(self, n1, n2):
        self.lower_node = n1
        self.higher_node = n2


engine = create_engine('postgresql://dbajj:muna00@localhost/music_sep')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

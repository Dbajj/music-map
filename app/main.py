from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from app.adapter import GraphAdapter
from configparser import SafeConfigParser
from py2neo import Graph, NodeMatcher, RelationshipMatcher
from app.repository import GraphRepository
from app.model.artist import Artist
from app.model.release import Release
from json import JSONEncoder
from flask_cors import CORS
import os
import pdb

GRAPH_URI = "bolt://104.248.220.9:7687"

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
# Allow POST requests with JSON
app.config['CORS_HEADERS'] = 'Content-Type'

config = SafeConfigParser()
assert os.path.exists(os.getcwd() + '/conf/settings.cfg')
config.read(os.getcwd() + '/conf/settings.cfg')

graph_adapter = GraphAdapter()
graph_dao = Graph(GRAPH_URI,
                  auth=(config.get('neo4j', 'username'),
                        (config.get('neo4j', 'password'))))
graph_repository = GraphRepository(graph_adapter,
                                   NodeMatcher(graph_dao),
                                   RelationshipMatcher(graph_dao))

class PathEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


app.json_encoder = PathEncoder


class ArtistIdApi(Resource):
    @marshal_with(Artist.fields)
    def get(self, artist_id):
        result = graph_repository.get_artist_by_id(str(artist_id))
        if result is None:
            abort(404, message="Artist id {} doesn't exist".format(artist_id))
        else:
            return result

class ArtistNameApi(Resource):
    @marshal_with(Artist.fields)
    def get(self, artist_name):
        result = graph_repository.get_artist_by_name(artist_name)
        if result is None:
            abort(404, message="Artist name {} doesn't \
                    exist".format(artist_name))
        else:
            return result

class PathApi(Resource):
    def get(self):
        artist_id_one = request.args['artist_id_one']
        artist_id_two = request.args['artist_id_two']

        output = graph_repository.get_path_by_id(artist_id_one, artist_id_two)

        return jsonify(output)

class ReleaseApi(Resource):
    @marshal_with(Release.fields)
    def get(self, release_id: int):
        result = graph_repository.get_release_by_id(str(release_id))
        if result is None:
            abort(404, message="Release id {} doesn't \
                    exist".format(release_id))
        else:
            return result

api.add_resource(ArtistIdApi, '/artist/<int:artist_id>')
api.add_resource(ArtistNameApi, '/artist/<string:artist_name>')
api.add_resource(PathApi, '/path')
api.add_resource(ReleaseApi, '/release/<int:release_id>')


if __name__ == '__main__':
    app.run(debug=True)

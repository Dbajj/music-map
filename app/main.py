
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from app.adapter import GraphAdapter
import pdb

GRAPH_URI = "bolt://127.0.0.1:7687"

app = Flask(__name__)
api = Api(app)

graph_adapter = GraphAdapter(GRAPH_URI,"neo4j","***REMOVED***")

resource_fields = {
    'name': fields.String,
    'id': fields.String
}


class ArtistApi(Resource):
    @marshal_with(resource_fields)
    def get(self, artist_id):
        result = graph_adapter.get_artist_by_id(artist_id);
        if result is None:
            abort(404, message="Artist id {} doesn't exist".format(artist_id))
        else:
            return result

class PathApi(Resource):
    # TODO Figure out how to parse the returned Relationship structure into
    # some sort of json response
    def get(self):
        artist_id_one = request.args['artist_id_one']  
        artist_id_two = request.args['artist_id_two']
        pdb.set_trace()
        result = graph_adapter.get_path_by_id(artist_id_one,artist_id_two)



api.add_resource(ArtistApi,'/artist/<string:artist_id>')
api.add_resource(PathApi,'/path/')


if __name__ == '__main__':
    app.run(debug=True)

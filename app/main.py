
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from neo4j.v1 import GraphDatabase

GRAPH_URI = "bolt://127.0.0.1:7687"

app = Flask(__name__)
api = Api(app)

graph_driver = GraphDatabase.driver(GRAPH_URI, auth=("neo4j", "***REMOVED***"))

class Node(Resource):
    def get(self, node_id):
        with graph_driver.session() as session:
            return session.run("MATCH(n:Artist {})")

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)

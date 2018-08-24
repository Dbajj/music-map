import pdb
import pytest
from app import graph_api
import docker
import os
import time
import csv
from py2neo import Node, Relationship, NodeMatcher

TEST_URI = "bolt://127.0.0.1:7688"
TESTFILE_URI_NODE = "data/test_csv/test_artist_simple.csv"
TESTFILE_URI_RELATION = "data/test_csv/test_release_simple.csv"
SECOND = 1000000000
CHECKTIMEOUT = 1


@pytest.fixture
def test_api():
    working_dir = os.getcwd()
    client = docker.from_env()
    container = None

    try:
        container = client.containers.get("neo4j_test")
        if (container.status == 'exited'):
            container.start()
    except:
        client.containers.run("neo4j:3.0",
                ports={'7474/tcp':7478, '7687/tcp':7688},
                volumes={f"{working_dir}/neo4j-test/data" : {'bind': '/data', 'mode': 'rw' },
                    f'{working_dir}/neo4j-test/logs': {'bind': '/logs', 'mode': 'rw'}}, 
                detach=True,
                environment = ["NEO4J_AUTH=none"],
                name="neo4j_test",
                healthcheck = {"test": "curl --fail http://127.0.0.1:7474 || exit 1",
                    "interval": 5*SECOND,
                    "timeout": 5*SECOND,
                    "retries": 5},
                )
        container = client.containers.get("neo4j_test")


    while(container.attrs['State']['Health']['Status'] != 'healthy'):
        time.sleep(CHECKTIMEOUT)
        container = client.containers.get("neo4j_test")


    api = graph_api.GraphAdapter(TEST_URI, "neo4j", "***REMOVED***")
    load_test_nodes(api, TESTFILE_URI_NODE)
    load_test_relations(api, TESTFILE_URI_RELATION)
    yield api
    clear_nodes(api)
    

def load_test_nodes(api, uri):
    working_dir = os.getcwd()
    with open(f'{working_dir}/{TESTFILE_URI_NODE}', 'r') as csvfile:
        reader = csv.reader(csvfile)
        graph = api._graph
        tx = graph.begin()
        for entry in reader:
            tx.create(Node("Artist",artistId=entry[0],name=entry[1]))
        tx.commit()

def load_test_relations(api, uri):
    working_dir = os.getcwd()
    with open(f'{working_dir}/{TESTFILE_URI_RELATION}', 'r') as csvfile:
        reader = csv.reader(csvfile) 
        graph = api._graph
        tx = graph.begin()
        matcher = NodeMatcher(graph)
        for entry in reader:
            first = matcher.match(artistId=entry[1]).first()
            second = matcher.match(artistId=entry[2]).first()
            tx.create(Relationship(first,entry[3],second,masterId=entry[0]))
        tx.commit()


    

        

def clear_nodes(api):
    api._graph.run("MATCH(n) DETACH DELETE n")




def test_get_artist_by_id(test_api):
    test_api.get_artist_by_id("123451")



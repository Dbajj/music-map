import pdb
import pytest
from app import graph_api
import docker
import os
import time

TEST_URI = "bolt://127.0.0.1:7688"
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
    yield api
    api.close()
    container.kill()
    

def test_get_artist_by_id(test_api):
    test_api.get_artist_by_id("123451")



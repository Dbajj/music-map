import unittest
import pdb
from app import graph_api

TEST_URI = "bolt://127.0.0.1:7687"
TEST_USER = "neo4j"
TEST_PASSWORD = "***REMOVED***"

class TestGraphApi(unittest.TestCase):
    
    def test_get_artist_by_id(self):
        test_instance = graph_api.GraphAdapter(TEST_URI, TEST_USER, TEST_PASSWORD)
        test_instance.close()

    
if __name__ == '__main__':
    unittest.main()


import pytest
from unittest.mock import MagicMock 
from app.model.path import Path
import pdb

class TestPath(object):
    def test_path_constructor(self, mocker):
        test_obj = "Test Value"
        test_path = Path(test_obj)

        assert test_path.head.val == test_obj
        assert test_path.end.val == test_obj

    def test_path_iterator(self, mocker):
        test_objs = ["O1", "E1", "O2", "E2", "O3", "E3", "O4"]
        test_path = Path(test_objs[0])

        for i in range(1,len(test_objs) - 1,2):
            print(i)
            test_path.add_edge_with_node(test_objs[i], test_objs[i+1])

        i = 0
        for value in test_path:
            assert value == test_objs[i]
            i += 1

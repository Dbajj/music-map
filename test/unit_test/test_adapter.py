import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from pytest_mock import mocker
from py2neo import NodeMatch, Node
import pdb
import app

#
#@patch('app.graph_api.Graph')
#@patch('app.graph_api.NodeMatcher')
#def test_get_artist_by_id_not_present(matcher_mock, init_mock):
#    matcher_mock.return_value.match.return_value.first.return_value = None
#
#    api = app.graph_api.GraphAdapter(None,None,None)
#    result = api.get_artist_by_id("123412")
#
#    assert result is None
#    matcher_mock.return_value.match.assert_called_with("123412")
#

class TestGraphAdapter(object):

    def test_get_artist_by_id_not_present(self,mocker):
        mocker.patch('app.adapter.Graph')
        mocker.patch('app.adapter.NodeMatcher')
        app.adapter.NodeMatcher.return_value.match.return_value.first.return_value = None


        api = app.adapter.GraphAdapter(None,None,None)
        result = api.get_artist_by_id('123412')

        assert result is None
        app.adapter.NodeMatcher.return_value.match.assert_called_with('Artist',artistId="123412")

    def test_get_artist_by_id_present(self,mocker):
        mocker.patch('app.adapter.Graph')
        mocker.patch('app.adapter.NodeMatcher')
        app.adapter.NodeMatcher.return_value.match.return_value.first.return_value\
                = Node("Artist",name="Eminem",artistId="123412")

        api = app.adapter.GraphAdapter(None,None,None)
        result = api.get_artist_by_id('123412')

        assert result == app.adapter.Artist("Eminem",'123412')
        app.adapter.NodeMatcher.return_value.match.assert_called_with('Artist',artistId="123412")

    # TODO Complete this with appropriate return type from py2neo and appropriate
    # asserts
    def test_get_path_by_id_present(self,mocker):
        mocker.patch('app.adapter.Graph')
        cursor_mock = MagicMock()
        path_mock = MagicMock()
        app.adapter.Graph.return_value.run.return_value = cursor_mock
        cursor_mock.evaluate.return_value = path_mock

        
        
        pdb.set_trace()
        api = app.adapter.GraphAdapter(None,None,None)
        result = api.get_path_by_id("123412","128341")




import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from pytest_mock import mocker
from py2neo import NodeMatch
import pdb
import app


@patch('app.graph_api.Graph')
@patch('app.graph_api.NodeMatcher')
def test_get_artist_by_id_not_present(matcher_mock, init_mock):
    matcher_mock.return_value.match.return_value.first.return_value = None

    api = app.graph_api.GraphAdapter(None,None,None)
    result = api.get_artist_by_id("123412")

    assert result is None
    matcher_mock.return_value.match.assert_called_with("123412")


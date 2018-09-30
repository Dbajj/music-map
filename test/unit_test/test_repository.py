import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from app.model.artist import Artist
from app.repository import GraphRepository
import pdb


class TestGraphRepository(object):

    def test_get_artist_by_id_present(self, mocker):
        adapter_mock = MagicMock()
        matcher_mock = MagicMock()
        repo = GraphRepository(adapter_mock, matcher_mock)

        sample_id = "122455"
        sample_name = "Eminem"

        matcher_return = MagicMock()
        matcher_return.first.return_value = {
            'name': f'{sample_name}', 'artistId': f'{sample_id}'}

        matcher_mock.match.return_value = matcher_return
        adapter_mock.generate_artist.return_value = Artist(f'{sample_name}',
                                                           f'{sample_id}')
        val = repo.get_artist_by_id(sample_id)

        adapter_mock.generate_artist.assert_called_with(matcher_return)
        matcher_mock.match.assert_called_with("Artist", artistId=sample_id)

        assert val == adapter_mock.generate_artist.return_value

    def test_get_artist_by_id_not_present(self, mocker):
        adapter_mock = MagicMock()
        matcher_mock = MagicMock()
        repo = GraphRepository(adapter_mock, matcher_mock)

        sample_id = "122455"

        matcher_mock.match.return_value = None

        val = repo.get_artist_by_id(sample_id)

        adapter_mock.generate_artist.assert_not_called()
        matcher_mock.match.assert_called_with("Artist", artistId=sample_id)

        assert val is None


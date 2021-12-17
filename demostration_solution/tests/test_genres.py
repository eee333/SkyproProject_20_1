from unittest.mock import MagicMock
import pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture
def genre_dao():
    genre_dao = GenreDAO(None)
    genre1 = Genre(
        id=1,
        name="Genre1"
    )
    genre2 = Genre(
        id=2,
        name="Genre2"
    )
    genre3 = Genre(
        id=3,
        name="Genre3"
    )
    dict_objects = {1:genre1, 2: genre2, 3: genre3}
    genre_dao.get_one = MagicMock(side_effect=dict_objects.get)
    genre_dao.get_all = MagicMock(return_value=[genre1, genre2, genre3])
    genre_dao.create = MagicMock(return_value=Genre(id=4, name="Genre4"))
    genre_dao.delete = MagicMock(side_effect=dict_objects.pop)
    genre_dao.update = MagicMock()
    genre_dao.partially_update = MagicMock()
    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre.id != None

    def test_get_one_out(self):
        genre = self.genre_service.get_one(100)
        assert genre == None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        genre_d = {
            "name": "Genre4"
        }
        genre = self.genre_service.create(genre_d)
        assert genre.id != None

    def test_delete(self):
        self.genre_service.delete(1)
        genre = self.genre_service.get_one(1)
        assert genre == None

    def test_update(self):
        genre_d = {
            "id": 2,
            "name": "Genre2_upd"
        }
        self.genre_service.update(genre_d)

    def test_partially_update(self):
        genre_d = {
            "id": 3,
            "name": "Genre3_upd"
        }
        self.genre_service.partially_update(genre_d)




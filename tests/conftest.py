import pytest
from page_analyzer import app


@pytest.fixture()
def test_app():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testsekretkey'
    app.config['DATABASE_URL'] = 'test_database_url'

    yield app


@pytest.fixture()
def client(test_app):
    return app.test_client()

from unittest import mock
from datetime import date


def test_post_urls_incorrect_url(client):

    # Incorrect URL
    response = client.post('/urls', data={
        'url': "google.com",
    }, follow_redirects=True)
    flash_messages = 'Некорректный URL'.encode("utf-8", "ignore")
    assert flash_messages in response.data


def test_add_existing_url(client, test_app):
    with mock.patch('psycopg2.connect') as mock_connect:
        today = date.today
        expected = ('1', 'https://google.com', today)

        mock_con_cm = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_con = mock_con_cm.__enter__.return_value  # object assigned to con in with ... as con
        mock_cur_cm = mock_con.cursor.return_value  # resultof con.cursor(cursor_factory=DictCursor)
        mock_cur = mock_cur_cm.__enter__.return_value  # object assigned to cur in with ... as cur

        mock_cur.fetchone.return_value = expected

        response = client.post('/urls', data={
            'url': 'https://google.com'
        }, follow_redirects=True)

        mock_connect.assert_called_with(test_app.config['DATABASE_URL'])
        mock_cur.execute('SELECT id FROM urls WHERE name = %s',
                         ('https://google.com',))

        flash_messages = 'Страница уже существует'.encode("utf-8", "ignore")
        assert flash_messages in response.data


def test_add_new_url(client, test_app):
    with mock.patch('psycopg2.connect') as mock_connect:
        today = date.today

        mock_con_cm = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_con = mock_con_cm.__enter__.return_value  # object assigned to con in with ... as con
        mock_cur_cm = mock_con.cursor.return_value  # resultof con.cursor(cursor_factory=DictCursor)
        mock_cur = mock_cur_cm.__enter__.return_value  # object assigned to cur in with ... as cur

        # mock_cur.fetchone.return_value
        mock_cur.fetchone.return_value = ('1', 'test_data', today)
        # ('1', 'for_test', today)]
        response = client.post('/urls', data={
            'url': 'https://google.com'
        }, follow_redirects=True)

        mock_connect.assert_called_with(test_app.config['DATABASE_URL'])
        mock_cur.execute("INSERT INTO urls (name, created_at) "
                         "VALUES (%s, %s) RETURNING id",
                         ('https://google.com', "01-01-2023"))

        flash_messages = 'Страница успешно добавлена'.encode("utf-8", "ignore")
        assert flash_messages in response.data

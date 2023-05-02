def test_request_example(client):
    response = client.get("/")
    data_h1 = '<h1 class="display-3">Анализатор страниц</h1>'.encode('utf-8', 'ignore')
    data_p = (
        '<p class="lead">Бесплатно проверяйте сайты на SEO пригодность</p>'
    ).encode('utf-8', 'ignore')
    assert data_h1 in response.data
    assert data_p in response.data
    assert b'href="https://ru.hexlet.io/"' in response.data

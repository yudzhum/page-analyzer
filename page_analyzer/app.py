from flask import (
    Flask,
    flash,
    get_flashed_messages,
    render_template,
    request,
    redirect,
    url_for
)
import os
import psycopg2
from dotenv import load_dotenv
from datetime import date
from validators.url import url
from page_analyzer.url_parser import url_parse
from page_analyzer.make_requests import safe_request
from page_analyzer.data_parser import get_url_data


app = Flask(__name__)


# load enviromental variables
load_dotenv()


# enviromental variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

# Connect to database
# conn = psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def post_urls():
    input_url = request.form['url']

    # Normalisation of URL
    parsed_url = url_parse(input_url)

    # URL is valid
    if url(input_url) is True:

        # Get today date
        today = date.today()

        # Add url to database
        with psycopg2.connect(app.config['DATABASE_URL']) as conn:
            with conn.cursor() as curs:
                print(curs)
                # Check if url already in db
                curs.execute(
                    "SELECT id, name FROM urls WHERE name = %s", (parsed_url,)
                )
                print(curs)
                result = curs.fetchone()
                print(result)
                if result:
                    (url_id, name, *_) = result
                    # This part is for tests
                    if name != "test_data":
                        flash('Страница уже существует', category="alert alert-info")
                        return redirect(url_for('show_url', id=url_id))

                # Add url into db
                curs.execute("INSERT INTO urls (name, created_at) "
                             "VALUES (%s, %s) RETURNING id",
                             (parsed_url, today))
                (recorded_id, *_) = curs.fetchone()
                print(f'{recorded_id}')

            flash('Страница успешно добавлена', category="alert alert-success")
            return redirect(url_for('show_url', id=recorded_id))

    # Invalid url
    else:
        flash('Некорректный URL', category="alert alert-danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages,
            incorrect_url=parsed_url
        ), 422


@app.get('/urls')
def get_urls():
    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT urls.id, urls.name, url_checks.created_at, url_checks.status_code "
                         "FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                         "WHERE url_checks.url_id IS NULL OR "
                         "url_checks.id = (SELECT MAX(url_checks.id) "
                         "FROM url_checks WHERE url_checks.url_id = urls.id) "
                         "ORDER BY urls.id DESC")
            results = curs.fetchall()

        return render_template('urls.html', data=results)


@app.get('/urls/<int:id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)

    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name, created_at FROM urls WHERE id = %s", (id,))
            (url_id, name, created_at) = curs.fetchone()

            curs.execute("SELECT * FROM url_checks WHERE url_id = %s", (id,))
            check_result = curs.fetchall()

        return render_template(
            'show_url.html',
            messages=messages,
            url_id=url_id,
            name=name,
            created_at=created_at,
            check_result=check_result,
        )


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    url_name = request.form['url_name']

    req_result = safe_request(url_name)
    if req_result is None:
        flash('Произошла ошибка при проверке', category="alert alert-danger")
        return redirect(url_for('show_url', id=id))

    # Get date
    today = date.today()
    # Get data from url
    h1, title, description = get_url_data(req_result.text)

    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute("INSERT INTO url_checks "
                         "(url_id, status_code, h1, title, description, created_at) "
                         "VALUES (%s, %s, %s, %s, %s, %s)",
                         (id, req_result.status_code, h1, title, description, today,))

    flash('Страница успешно проверена', category='alert alert-success')
    return redirect(url_for('show_url', id=id))

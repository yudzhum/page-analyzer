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


app = Flask(__name__)


# load enviromental variables
load_dotenv()


# enviromental variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Connect to database
conn = psycopg2.connect(DATABASE_URL)


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
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as curs:
            # Check if url already in db
                curs.execute("SELECT id FROM urls WHERE name = %s", (parsed_url,))
                result = curs.fetchone()
                if result:
                    flash('Адрес уже добавлен', category="alert alert-info")
                    (url_id, *_) = result
                    return redirect(url_for('show_url', id=url_id))

                # Add url into db
                curs.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id", (parsed_url, today))
                (recorded_id, *_) = curs.fetchone()

            flash('Страница успешно добавлена', category="alert alert-success")
            return redirect(url_for('show_url', id=recorded_id))

    #Invalid url
    else:
        flash('Некорректный URL', category="alert alert-danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages, incorrect_url=parsed_url)


@app.get('/urls')
def get_urls():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT urls.id, urls.name, url_checks.created_at FROM urls "
            "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
            "WHERE url_checks.id = (SELECT MAX(url_checks.id) FROM url_checks WHERE url_checks.url_id = urls.id) "
            "ORDER BY urls.id DESC")
            results = curs.fetchall()

        return render_template('urls.html', data=results)


@app.get('/urls/<id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)

    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name, created_at FROM urls WHERE id = %s", (id,))
            (url_id, name, created_at) = curs.fetchone()

            curs.execute("SELECT id, created_at FROM url_checks WHERE url_id = %s", (id,))
            check_result = curs.fetchall()

        return render_template(
            'show_url.html',
            messages=messages,
            url_id=url_id,
            name=name,
            created_at=created_at,
            check_result=check_result,
            )


@app.post('/urls/<id>/checks')
def url_checks(id):
    today = date.today()

    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute("INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s)", (id, today))
    
    return redirect(url_for('show_url', id=id))


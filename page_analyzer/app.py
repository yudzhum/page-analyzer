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

    # URL is valid
    if url(input_url) is True:
    
        # Get today date
        today = date.today()
    
        # Add url to database
        with conn.cursor() as cursor:
            # Check if url already in db
            cursor.execute("SELECT id FROM urls WHERE name = %s", (input_url,))
            result = cursor.fetchone()
            if result:
                flash('Адрес уже добавлен', category="alert alert-info")
                (url_id, *_) = result
                return redirect(url_for('show_url', id=url_id))

            # Add url into db
            cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id", (input_url, today))
            (recorded_id, *_) = cursor.fetchone()

        flash('Страница успешно добавлена', category="alert alert-success")
        return redirect(url_for('show_url', id=recorded_id))

    #Invalid url
    else:
        flash('Некорректный URL', category="alert alert-danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages, incorrect_url=input_url)


@app.get('/urls')
def get_urls():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM urls ORDER BY id DESC")
        results = cursor.fetchall()

    return render_template('urls.html', data=results)


@app.get('/urls/<id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)

    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, created_at FROM urls WHERE id = %s", (id,))
        (url_id, name, created_at) = cursor.fetchone()

    return render_template(
        'show_url.html',
        messages=messages,
        url_id=url_id,
        name=name,
        created_at=created_at,
        )


@app.post('/urls/<id>/checks')
def url_checks(id):
    pass

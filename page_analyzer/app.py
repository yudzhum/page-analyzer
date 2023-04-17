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
            cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (input_url, today))

        return redirect(url_for('get_urls'))

    #Invalid url
    else:
        flash('Incorrect URL', category="alert alert-danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages, incorrect_url=input_url)



@app.get('/urls')
def get_urls():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM urls")
        records = cursor.fetchall()
    r = records
    return f'{r}'

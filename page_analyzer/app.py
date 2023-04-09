from flask import (
    Flask, 
    render_template, 
    request, 
    redirect,
    url_for
)
import os
import psycopg2
from dotenv import load_dotenv
from datetime import date


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
    return render_template('index.html')


@app.post('/urls')
def post_urls():
    url = request.form['url']
    today = date.today()
    
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (url, today))

    return redirect(url_for('get_urls'))


@app.get('/urls')
def get_urls():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM urls")
        records = cursor.fetchall()
    r = records
    return f'{r}'

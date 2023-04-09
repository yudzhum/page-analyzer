from flask import (
    Flask, 
    render_template, 
    request
)
import os
import psycopg2
from dotenv import load_dotenv


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
    return f'{url}'


@app.get('/urls')
def get_urls():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls")
    records = cursor.fetchall()
    return f'{records}'

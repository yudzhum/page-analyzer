from flask import (
    Flask, 
    render_template, 
    request
)
import os
from dotenv import load_dotenv


app = Flask(__name__)


# load enviromental variables
load_dotenv()


# enviromental variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def post_urls():
    url = request.form['url']
    return f'{url}'


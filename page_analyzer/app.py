from flask import Flask, render_template
import os
from dotenv import load_dotenv


app = Flask(__name__)


# load enviromental variables
load_dotenv()


# enviromental variables
secret_key = os.environ.get('SECRET_KEY')
database_url = os.environ.get('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls():
    return return f'The secret key is: {secret_key} and the database URL is: {database_url}'

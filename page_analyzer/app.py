from flask import Flask, render_template
import os
from dotenv import load_dotenv


app = Flask(__name__)


# load enviromental variables
load_dotenv()


# enviromental variables
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls():
    if DATABASE_URL is not None:
        return f"DATABASE_URL is load succesfully"
    return f'DATABASE_URL is None'

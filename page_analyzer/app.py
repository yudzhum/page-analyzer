from flask import Flask, render_template
import os
from dotenv import load_dotenv


app = Flask(__name__)


# load enviromental variables
load_dotenv()


# enviromental variables
config_values = {
    'secret_key': os.getenv('SECRET_KEY'),
    'database_url': os.getenv('DATABASE_URL')
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls():
    return f'config is {config_values["secret_key"], config_values["database_url"]}'

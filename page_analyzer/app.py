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
from dotenv import load_dotenv
from datetime import date
from page_analyzer.url import url_parse, url_validation, make_check
from page_analyzer.db_access import (
    get_id_from_urls,
    add_url_into_db,
    get_urls_data,
    get_url_info,
    get_check_info,
    insert_check_result
)

app = Flask(__name__)


load_dotenv()

# enviromental variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def post_urls():
    input_url = request.form['url']
    validation = url_validation(input_url)

    if not validation.get('valid'):
        alert_message = validation.get('message')
        flash(f'{alert_message}', category="alert alert-danger")
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages,
            incorrect_url=input_url
        ), 422

    parsed_url = url_parse(input_url)
    today = date.today()

    result = get_id_from_urls(parsed_url)
    if result:
        (url_id, *_) = result
        flash('Страница уже существует', category="alert alert-info")
        return redirect(url_for('show_url', id=url_id))

    else:
        id_info = add_url_into_db(parsed_url, today)
        (url_id, *_) = id_info

        flash('Страница успешно добавлена', category="alert alert-success")
        return redirect(url_for('show_url', id=url_id))


@app.get('/urls')
def get_urls():
    data = get_urls_data()
    return render_template('urls.html', data=data)


@app.get('/urls/<int:id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)

    (url_id, name, created_at) = get_url_info(id)
    check_result = get_check_info(id)

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

    check_result = make_check(url_name)

    if check_result is None:
        flash('Произошла ошибка при проверке', category="alert alert-danger")
        return redirect(url_for('show_url', id=id))

    today = date.today()
    insert_check_result(id, check_result, today)

    flash('Страница успешно проверена', category='alert alert-success')
    return redirect(url_for('show_url', id=id))

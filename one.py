# -*- coding: utf8 -*-
"""
Веб морда для скрипта vkMusicSync, в которой будет происходить регистрация пользователя,
будут указываться его регистрационные данные для вк.
В последствии скрипт будет автоматически проводить синхронизацию плей листа
и пользователь сможет локально слушать треки через веб страничку.
"""

# все импорты
import os, sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# конфигурация
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = "\x972\x0e'\xe9\x89\xa0\xd6\xa7\xbe\x88\xe1\xb7s\x06\xf4\xb63\xd5J"

# создаем приложение
app = Flask(__name__)
app.config.from_object(__name__)

# загружаем конфигурацию
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'one.db'),
    DEBUG=True,
    SECRET_KEY="\x972\x0e'\xe9\x89\xa0\xd6\xa7\xbe\x88\xe1\xb7s\x06\xf4\xb63\xd5J",
    USERNAME='admin',
    PASSWORD='default'
))
#Возможность загрузить файл конфигурации через переменную
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Устанавливаем соединение с базой данных"""
    connect = sqlite3.connect(app.config['DATABASE'])
    connect.row_factory = sqlite3.Row
    return connect

def init_db():
    """Инициализация базы данных"""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Проверяем соединение с БД. Если нет, создаем"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_tracks():
    """Получаем список треков для главной страницы"""
    #Если пользователь не вошел в систему, то редирект на страницу авторизации
    if not session.get('logged_in'):
        redirect(url_for('login'))
    else:
        db = get_db()
        cur = db.execute('select artist, title from tracks order by id desc')
        entries = cur.fetchall()
    return render_template('show_tracks.html', )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница авторизации"""
    error=None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('show_tracks'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Страница выхода"""
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()



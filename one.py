# -*- coding: utf8 -*-
"""
Веб морда для скрипта vkMusicSync, в которой будет происходить регистрация пользователя,
будут указываться его регистрационные данные для вк.
В последствии скрипт будет автоматически проводить синхронизацию плей листа
и пользователь сможет локально слушать треки через веб страничку.
"""

# все импорты
import os, sqlite3, re, configparser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

#Кто вошел в систему
whoami = ''

# конфигурация
pattern_login = "[a-zA-Zа-яА-Я]"
pattern_pass = "[a-zA-Zа-яА-Я0-9]"
DATABASE = 'one.db'
DEBUG = True
SECRET_KEY = "\x972\x0e'\xe9\x89\xa0\xd6\xa7\xbe\x88\xe1\xb7s\x06\xf4\xb63\xd5J"


# создаем приложение
app = Flask(__name__)
app.config.from_object(__name__)

# загружаем конфигурацию
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'one.db'),
    SECRET_KEY="\x972\x0e'\xe9\x89\xa0\xd6\xa7\xbe\x88\xe1\xb7s\x06\xf4\xb63\xd5J",
    USERNAME='admin',
    PASSWORD='default'
))
#Возможность загрузить файл конфигурации через переменную
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Устанавливаем соединение с базой данных"""
    connect = sqlite3.connect(app.config['DATABASE'])
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
        return redirect(url_for('login'))
    else:
        '''Получаем список файлов из конкретной папки'''
        directory = os.path.join(os.getcwd(), 'static/vkmusic')
        entries = os.listdir(directory)
        for i in xrange(len(entries)):
            entries[i] = 'static/vkmusic/' + entries[i].decode('utf-8')
    return render_template('show_tracks.html', entries=entries)

def check_user(username):
    """Проверяем зарегистрирован ли пользователь"""
    global status
    db = get_db()
    cur = db.execute("select login, password from users where login='{0}'".format(username))
    cur = cur.fetchall()[0]
    if len(cur) != 0:
        status = True
        password = list(cur)[1]
    else:
        status = False
        password = None
    return status, password

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница авторизации"""
    error=None
    if request.method == 'POST':
        #прописать правило проверки длины логина и пароля  
        status, password = check_user(request.form['username'])
        if status == True:
            if request.form['password'].encode('utf8') == password:
                session['logged_in'] = True
                global whoami
                whoami = request.form['username']
                return redirect(url_for('show_tracks'))
            else:
                error = 'Invalid password'
        else:
            error = 'Invalid username'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Страница выхода"""
    session.pop('logged_in', None)
    #flash('You were logged out.')
    return redirect(url_for('login'))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """Страница регистрации"""
    error=None
    if request.method == 'POST':
        if len(request.form['username']) < 4 or not re.search(pattern_login, request.form['username']):
            error = 'Invalid username'
        elif len(request.form['password']) < 8 or not re.search(pattern_pass, request.form['password']):
            error = 'Invalid password'
        else:
            db = get_db()
            try:
                db.execute('insert into users (login, password) values (?, ?)',
                        (request.form['username'], request.form['password']))
                usertable = 'create table %s (id integer primary key autoincrement, artist text not null, title text not null)' % whoami
                db.executescript(usertable)
                db.commit()
                flash('You was succesfully sign up.')
                return redirect(url_for('login'))
            except sqlite3.DatabaseError as err:
                error = err
    return render_template('registration.html', error=error)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'one.cfg'))
    app.run(host = str(config['DEFAULT']['IP']), port = int(config['DEFAULT']['PORT']), debug = str(config['DEFAULT']['DEBUG']))


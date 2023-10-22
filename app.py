import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session, g
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
import os, datetime, time
from datetime import date

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask('__name__')
app.config['SECRET_KEY'] = '12345678'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts = posts)

@app.route('/avaliate/<int:id>', methods=('GET', 'POST'))
def avaliate(id):
    if request.method == 'POST':
        id = request.form['id2']
        av1 = request.form['avaliacao1']
        av2 = request.form['avaliacao2']
        av3 = request.form['avaliacao3']
        data_da_avaliacao = date.today()
        conn = get_db_connection()
        conn.execute('INSERT INTO avaliacoes (id, data_da_avaliacao, avaliacao01, avaliacao02, avaliacao03) VALUES (?, ?, ?, ?, ?)',
                    (id, data_da_avaliacao, av1, av2, av3))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('avaliate.html', post=id)

@app.route('/desc')
def index_desc():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created desc').fetchall()
    conn.close()
    return render_template('index_desc.html', posts = posts)

@app.route('/60')
def index_60():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts WHERE julianday("now") - julianday(created) <= 60 ORDER BY created desc').fetchall()
    conn.close()
    return render_template('index_60.html', posts = posts )

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    cdays = (date.today() - datetime.datetime.strptime(post['created'], '%Y-%m-%d').date()).days
    udays = (date.today() - datetime.datetime.strptime(post['updated'], '%Y-%m-%d').date()).days
    return render_template('post.html', post = post, cdays = cdays, udays = udays)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if g.user is not None:
        if request.method == 'POST':
            title = request.form['title']
            details = request.form['details']
            created = date.today()
            links = request.form['links']
            updated = created
            date1 = request.form['date1']
            evaluation1 = request.form['evaluation1']
            date2 = request.form['date2']
            evaluation2 = request.form['evaluation2']
            date3 = request.form['date3']
            evaluation3 = request.form['evaluation3']
            date4 = request.form['date4']
            evaluation4 = request.form['evaluation4']
            date5 = request.form['date5']
            evaluation5 = request.form['evaluation5']
            date6 = request.form['date6']
            evaluation6 = request.form['evaluation6']
            clipping = request.form['clipping']
            cme = request.form['cme']


            if not title:
                flash('Title is required!')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO posts (created, updated, title, details, links, date1, evaluation1, date2, evaluation2, date3, evaluation3, date4, evaluation4, date5, evaluation5, date6, evaluation6, clipping, cme) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (created, updated, title, details, links, date1, evaluation1, date2, evaluation2, date3, evaluation3, date4, evaluation4, date5, evaluation5, date6, evaluation6, clipping, cme))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
        return render_template('create.html')
    flash('Necessário login!')
    return redirect(url_for('login'))
            

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    if g.user is not None:
        post = get_post(id)

        if request.method == 'POST':
            created = post['created']
            updated = date.today()
            title = request.form['title']
            details = request.form['details']
            links = request.form['links']
            date1 = request.form['date1']
            evaluation1 = request.form['evaluation1']
            date2 = request.form['date2']
            evaluation2 = request.form['evaluation2']
            date3 = request.form['date3']
            evaluation3 = request.form['evaluation3']
            date4 = request.form['date4']
            evaluation4 = request.form['evaluation4']
            date5 = request.form['date5']
            evaluation5 = request.form['evaluation5']
            date6 = request.form['date6']
            evaluation6 = request.form['evaluation6']
            clipping = request.form['clipping']
            cme = request.form['cme']
            
            
            if not title:
                flash('Title is required!')
            else:
                conn = get_db_connection()
                conn.execute('UPDATE posts SET created = ?, updated = ?, title = ?, details = ?, links = ?, date1 = ?,  evaluation1 = ?, date2 = ?, evaluation2 = ?, date3 = ?, evaluation3 = ?, date4 = ?, evaluation4 = ?, date5 = ?, evaluation5 = ?, date6 = ?, evaluation6 = ?, clipping = ?, cme = ?'
                            ' WHERE id = ?',
                            (created, updated, title, details, links,  date1, evaluation1, date2, evaluation2, date3, evaluation3, date4, evaluation4, date5, evaluation5, date6, evaluation6, clipping, cme, id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
        return render_template('edit.html', post=post)
    flash('Necessário login!')
    return redirect(url_for('login'))



@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi excluído do cadastro!'.format(post['title']))
    return redirect(url_for('index'))

# Cadastro e Login #

@app.route('/register', methods=('GET', 'POST'))
def register():  
    if g.user is not None:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            conn = get_db_connection()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'

            if error is None:
                try:
                    conn.execute(
                        "INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
                    )
                    conn.commit()
                except conn.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    flash('"{}" foi cadastrado com sucesso!'.format(request.form['username']))
                    return redirect(url_for("index"))
                flash(error)
        return render_template('register.html')
        
    flash('Necessário login!')
    return render_template('login.html')
    

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        error = None
        user = conn.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db_connection().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

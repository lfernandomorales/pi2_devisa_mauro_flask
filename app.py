import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session, g
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
import os, datetime, time
from datetime import date, datetime

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_avaliacao(post_id):
    conn = get_db_connection()
    avaliacao = conn.execute('SELECT * FROM avaliacoes WHERE id = ?', (post_id,)).fetchall()
    conn.close()
    if avaliacao is None:
        abort(404)
    return avaliacao

app = Flask('__name__')
app.config['SECRET_KEY'] = '12345678'

@app.route('/')
def index():
    conn = get_db_connection()
    if request.args.get('ordered') == '60':
        posts = conn.execute('SELECT * FROM posts WHERE julianday("now") - julianday(created) <= 60 ORDER BY created desc').fetchall()
        ordered = '60'
    if request.args.get('ordered') == 'desc':
        posts = conn.execute('SELECT * FROM posts ORDER BY created desc').fetchall()
        ordered = 'desc'
    else:
        posts = conn.execute('SELECT * FROM posts').fetchall()
        ordered = ''
    conn.close()
   # posts = conn.execute('SELECT * FROM posts').fetchall()
    #conn.close()
    return render_template('index.html', posts = posts, ordered = ordered)

@app.route('/avaliate/<int:id>', methods=('GET', 'POST'))
def avaliate(id):
    if request.method == 'POST':
        id = request.form['id']
        data_da_avaliacao = datetime.now()
        av1 = request.form['avaliacao1']
        av2 = request.form['avaliacao2']
        av3 = request.form['avaliacao3']
        av4 = request.form['avaliacao4']
        av5 = request.form['avaliacao5']
        av6 = request.form['avaliacao6']
        av7 = request.form['avaliacao7']
        av8 = request.form['avaliacao8']
        av9 = request.form['avaliacao9']
        av10 = request.form['avaliacao10']
        av11 = request.form['avaliacao11']
        av12 = request.form['avaliacao12']
        av13 = request.form['avaliacao13']
        av14 = request.form['avaliacao14']
        av15 = request.form['avaliacao15']
        av16 = request.form['avaliacao16']
        av17 = request.form['avaliacao17']
        av18 = request.form['avaliacao18']
        av19 = request.form['avaliacao19']
        av20 = request.form['avaliacao20']
        av21 = request.form['avaliacao21']
        probabilidade = request.form['probabilidade']
        impacto_saude_humana = request.form['impacto_saude_humana']
        impacto_na_assistencia = request.form['impacto_assistencia']
        impacto_social = request.form['impacto_social']
        impacto_na_capacidade_de_resposta = request.form['impacto_capacidade_resposta'] 
        avaliacao_de_risco = request.form['risco'] 
        #compartilhamento_da_informacao BOOLEAN,
        conn = get_db_connection()
        conn.execute('INSERT INTO avaliacoes (id, data_da_avaliacao, avaliacao01, avaliacao02, avaliacao03, avaliacao04, avaliacao05, avaliacao06, avaliacao07, avaliacao08, avaliacao09, avaliacao10, avaliacao11, avaliacao12, avaliacao13, avaliacao14, avaliacao15, avaliacao16, avaliacao17, avaliacao18, avaliacao19, avaliacao20, avaliacao21, probabilidade, impacto_saude_humana, impacto_na_assistencia, impacto_social, impacto_na_capacidade_de_resposta, avaliacao_de_risco) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (id, data_da_avaliacao, av1, av2, av3, av4, av5, av6, av7, av8, av9, av10, av11, av12, av13, av14, av15, av16, av17, av18, av19, av20, av21, probabilidade, impacto_saude_humana, impacto_na_assistencia, impacto_social, impacto_na_capacidade_de_resposta, avaliacao_de_risco))
        conn.execute('UPDATE posts SET ultima_avaliacao_risco = ? WHERE id = ?', (avaliacao_de_risco, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('avaliate.html', post=id)

@app.route('/desc')
def index_desc():
    conn = get_db_connection()
    if request.args('ordered')==60:
        posts = conn.execute('SELECT * FROM posts WHERE julianday("now") - julianday(created) <= 60 ORDER BY created desc').fetchall()
    if request.args('ordered')=='desc':
        posts = conn.execute('SELECT * FROM posts ORDER BY created desc').fetchall()
    else:
        posts = conn.execute('SELECT * FROM posts').fetchall()
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
    avaliacao = get_avaliacao(post_id)
    cdays = (date.today() - datetime.strptime(post['created'], '%Y-%m-%d').date()).days
    udays = (date.today() - datetime.strptime(post['updated'], '%Y-%m-%d').date()).days
    return render_template('post.html', post = post, cdays = cdays, udays = udays, avaliacao = avaliacao)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if g.user is not None:
        if request.method == 'POST':
            title = request.form['title']
            details = request.form['details']
            created = date.today()
            links = request.form['links']
            updated = created
            status_evento = request.form['status_evento']
            clipping = request.form['clipping']
            cme = request.form['cme']
            #ultima_data_no_clipping = request.form['ultima_data_no_clipping']
            #data_inicio_monitoramento_no_cme = request.fomr['data_inicio_monitoramento_no_cme']
            #data_encerramento_do_monitoramento = request.form['data_encerramento_do_monitoramento']


            if not title:
                flash('Title is required!')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO posts (created, updated, title, details, links, clipping, cme, status_evento) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                            (created, updated, title, details, links, clipping, cme,  status_evento))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
        return render_template('create.html', post = [])
    flash('Necessário login!')
    return redirect(url_for('login'))
            

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    if g.user is not None:
        post = get_post(id)

        if request.method == 'POST':
            created = post['created']
            updated = date.today()
            title = request.form['title']
            details = request.form['details']
            links = request.form['links']
            status_evento = request.form['status_evento']
            clipping = request.form['clipping']
            cme = request.form['cme']
            #ultima_data_no_clipping = request.form['ultima_data_no_clipping']
            #data_inicio_monitoramento_no_cme = request.fomr['data_inicio_monitoramento_no_cme']
            #data_encerramento_do_monitoramento = request.form['data_encerramento_do_monitoramento']

            if not title:
                flash('Title is required!')
            else:
                conn = get_db_connection()
                conn.execute('UPDATE posts SET created = ?, updated = ?, title = ?, details = ?, links = ?, status_evento = ?, clipping = ?, cme = ?'
                            ' WHERE id = ?',
                            (created, updated, title, details, links, status_evento, clipping, cme, id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
        return render_template('create.html', post=post)
    flash('Necessário login!')
    return redirect(url_for('login'))



@app.route('/delete/<int:id>', methods=('POST',))
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
            error = 'Incorrect username or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

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

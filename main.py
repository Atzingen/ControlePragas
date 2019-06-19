# -*- coding: latin-1 -*-
from flask import Flask, render_template, redirect, session, request, url_for, flash, make_response
from functools import wraps
from ast import literal_eval
from dateutil import parser
from passlib.hash import sha256_crypt
import banco

app = Flask(__name__)
app.secret_key = b'fjsdakljfwecvakvkjvkdjafkjf'
#banco.cria_banco()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Voce precisa fazer login antes')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
def home():
    return redirect(url_for('inserir'))

@app.route("/cadastro")
def cadastro():
    if request.args:
        try:
            email = request.args.get('email')
            nome = request.args.get('nome')
            quadra = request.args.get('quadra')
            lote = request.args.get('lote')
            telefone = request.args.get('telefone')
            password = sha256_crypt.encrypt(request.args.get('password'))
            if 'logged_in' in session:
                banco.delete_pessoa(session['email'])
                session['email'] = email
                session['nome'] = nome
            banco.insere_pessoa(nome, email, int(quadra), int(lote), str(telefone), password)
            if 'logged_in' in session:
                flash('Usuario atualizado com sucesso')
            else:
                flash('Usuario cadastrado com sucesso')
            return redirect(url_for('inserir'))
        except Exception as e:
            print("except", e)
            flash('Erro no preenchimento do cadastro')
            flash(e)
            render_template('cadastro.html')
    return render_template('cadastro.html')

@app.route("/inserir")
@login_required
def inserir():
    if request.args:
        quantidade = int(request.args.get('quantidade'))
        data = parser.parse(request.args.get('data'))
        posicao = literal_eval(request.args.get('posicao'))
        banco.insere_praga(posicao[0], posicao[1], data, session['email'], quantidade)
    pragas_usuario = banco.lista_pragas(pessoa=session['email'])
    return render_template("inserir.html", pragas_usuario=pragas_usuario)

@app.route('/apagar')
@login_required
def apagar():
    if request.args:
        id_apagar = request.args.get('id')
        banco.remove_praga(int(id_apagar))
        flash('Dado apagado')
    pragas_usuario = banco.lista_pragas(pessoa=session['email'])
    return render_template('inserir.html', pragas_usuario=pragas_usuario)

@app.route("/analise")
@login_required
def analise():
    dados = banco.lista_pragas()
    return render_template("analise.html", dados=dados)

@app.route("/login")
def login():
    if request.args:
        try:
            email = request.args.get('email')
            senha = request.args.get('senha')
            senha_hash = banco.senha_usuario(email)
            if sha256_crypt.verify(senha, senha_hash):
                session['logged_in'] = True
                session['email'] = email
                session['nome'] = banco.nome_usuario(email)
                flash('Login efetuado com sucesso')
                return redirect(url_for('inserir'))
            else:
                flash('usuário e senha não conferem')
        except Exception as e:
            print('except', e)
    return render_template("login.html")

@app.route("/usuario")
@login_required
def usuario():
    return render_template('cadastro.html')

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash('Sua sessão foi terminada com sucesso')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

from flask import Flask, render_template, redirect, session, request, url_for, flash, make_response
from functools import wraps
from passlib.hash import sha256_crypt
import banco

app = Flask(__name__)
app.secret_key = b'fjsdakljfwecvakvkjvkdjafkjf'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
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
                flash('Usuário cadastrado com sucesso')
            else:
                flash('Usuário atualizado com sucesso')
            return redirect(url_for('inserir'))
        except Exception as e:
            print("except", e)
            flash('Erro no preenchimento do cadastro')
            render_template('cadastro.html')
    return render_template('cadastro.html')

@app.route("/inserir")
@login_required
def inserir():
    return render_template("inserir.html")

@app.route("/analise")
@login_required
def analise():
    return render_template("analise.html")

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
    app.run(host='0.0.0.0', port=5000, debug=True)
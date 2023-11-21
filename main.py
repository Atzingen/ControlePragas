import os, base64
from flask import Flask, render_template, redirect, session, request, url_for, flash, make_response
from functools import wraps
from ast import literal_eval
from dateutil import parser
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
from logger_cfg import configure_logger
import banco

load_dotenv()

logger = configure_logger()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

MAPS_API_KEY = os.environ.get('MAPS_API_KEY')
CODIGO_INSCRICAO = os.environ.get('CODIGO_INSCRICAO')
ADMIN_EMAILS = eval(os.environ.get('ADMIN_EMAILS'))

banco.cria_banco()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Voce precisa fazer login antes')
            return redirect(url_for('login'))
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session:
            return f(*args, **kwargs)
        else:
            flash('Apenas admins podem acessar essa pagina')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
def home():
    return redirect(url_for('inserir'))

@app.route("/cadastro")
def cadastro():
    if request.args:
        try:
            codigo = request.args.get('codigo')
            email = request.args.get('email')
            nome = request.args.get('nome')
            quadra = request.args.get('quadra')
            lote = request.args.get('lote')
            telefone = request.args.get('telefone')
            password = sha256_crypt.encrypt(request.args.get('password'))
            if 'logged_in' in session and codigo == CODIGO_INSCRICAO:
                banco.delete_pessoa(session['email'])
                banco.insere_pessoa(nome, email, int(quadra), int(lote), str(telefone), password)
                session['email'] = email
                session['nome'] = nome
                flash('Usuario atualizado com sucesso')
            elif codigo == CODIGO_INSCRICAO:
                banco.insere_pessoa(nome, email, int(quadra), int(lote), str(telefone), password)
                flash('Usuario cadastrado com sucesso')
            else:
                flash('Erro no preenchimento do cadastro')
            return redirect(url_for('inserir'))
        except Exception as e:
            logger.debug(f"except cadastro \n{e}\n\n")
            flash('Erro no preenchimento do cadastro')
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
    return render_template("inserir.html", pragas_usuario=pragas_usuario, MAPS_API_KEY=MAPS_API_KEY)

@app.route('/apagar')
@login_required
def apagar():
    if request.args:
        id_apagar = request.args.get('id')
        banco.remove_praga(int(id_apagar))
        flash('Dado apagado')
    pragas_usuario = banco.lista_pragas(pessoa=session['email'])
    return render_template('inserir.html', pragas_usuario=pragas_usuario)

@app.route('/apaga_user')
@admin_required
def apaga_user():
    if request.args:
        email = request.args.get('email')
        banco.delete_pessoa(email)
        flash('Dado apagado')
    return redirect(url_for('adm_view'))

@app.route("/analise")
@login_required
def analise():
    dados = banco.lista_pragas()
    return render_template("analise.html", dados=dados, MAPS_API_KEY=MAPS_API_KEY)

@app.route("/download")
@login_required
def download():
    dados = banco.lista_pragas()
    csv = 'latitude,longitude,tempo,contato,quantidade\n'
    for dado in dados:
        csv += str(dado[0]) + ',' + str(dado[1]) + ',' + str(dado[2]) + ',' + dado[3] + ',' + str(dado[4]) + '\n'
    response = make_response(csv)
    response.headers['Content-Disposition'] = 'attachment; filename=export.csv'
    response.mimetype='text/csv'
    return response

@app.route("/login")
def login():
    if request.args:
        try:
            email = request.args.get('email')
            senha = request.args.get('password')
            senha_hash = banco.senha_usuario(email)
            if sha256_crypt.verify(senha, senha_hash):
                session['logged_in'] = True
                session['email'] = email
                session['nome'] = banco.nome_usuario(email)
                if email in ADMIN_EMAILS:
                    session['is_admin'] = True
                flash('Login efetuado com sucesso')
                return redirect(url_for('inserir'))
            else:
                flash('usuário e senha não conferem')
        except Exception as e:
            logger.debug(f"except login \n{e}\n\n")
    return render_template("login.html")

@app.route("/usuario")
@login_required
def usuario():
    usuario = banco.dados_usuario(session['email'])
    session['quadra'] = usuario[2]
    session['lote'] = usuario[3]
    session['telefone'] = usuario[4]
    return render_template('cadastro.html')

@app.route("/adm_view")
@admin_required
def adm_view():
    dados = banco.lista_pragas()
    pessoas = banco.lista_pessoas()
    logger.info(f"dados: {dados} pessoas: {pessoas}")
    return render_template("adm_view.html", dados=dados, pessoas=pessoas)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash('Sua sessão foi terminada com sucesso')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404 {request.url}")
    return render_template('404.html')

if __name__ == "__main__":
    logger.info('Iniciando o seriçao com flask debug server')
    app.run(host='0.0.0.0', port=5000, debug=True)

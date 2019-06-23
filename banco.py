# -*- coding: latin-1 -*-
import psycopg2, datetime, os

host_ip = os.environ.get('db_ip_host')
db_pwd = os.environ.get('db_pwd')


def cria_banco():
    try:
        conn = psycopg2.connect(host=host_ip, database='postgres', user='postgres', password=db_pwd)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS escorpiao(id	SERIAL, latitude REAL NOT NULL, longitude REAL NOT NULL, time TEXT NOT NULL, quem TEXT NOT NULL, quantidade INTEGER)')
        conn.commit()
        cursor.execute('CREATE TABLE IF NOT EXISTS pessoas(id SERIAL, Nome TEXT, email TEXT NOT NULL UNIQUE, Quadra INTEGER, Lote INTEGER, Telefone TEXT,Senha TEXT)')
        conn.commit()
        conn.close()
    except:
        conn.close()
        return None
        
def insere_pessoa(Nome, email, Quadra, Lote, Telefone, Senha):
    try:
        conn = psycopg2.connect(host=host_ip, database='postgres', user='postgres', password=db_pwd)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO pessoas(Nome, email, Quadra, Lote, Telefone, Senha) 
                    VALUES(%s,%s,%s,%s,%s,%s)""",  (Nome, email, Quadra, Lote, Telefone, Senha))
        conn.commit()
        conn.close()
    except:
        conn.close()
        return None

def delete_pessoa(email):
    try:
        conn = psycopg2.connect(host=host_ip, database='postgres', user='postgres', password=db_pwd)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM pessoas WHERE email=%s""", (email,))
        conn.commit()
        conn.close()
    except:
        conn.close()
        return None

def insere_praga(latitude, longitude, tempo, quem, quantidade):
    try:
        conn = psycopg2.connect(host=host_ip, database='postgres', user='postgres', password=db_pwd)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO escorpiao(latitude, longitude, time, quem, quantidade) 
                          VALUES(%s,%s,%s,%s,%s)""",(latitude, longitude, tempo,quem, quantidade))
        conn.commit()
        conn.close()
    except:
        conn.close()
        return None

def lista_pragas(pessoa=None, data=None):
    try:
        conn = psycopg2.connect(host=host_ip, database='postgres', user='postgres', password=db_pwd)
        cursor = conn.cursor()
        if pessoa:
            if not data:
                cursor.execute("""SELECT * FROM escorpiao WHERE quem=%s""", (pessoa,))
            else:
                pass  #TODO query by date
        else:
            if not data:
                cursor.execute("""SELECT * FROM escorpiao""")
            else:
                pass # aqui tambem query by date
        return cursor.fetchall()
    except:
        conn.close()
        return None

def remove_praga(id):
    try:
        conn = psycopg2.connect(host=host_ip, database='postgres', user='postgres', password=db_pwd)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM escorpiao WHERE id=%s""", (id,))
        conn.commit()
        conn.close()
    except:
        conn.close()
        return None

def senha_usuario(email):
    try:
        conn = psycopg2.connect(host=host_ip, database='postgres', user='postgres', password=db_pwd)
        cursor = conn.cursor()
        cursor.execute("""SELECT senha from pessoas WHERE email=%s""", (email,))
        senha_banco = cursor.fetchone()[0]
        conn.close()
        return senha_banco
    except:
        conn.close()
        return None
    
def nome_usuario(email):
    try:
        conn = psycopg2.connect(host=host_ip, database='postgres', user='postgres', password=db_pwd)
        cursor = conn.cursor()
        cursor.execute("""SELECT Nome from pessoas WHERE email=%s""", (email,))    
        nome = cursor.fetchone()[0]
        conn.close()
        return nome
    except:
        conn.close()
        return None









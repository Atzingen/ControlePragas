import sqlite3, datetime

local_banco = 'banco.db'

def cria_banco():
    conn = sqlite3.connect(local_banco)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS escorpiao(id	INTEGER PRIMARY KEY AUTOINCREMENT, latitude REAL NOT NULL, longitude REAL NOT NULL, time TEXT NOT NULL, quem TEXT NOT NULL, quantidade INTEGER)')
    conn.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS pessoas(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Nome TEXT, email TEXT NOT NULL UNIQUE, Quadra INTEGER, Lote INTEGER, Telefone TEXT,Senha TEXT)')
    conn.commit()
    conn.close()

def insere_pessoa(Nome, email, Quadra, Lote, Telefone, Senha):
    conn = sqlite3.connect(local_banco)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO pessoas(Nome, email, Quadra, Lote, Telefone, Senha) 
                VALUES(?,?,?,?,?,?)""",  (Nome, email, Quadra, Lote, Telefone, Senha))
    conn.commit()
    conn.close()

def delete_pessoa(email):
    conn = sqlite3.connect(local_banco)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM pessoas WHERE email=?""", (email,))
    conn.commit()
    conn.close()

def insere_praga(latitude, longitude, tempo, quem, quantidade):
    conn = sqlite3.connect(local_banco)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO escorpiao(latitude, longitude, time, quem, quantidade) 
                      VALUES(?,?,?,?,?)""",(latitude, longitude, tempo,quem, quantidade))
    conn.commit()
    conn.close()

def lista_pragas(pessoa=None, data=None):
    conn = sqlite3.connect(local_banco)
    cursor = conn.cursor()
    if pessoa:
        if not data:
            cursor.execute("""SELECT * FROM escorpiao WHERE quem=?""", (pessoa,))
        else:
            pass  #TODO query by date
    else:
        if not data:
            cursor.execute("""SELECT * FROM escorpiao""")
        else:
            pass # aqui tambem query by date
    return cursor.fetchall()

def remove_praga(id):
    conn = sqlite3.connect(local_banco)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM escorpiao WHERE id=?""", (id,))
    conn.commit()
    conn.close()

def senha_usuario(email):
    conn = sqlite3.connect(local_banco)
    cursor = conn.cursor()
    cursor.execute("""SELECT senha from pessoas WHERE email=?""", (email,))
    senha_banco = cursor.fetchone()[0]
    return senha_banco

def nome_usuario(email):
    conn = sqlite3.connect(local_banco)
    cursor = conn.cursor()
    cursor.execute("""SELECT Nome from pessoas WHERE email=?""", (email,))
    nome = cursor.fetchone()[0]
    return nome

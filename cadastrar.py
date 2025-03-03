import sqlite3


conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        senha TEXT
    )
""")
conn.commit()


def cadastrar_usuario(nome, senha):
    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))
    conn.commit()

cadastrar_usuario("Alexsandro", "201211")
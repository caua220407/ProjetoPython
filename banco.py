
import sqlite3
from pathlib import Path


# Caminho fixo para o banco de dados
BASE_DIR = Path(__file__).resolve().parent
CAMINHO_BANCO = BASE_DIR / "misterINFRA.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def criar_banco():

    with conectar() as conexao:

        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                foto TEXT,
                usa_oculos INTEGER
            )
        """)

        # Compatibilidade com bancos antigos
        cursor.execute("PRAGMA table_info(usuarios)")
        colunas = cursor.fetchall()

        nomes_colunas = [coluna[1] for coluna in colunas]

        if "foto" not in nomes_colunas:
            cursor.execute("""
                ALTER TABLE usuarios
                ADD COLUMN foto TEXT
            """)

        if "usa_oculos" not in nomes_colunas:
            cursor.execute("""
                ALTER TABLE usuarios
                ADD COLUMN usa_oculos INTEGER
            """)


def cadastrar_usuario(nome, foto, usa_oculos=None):

    with conectar() as conexao:

        cursor = conexao.cursor()

        # Verifica se o nome já existe
        cursor.execute("""
            SELECT idUsuario FROM usuarios
            WHERE nome = ?
        """, (nome,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return None

        # Cadastra o novo usuário
        cursor.execute("""
            INSERT INTO usuarios (nome, foto, usa_oculos)
            VALUES (?, ?, ?)
        """, (nome, foto, usa_oculos))

        return cursor.lastrowid


def listar_usuarios():

    # Mantém a compatibilidade com códigos antigos
    with conectar() as conexao:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT idUsuario, nome, foto
            FROM usuarios
        """)

        return cursor.fetchall()


def listar_usuarios_com_oculos():

    with conectar() as conexao:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT idUsuario, nome, foto, usa_oculos
            FROM usuarios
        """)

        return cursor.fetchall()


def buscar_usuario(id_usuario):

    with conectar() as conexao:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT idUsuario, nome, foto
            FROM usuarios
            WHERE idUsuario = ?
        """, (id_usuario,))

        return cursor.fetchone()


def buscar_usuario_com_oculos(id_usuario):

    with conectar() as conexao:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT idUsuario, nome, foto, usa_oculos
            FROM usuarios
            WHERE idUsuario = ?
        """, (id_usuario,))

        return cursor.fetchone()


# Inicializa a estrutura do banco
criar_banco()

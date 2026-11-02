import sqlite3
from pathlib import Path #serve para montar caminhos de arquivo.

PASTA_DATABASE = Path(__file__).resolve().parent
PASTA_PROJETO = PASTA_DATABASE.parent


class SQLiteDB:
    ARQUIVO_BANCO = PASTA_PROJETO / "worknow.db"
    PASTA_SCRIPTS = PASTA_DATABASE / "scripts"

    def __init__(self):
        self.conn = None
        self.cursor = None

    def conectar(self):
        """Abre a conexão com o banco."""
        self.conn = sqlite3.connect(self.ARQUIVO_BANCO)
        self.conn.row_factory = sqlite3.Row  # permite usar linha["nome"]
        self.conn.execute("PRAGMA foreign_keys = ON")  # ativa as chaves estrangeiras
        self.cursor = self.conn.cursor()

    def desconectar(self):
        """Fecha a conexão com o banco."""
        if self.conn:
            self.conn.close()
        self.conn = None
        self.cursor = None

    def executar(self, query, params=()):
        """Executa INSERT, UPDATE ou DELETE. Retorna o id da linha criada.
        Ainda NÃO salva: chame confirmar() quando terminar tudo."""
        self.cursor.execute(query, params)
        return self.cursor.lastrowid

    def consultar(self, query, params=()):
        """Executa um SELECT e devolve a lista de linhas."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def confirmar(self):
        """Salva de verdade tudo que foi executado."""
        self.conn.commit()

    def desfazer(self):
        """Cancela tudo que foi executado desde o último confirmar()."""
        self.conn.rollback()

    def executar_script_sql(self, nome_arquivo):
        """Roda um arquivo .sql da pasta database/scripts."""
        caminho = self.PASTA_SCRIPTS / nome_arquivo
        with open(caminho, "r", encoding="utf-8") as f:
            script = f.read()
        self.cursor.executescript(script)
        self.conn.commit()
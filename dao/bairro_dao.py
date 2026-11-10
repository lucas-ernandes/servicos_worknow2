from database.sqlitedb import SQLiteDB

class BairroDAO:
    def __init__(self):
        self.db = SQLiteDB()
    
    def listar_todos(self):
        """ Devolve todos os bairros em ordem alfabética.
        Cada bairro é um dicionário: {"id_bairro": 1, "nome_bairro": "...", "zona": "..."} """
        self.db.conectar()
        try:
            linhas = self.db.consultar(
                "SELECT id_bairro, nome_bairro, zona FROM bairros ORDER BY nome_bairro;"
            )
        finally:
            self.db.desconectar()
            
        return [dict(linha) for linha in linhas]
    
    def buscar_por_id(self, id_bairro):
        # Devolve o bairro (dicionário) ou None se o id não existir.
        self.db.conectar()
        try:
            linhas = self.db.consultar(
                "SELECT id_bairro, nome_bairro, zona FROM bairros WHERE id_bairro = ?;",
                (id_bairro,),
            )
        finally:
            self.db.desconectar()

        if len(linhas) == 0:
            return None
        return dict(linhas[0])
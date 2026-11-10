from database.sqlitedb import SQLiteDB

class CategoriaDAO:
    
    def __init__(self):
        self.db = SQLiteDB()

    def listar_todas(self):
        """ Devolve todas as categorias em ordem alfabética.
        Cada categoria é um dicionário: {"id_categoria": 1, "nome_categoria": "..."} """

        self.db.conectar()
        try:
            linhas = self.db.consultar(
                "SELECT id_categoria, nome_categoria FROM categorias_servico ORDER BY nome_categoria;"
            )
            
        finally:
            self.db.desconectar()
        
        return [dict(linha) for linha in linhas]
        
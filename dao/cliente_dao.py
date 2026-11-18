from database.sqlitedb import SQLiteDB

class ClienteDAO:
    def __init__(self):
        self.db = SQLiteDB()
    
    """Devolve o id_bairro salvo no cadastro do cliente, ou None se ele
        não tiver escolhido um bairro (é opcional para cliente)."""
    def buscar_bairro(self, id_usuario):
        self.db.conectar()
        try:
            linhas = self.db.consultar(
                "SELECT id_bairro FROM clientes WHERE id_usuario = ?;", (id_usuario,)
            )
        finally:
            self.db.desconectar()

        if len(linhas) == 0:
            return None
        return linhas[0]["id_bairro"]
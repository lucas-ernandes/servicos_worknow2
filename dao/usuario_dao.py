from database.sqlitedb import SQLiteDB

class UsuarioDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def buscar_por_email(self, email):
        """Retorna um dicionário com os dados do usuário, ou None se não existir."""
        self.db.conectar()
        try:
            linhas = self.db.consultar("SELECT * FROM usuarios WHERE email = ?;", (email,))
        finally:
            self.db.desconectar()

        if len(linhas) == 0:
            return None
        return dict(linhas[0])

    def _inserir_usuario(self, data, tipo):
        """Insere na tabela usuarios e devolve o id novo (uso interno do DAO)."""
        sql = """INSERT INTO usuarios (nome, email, senha_hash, telefone, tipo_usuario)
                 VALUES (?, ?, ?, ?, ?);"""
        return self.db.executar(
            sql,
            (data["nome"], data["email"], data["senha_hash"], data["telefone"], tipo),
        )

    def criar_cliente(self, data):
        """Salva em usuarios + clientes. Retorna o id do usuário, ou None se der erro."""
        self.db.conectar()
        try:
            id_usuario = self._inserir_usuario(data, "cliente")
            self.db.executar(
                "INSERT INTO clientes (id_usuario, endereco_referencia) VALUES (?, ?);",
                (id_usuario, data["endereco"]),
            )
            self.db.confirmar()  # só salva se os dois INSERT deram certo
            return id_usuario
        except Exception as erro:
            self.db.desfazer()  # se algo falhou, não salva nada
            print(f"Erro ao criar cliente: {erro}")
            return None
        finally:
            self.db.desconectar()

    def criar_profissional(self, data):
        """Salva em usuarios + profissionais. Retorna o id do usuário, ou None se der erro."""
        self.db.conectar()
        try:
            id_usuario = self._inserir_usuario(data, "profissional")
            self.db.executar(
                """INSERT INTO profissionais (id_usuario, endereco_referencia, categoria, descricao)
                   VALUES (?, ?, ?, ?);""",
                (id_usuario, data["endereco"], data["categoria"], data["descricao"]),
            )
            self.db.confirmar()
            return id_usuario
        except Exception as erro:
            self.db.desfazer()
            print(f"Erro ao criar profissional: {erro}")
            return None
        finally:
            self.db.desconectar()
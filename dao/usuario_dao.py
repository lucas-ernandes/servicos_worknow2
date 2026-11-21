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
                "INSERT INTO clientes (id_usuario, id_bairro) VALUES (?, ?);",
                (id_usuario, data["id_bairro"]),
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
                """INSERT INTO profissionais (id_usuario, id_bairro, id_categoria, descricao)
                   VALUES (?, ?, ?, ?);""",
                (id_usuario, data["id_bairro"], data["id_categoria"], data["descricao"]),
            )
            self.db.confirmar()
            return id_usuario
        except Exception as erro:
            self.db.desfazer()
            print(f"Erro ao criar profissional: {erro}")
            return None
        finally:
            self.db.desconectar()
            
    def buscar_perfil_cliente(self, id_usuario):
        """Dados para a tela "Editar perfil" de um cliente."""
        sql = """
            SELECT u.id_usuario, u.nome, u.email, u.telefone, u.foto, c.id_bairro
            FROM usuarios u
            JOIN clientes c ON c.id_usuario = u.id_usuario
            WHERE u.id_usuario = ?;
        """
        self.db.conectar()
        try:
            linhas = self.db.consultar(sql, (id_usuario,))
        finally:
            self.db.desconectar()
        if len(linhas) == 0:
            return None
        return dict(linhas[0])
    
    
    def buscar_perfil_profissional(self, id_usuario):
        """Dados para a tela "Editar perfil" de um profissional."""
        sql = """
            SELECT u.id_usuario, u.nome, u.email, u.telefone, u.foto,
                   p.id_bairro, p.id_categoria, p.descricao
            FROM usuarios u
            JOIN profissionais p ON p.id_usuario = u.id_usuario
            WHERE u.id_usuario = ?;
        """
        self.db.conectar()
        try:
            linhas = self.db.consultar(sql, (id_usuario,))
        finally:
            self.db.desconectar()
        if len(linhas) == 0:
            return None
        return dict(linhas[0])
    
    
    def atualizar_cliente(self, id_usuario, nome, telefone, id_bairro):
        """Atualiza nome/telefone (usuarios) e bairro (clientes). Devolve True/False."""
        self.db.conectar()
        try:
            self.db.executar(
                "UPDATE usuarios SET nome = ?, telefone = ? WHERE id_usuario = ?;",
                (nome, telefone, id_usuario),
            )
            self.db.executar(
                "UPDATE clientes SET id_bairro = ? WHERE id_usuario = ?;",
                (id_bairro, id_usuario),
            )
            self.db.confirmar()
            return True
        except Exception as erro:
            self.db.desfazer()
            print(f"Erro ao atualizar cliente: {erro}")
            return False
        finally:
            self.db.desconectar()
    
    
    def atualizar_profissional(self, id_usuario, nome, telefone, id_bairro, id_categoria, descricao):
        """Atualiza nome/telefone (usuarios) e bairro/categoria/descrição (profissionais)."""
        self.db.conectar()
        try:
            self.db.executar(
                "UPDATE usuarios SET nome = ?, telefone = ? WHERE id_usuario = ?;",
                (nome, telefone, id_usuario),
            )
            self.db.executar(
                """UPDATE profissionais SET id_bairro = ?, id_categoria = ?, descricao = ?
                   WHERE id_usuario = ?;""",
                (id_bairro, id_categoria, descricao, id_usuario),
            )
            self.db.confirmar()
            return True
        except Exception as erro:
            self.db.desfazer()
            print(f"Erro ao atualizar profissional: {erro}")
            return False
        finally:
            self.db.desconectar()
            
    def atualizar_foto(self, id_usuario, nome_arquivo):
        self.db.conectar()
        try:
            self.db.executar("UPDATE usuarios SET foto = ? WHERE id_usuario = ?;", (nome_arquivo, id_usuario))
            self.db.confirmar()
            return True
        except Exception as erro:
            self.db.desfazer()
            print(f"Erro ao atualizar foto: {erro}")
            return False
        finally:
            self.db.desconectar()
            
    
    def buscar_foto(self, id_usuario):
        """Nome do arquivo de foto do usuário logado, ou None se não tiver.
        Usada pra mostrar a bolinha no menu, sem precisar mexer no login."""
        self.db.conectar()
        try:
            linhas = self.db.consultar("SELECT foto FROM usuarios WHERE id_usuario = ?;", (id_usuario,))
        finally:
            self.db.desconectar()
        if len(linhas) == 0:
            return None
        return linhas[0]["foto"]
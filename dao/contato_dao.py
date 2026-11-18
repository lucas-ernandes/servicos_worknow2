from database.sqlitedb import SQLiteDB

class ContatoDAO:
    def __init__(self):
        self.db = SQLiteDB()
        
    '''
    Contato ainda em andamento (status 'iniciado') entre esse cliente e
    esse profissional, ou None. Serve para não criar um contato novo toda
    vez que o cliente clicar em "Entrar em contato" com a mesma pessoa.
    '''
    def buscar_ativo(self, id_cliente, id_profissional):
        self.db.conectar()
        try:
            linhas = self.db.consultar(
                """SELECT * FROM contatos
                    WHERE id_cliente = ? AND id_profissional = ? AND status = 'iniciado'; """,
                (id_cliente, id_profissional),
            )
        finally:
            self.db.desconectar()

        if len(linhas) == 0:
            return None
        return dict(linhas[0])
    
    
    def criar(self, id_cliente, id_profissional):
        """Cria um novo contato com status 'iniciado'. Devolve o id criado."""
        self.db.conectar()
        try:
            id_contato = self.db.executar(
                "INSERT INTO contatos (id_cliente, id_profissional) VALUES (?, ?);",
                (id_cliente, id_profissional),
            )
            self.db.confirmar()
            return id_contato
        finally:
            self.db.desconectar()
            
    def buscar_por_id(self, id_contato):
        """Devolve o contato (dicionário) ou None se o id não existir."""
        self.db.conectar()
        try:
            linhas = self.db.consultar("SELECT * FROM contatos WHERE id_contato = ?;", (id_contato,))
        finally:
            self.db.desconectar()

        if len(linhas) == 0:
            return None
        return dict(linhas[0])
    
    def marcar_concluido(self, id_contato):
        self.db.conectar()
        try:
            self.db.executar("UPDATE contatos SET status = 'concluido' WHERE id_contato = ?;", (id_contato,))
            self.db.confirmar()
            return True
        except Exception as erro:
            self.db.desfazer()
            print(f'Erro ao concluir contato: {erro}')
            return False
        finally:
            self.db.desconectar()
    
    
    def listar_do_cliente(self, id_cliente):
        """Lista os contatos do cliente, já com o nome e a categoria do
        profissional e, se existir, a avaliação já feita.
        LEFT JOIN: junta com avaliacoes mesmo quando ainda não existe avaliação
        para aquele contato (nesse caso id_avaliacao e nota vêm como None)."""

        sql = """
            SELECT c.id_contato, c.status, c.data_contato,
                p.id_profissional, u.nome AS nome_profissional, cat.nome_categoria,
                a.id_avaliacao, a.nota
            FROM contatos c
            JOIN profissionais p ON p.id_profissional = c.id_profissional
            JOIN usuarios u ON u.id_usuario = p.id_usuario
            JOIN categorias_servico cat ON cat.id_categoria = p.id_categoria
            LEFT JOIN avaliacoes a ON a.id_contato = c.id_contato
            WHERE c.id_cliente = ?
            ORDER BY c.data_contato DESC;
        """
        
        self.db.conectar()
        try:
            linhas = self.db.consultar(sql, (id_cliente,))
        finally:
            self.db.desconectar()
        return [dict(linha) for linha in linhas]
        
            
    
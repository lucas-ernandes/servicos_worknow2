from database.sqlitedb import SQLiteDB

class AvalicaoDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def existe_para_contato(self, id_contato):
        """True se esse contato já foi avaliado (cada contato só pode ter 1 avaliação)."""
        self.db.conectar()
        try:
            linhas = self.db.consultar("SELECT 1 FROM avaliacoes WHERE id_contato = ?;", (id_contato,))
        finally:
            self.db.desconectar()
        return len(linhas) > 0
    
    
    def criar(self, id_contato, id_cliente, id_profissional, nota, comentario):
        """Salva a avaliação e recalcula a nota média do profissional.
        Devolve True se deu certo."""
        self.db.conectar()
        try:
            self.db.executar(
                """INSERT INTO avaliacoes (id_contato, id_cliente, id_profissional, nota, comentario)
                   VALUES (?, ?, ?, ?, ?);""",
                (id_contato, id_cliente, id_profissional, nota, comentario),
            )
            # Recalcula a média com TODAS as notas desse profissional (incluindo a que acabou de entrar)
            media = self.db.consultar(
                "SELECT AVG(nota) AS media FROM avaliacoes WHERE id_profissional = ?;",
                (id_profissional,),
            )[0]["media"]
            
            self.db.executar(
                "UPDATE profissionais SET nota_media = ? WHERE id_profissional = ?;",
                (media, id_profissional),
            )
            self.db.confirmar()
            return True
        except Exception as erro:
            self.db.desfazer()
            print(f"Erro ao criar avaliação: {erro}")
            return False
        finally:
            self.db.desconectar()
            
    def listar_do_profissional(self, id_profissional):
        """Avaliações recebidas por um profissional, com o nome de quem avaliou."""
        sql = """
            SELECT a.id_avaliacao, a.nota, a.comentario, a.resposta_profissional, a.data_avaliacao,
                   u.nome AS nome_cliente, u.foto AS foto_cliente
            FROM avaliacoes a
            JOIN usuarios u ON u.id_usuario = a.id_cliente
            WHERE a.id_profissional = ?
            ORDER BY a.data_avaliacao DESC;
        """
        self.db.conectar()
        try:
            linhas = self.db.consultar(sql, (id_profissional,))
        finally:
            self.db.desconectar()
        return [dict(linha) for linha in linhas]
    
    
    def responder(self, id_avaliacao, id_profissional, texto):
        """Grava a resposta do profissional. Só funciona se a avaliação for
        DESSE profissional e ainda NÃO tiver resposta (1 resposta por avaliação).
        Devolve True só se alguma linha foi realmente alterada."""
        self.db.conectar()
        try:
            self.db.executar(
                """UPDATE avaliacoes SET resposta_profissional = ?
                   WHERE id_avaliacao = ? AND id_profissional = ? AND resposta_profissional IS NULL;""",
                (texto, id_avaliacao, id_profissional),
            )
            # rowcount = quantas linhas o UPDATE realmente mudou. Se for 0, a condição do
            # WHERE não bateu (avaliação de outro profissional, ou já tinha resposta).
            alterou = self.db.cursor.rowcount > 0
            self.db.confirmar()
            return alterou
        except Exception as erro:
            self.db.desfazer()
            print(f"Erro ao responder avaliação: {erro}")
            return False
        finally:
            self.db.desconectar()
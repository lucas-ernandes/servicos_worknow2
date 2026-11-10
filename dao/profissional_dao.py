from database.sqlitedb import SQLiteDB

# Parte fixa da consulta (igual para todas as buscas).
'''
JOIN = "juntar tabelas". O profissional só guarda o NÚMERO do bairro e da 
categoria; com o JOIN a gente pega o NOME deles nas outras tabelas, e o nome da pessoa na tabela usuarios.
''' 
# Só aparecem profissionais disponíveis (interruptor ligado) e com conta ativa.

CONSULTA_BASE = """
    SELECT p.id_profissional, u.nome, p.descricao, p.nota_media,
        b.nome_bairro, b.zona, c.nome_categoria
    FROM profissionais p
    JOIN usuarios u ON u.id_usuario = p.id_usuario
    JOIN bairros b ON b.id_bairro = p.id_bairro
    JOIN categorias_servico c ON c.id_categoria = p.id_categoria
    WHERE p.disponivel = 1 AND u.status = 'ativo'
"""

# Ordem da lista: maior nota primeiro (DESC). Se empatar, ordem alfabética pelo nome.
ORDEM = " ORDER BY p.nota_media DESC, u.nome;"


"""Monta a consulta: base + filtro + (categoria, se foi escolhida) + ordem.
    Os pedaços de texto que somam aqui são FIXOS.
    Os valores que vêm do usuário vão sempre separados, nos "?"."""
class ProfissionalDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def _buscar(self, filtro, valores, id_categoria):
        
        sql =  CONSULTA_BASE + filtro
        if id_categoria is not None:
            sql += " AND p.id_categoria = ?"
            valores = valores + (id_categoria,)
        sql += ORDEM
        
        self.db.conectar()
        try:
            linhas = self.db.consultar(sql, valores)
        finally:
            self.db.desconectar()
        return [dict(linha) for linha in linhas]
    
    """Profissionais que atendem exatamente nesse bairro."""
    def buscar_no_bairro(self, id_bairro, id_categoria=None):
        return self._buscar(" AND p.id_bairro = ?", (id_bairro,), id_categoria)


    def buscar_na_zona(self, zona, id_bairro_excluido, id_categoria=None):
        """Profissionais dos OUTROS bairros da mesma zona."""
        return self._buscar(
            " AND b.zona = ? AND p.id_bairro != ?",
            (zona, id_bairro_excluido),
            id_categoria,
        )

    def buscar_todos(self, id_categoria=None):
        """Profissionais de qualquer bairro."""
        return self._buscar("", (), id_categoria)
    
    '''  Dados do perfil público de UM profissional (dicionário), ou None se não existir.
Aparece mesmo se estiver indisponível (a página avisa), mas não se a conta
estiver inativa ou banida. Não devolve e-mail nem telefone.'''

    def buscar_por_id(self, id_profissional):
     
        sql = """
            SELECT p.id_profissional, u.nome, u.data_cadastro, p.descricao,
                p.nota_media, p.disponivel,
                b.nome_bairro, b.zona, c.nome_categoria
            FROM profissionais p
            JOIN usuarios u ON u.id_usuario = p.id_usuario
            JOIN bairros b ON b.id_bairro = p.id_bairro
            JOIN categorias_servico c ON c.id_categoria = p.id_categoria
            WHERE p.id_profissional = ? AND u.status = 'ativo';
        """
        
        self.db.conectar()
        try:
            linhas = self.db.consultar(sql, (id_profissional,))
        finally:
            self.db.desconectar()
        
        if len(linhas) == 0:
            return None
        return dict(linhas[0])
    
    def buscar_disponibilidade(self, id_usuario):
        self.db.conectar()
        try:
            linhas = self.db.consultar(
                "SELECT disponivel FROM profissionais WHERE id_usuario = ?;",
                (id_usuario,),
            )
        finally:
            self.db.desconectar()
        
        if len(linhas) == 0:
            return None
        return linhas[0]["disponivel"]
    
    
    def atualizar_disponibilidade(self, id_usuario, valor):
        """Liga (1) ou desliga (0) a disponibilidade. Devolve True se deu certo."""
        self.db.conectar()
        try:
            # WHERE id_usuario = ?  garante que só mexe no profissional logado
            self.db.executar(
                "UPDATE profissionais SET disponivel = ? WHERE id_usuario = ?;",
                (valor, id_usuario),
            )
            self.db.confirmar()
            return True
        except Exception as erro:
            self.db.desfazer()
            print(f"Erro ao atualizar disponibilidade: {erro}")
            return False
        finally:
            self.db.desconectar()

    
        
        
        
        

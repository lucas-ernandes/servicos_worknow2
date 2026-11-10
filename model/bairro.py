from dao.bairro_dao import BairroDAO

"""Lista os bairros para montar a caixa de seleção do cadastro.
repassa o pedido ao DAO. É aqui que vai entrar a regra de
"bairros próximos" .
"""

class Bairro:
    @staticmethod
    def listar():
        return BairroDAO().listar_todos()
    
    @staticmethod
    def buscar(id_bairro):
        return BairroDAO().buscar_por_id(id_bairro)
    
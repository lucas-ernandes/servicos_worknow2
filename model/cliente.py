from dao.cliente_dao import ClienteDAO

class Cliente:
    
    @staticmethod
    def bairro_salvo(id_usuario):
    # id_bairro do cadastro do cliente, ou None se ele não escolheu um.
        return ClienteDAO().buscar_bairro(id_usuario)
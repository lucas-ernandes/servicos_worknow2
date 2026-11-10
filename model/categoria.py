from dao.categoria_dao import CategoriaDAO

class Categoria:
    @staticmethod
    def listar():
        # Listar as categorias de serviçopara a caixa de selecao
        return CategoriaDAO().listar_todas()
        
from dao.profissional_dao import ProfissionalDAO
from model.bairro import Bairro
from model.util import para_inteiro

class Profissional:
    """
    Regra da busca. Recebe o que veio da URL (texto) e devolve um dicionário:
            "nivel": "todos"   -> nenhum bairro escolhido
                     "bairro"  -> achou profissionais no bairro escolhido
                     "zona"    -> não tinha no bairro, mostra os da mesma zona
                     "nenhum"  -> não achou nem na zona
                     
            "bairro": o bairro escolhido (ou None)
            "profissionais": lista de profissionais encontrados"""
    @staticmethod
    def buscar(texto_bairro, texto_categoria):
        id_bairro = para_inteiro(texto_bairro)
        id_categoria = para_inteiro(texto_categoria)
        dao = ProfissionalDAO()

        bairro = None
        if id_bairro is not None:
            bairro = Bairro.buscar(id_bairro)
        
        # Sem bairro: mostra todo mundo (filtrando só pela categoria, se escolhida)
        if bairro is None:
            return {"nivel": "todos", "bairro": None,
                    "profissionais": dao.buscar_todos(id_categoria)}
            
        # 1º) tenta no bairro escolhido
        lista = dao.buscar_no_bairro(bairro["id_bairro"], id_categoria)
        if len(lista) > 0:
            return {"nivel": "bairro", "bairro": bairro, "profissionais": lista}

        # 2º) não tinha: tenta nos outros bairros da mesma zona
        lista = dao.buscar_na_zona(bairro["zona"], bairro["id_bairro"], id_categoria)
        if len(lista) > 0:
            return {"nivel": "zona", "bairro": bairro, "profissionais": lista}

        # 3º) não tem nada
        return {"nivel": "nenhum", "bairro": bairro, "profissionais": []}


    @staticmethod
    def obter(id_profissional):
        """Dados do perfil público de um profissional (ou None se não existir)."""
        return ProfissionalDAO().buscar_por_id(id_profissional)
    
    @staticmethod
    def esta_disponivel(id_usuario):
        """True (disponível), False (indisponível) ou None (não é profissional)."""
        valor =  ProfissionalDAO().buscar_disponibilidade(id_usuario)
        if valor is None:
             return None
        return valor == 1
    
    @staticmethod
    def definir_disponibilidade(id_usuario, texto):
        """Liga ou desliga. O 'texto' vem do formulário: "1" liga, "0" desliga.
        Qualquer outro valor é recusado (alguém pode mexer no formulário pelo navegador).
        Devolve True se deu certo."""
        
        if texto not in ("0", "1"):
            return False
        return ProfissionalDAO().atualizar_disponibilidade(id_usuario, int(texto))
     

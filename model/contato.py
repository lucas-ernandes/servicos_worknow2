from urllib.parse import quote

from dao.contato_dao import ContatoDAO
from dao.avalicao_dao import AvalicaoDAO
from dao.profissional_dao import ProfissionalDAO
from model.util import formatar_whatsapp


class Contato:
    @staticmethod
    def iniciar(id_cliente, id_profissional):
        """Cria o contato (ou reaproveita um que já está em andamento) e
        devolve o link do WhatsApp do profissional. Devolve None se o
        profissional não existir (id errado ou conta banida)."""
        info = ProfissionalDAO().buscar_contato(id_profissional)
        if info is None:
            return None

        dao = ContatoDAO()
        if dao.buscar_ativo(id_cliente, id_profissional) is None:
            dao.criar(id_cliente, id_profissional)

        numero = formatar_whatsapp(info["telefone"])
        mensagem = f"Olá, {info['nome']}! Vi seu perfil no WorkNOW e gostaria de saber mais sobre seus serviços."
        return f"https://wa.me/{numero}?text={quote(mensagem)}"

    @staticmethod
    def concluir(id_contato, id_cliente):
        """Marca como concluído. Só funciona se o contato for DESSE cliente
        e ainda estiver com status 'iniciado'. Devolve True/False."""
        contato = ContatoDAO().buscar_por_id(id_contato)
        if contato is None or contato["id_cliente"] != id_cliente:
            return False
        if contato["status"] != "iniciado":
            return False
        return ContatoDAO().marcar_concluido(id_contato)

    @staticmethod
    def listar_do_cliente(id_cliente):
        return ContatoDAO().listar_do_cliente(id_cliente)

    @staticmethod
    def obter_avaliavel(id_contato, id_cliente):
        """Usado antes de mostrar o formulário de avaliação: só devolve o
        contato se ele for desse cliente, estiver concluído e ainda não
        tiver sido avaliado. Qualquer outro caso devolve None."""
        contato = ContatoDAO().buscar_por_id(id_contato)
        if contato is None or contato["id_cliente"] != id_cliente:
            return None
        if contato["status"] != "concluido":
            return None
        if AvalicaoDAO().existe_para_contato(id_contato):
            return None

        # Acrescenta o nome do profissional, para a tela de avaliação mostrar "Avaliar Fulano"
        info = ProfissionalDAO().buscar_contato(contato["id_profissional"])
        contato["nome_profissional"] = info["nome"] if info else "profissional"
        return contato
    
    
    @staticmethod
    def remover(id_contato, id_cliente):
        """Remove (oculta) o contato da lista do cliente, em qualquer status
        (iniciado, concluído, com ou sem avaliação). Só funciona se o contato
        for desse cliente. A avaliação, se existir, continua existindo e
        continua contando na nota média do profissional."""
        
        contato = ContatoDAO().buscar_por_id(id_contato)
        if contato is None or contato["id_cliente"] != id_cliente:
            return False
        return ContatoDAO().ocultar(id_contato)

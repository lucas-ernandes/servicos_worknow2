from dao.avalicao_dao import AvalicaoDAO

class Avaliacao:
    def __init__(self, form):
        self.errors = []
        self.data = {
            'nota': form.get('nota', ""),
            'comentario': form.get('comentario', "").strip(),
        }
        
    def validate(self):
        if self.data["nota"] not in ("1", "2", "3", "4", "5"):
            self.errors.append("Escolha uma nota de 1 a 5 estrelas.")

    def salvar(self, id_contato, id_cliente, id_profissional):
        """Só chame depois de validate() não ter encontrado erros."""
        ok = AvalicaoDAO().criar(
           id_contato, id_cliente, id_profissional,
           int(self.data['nota']), self.data['comentario'],
        )
        if not ok:
            self.errors.append('Não foi possível registrar sua avaliação. Tente novamente. ')
        return ok
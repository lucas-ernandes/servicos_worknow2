import re
from dao.usuario_dao import UsuarioDAO
from model.util import para_inteiro

class Perfil:
    def __init__(self, tipo, form):
        """tipo: "cliente" ou "profissional" (vem da sessão, não do formulário,
        pra ninguém conseguir trocar o próprio tipo de conta editando o HTML)."""
        self.tipo = tipo
        self.errors = []
        self.data = {
            "nome": form.get("nome", "").strip(),
            "telefone": re.sub(r"\D", "", form.get("telefone", "")),
            "id_bairro": para_inteiro(form.get("id_bairro", "")),
            "id_categoria": para_inteiro(form.get("id_categoria", "")) if tipo == "profissional" else None,
            "descricao": form.get("descricao", "").strip() if tipo == "profissional" else "",
        }

    def validate(self):
        d = self.data

        if not d["nome"]:
            self.errors.append("Preencha o nome.")
        if len(d["nome"]) > 150:
            self.errors.append("O nome pode ter no máximo 150 caracteres.")
        if len(d["telefone"]) not in (10, 11):
            self.errors.append("Digite um telefone válido com DDD.")

        # O bairro continua opcional para cliente; obrigatório para profissional.
        if self.tipo == "profissional":
            if d["id_bairro"] is None:
                self.errors.append("Escolha o bairro onde você atende.")
            if d["id_categoria"] is None:
                self.errors.append("Escolha a categoria do seu serviço.")
            if len(d["descricao"]) < 20:
                self.errors.append("A descrição precisa ter pelo menos 20 caracteres.")

    def salvar(self, id_usuario):
        """Só chame depois de validate() não ter encontrado erros."""
        dao = UsuarioDAO()
        d = self.data

        if self.tipo == "cliente":
            ok = dao.atualizar_cliente(id_usuario, d["nome"], d["telefone"], d["id_bairro"])
        else:
            ok = dao.atualizar_profissional(
                id_usuario, d["nome"], d["telefone"], d["id_bairro"], d["id_categoria"], d["descricao"]
            )

        if not ok:
            self.errors.append("Não foi possível salvar as alterações. Tente novamente.")
        return ok
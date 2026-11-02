import re
from werkzeug.security import generate_password_hash, check_password_hash

from dao.usuario_dao import UsuarioDAO


class Usuario:
    def __init__(self, form):
        """form: os dados que vieram do formulário (request.form)."""
        self.errors = []
        self.data = {
            "tipo": form.get("tipo", ""),
            "nome": form.get("nome", "").strip(),
            "email": form.get("email", "").strip().lower(),
            "telefone": re.sub(r"\D", "", form.get("telefone", "")),  # fica só com números
            "senha": form.get("senha", ""),
            "confirmar": form.get("confirmar_senha", ""),
            "endereco": form.get("endereco_referencia", "").strip(),
            "categoria": form.get("categoria", "").strip(),
            "descricao": form.get("descricao", "").strip(),
        }

    def validate(self):
        """Confere as regras do cadastro. Se algo estiver errado,
        coloca as mensagens em self.errors (lista vazia = tudo certo)."""
        d = self.data

        if not d["nome"] or not d["email"] or not d["telefone"]:
            self.errors.append("Preencha todos os campos obrigatórios.")
        if len(d["nome"]) > 150 or len(d["email"]) > 150:
            self.errors.append("Nome e e-mail podem ter no máximo 150 caracteres.")
        if d["email"] and ("@" not in d["email"] or "." not in d["email"]):
            self.errors.append("Digite um e-mail válido.")
        if d["telefone"] and len(d["telefone"]) not in (10, 11):
            self.errors.append("Digite um telefone válido com DDD.")
        if len(d["senha"]) < 8:
            self.errors.append("A senha precisa ter pelo menos 8 caracteres.")
        if d["senha"] != d["confirmar"]:
            self.errors.append("As senhas não coincidem.")
        if d["tipo"] not in ("cliente", "profissional"):
            self.errors.append("Escolha o tipo de conta.")

        if d["tipo"] == "profissional":
            if not d["categoria"] or len(d["descricao"]) < 20 or not d["endereco"]:
                self.errors.append(
                    "Preencha categoria, região e descrição dos serviços (mín. 20 caracteres)."
                )

    def save(self):
        """Salva a conta no banco. Retorna o id do novo usuário, ou None se falhar
        (nesse caso o motivo fica em self.errors)."""
        dao = UsuarioDAO()

        if dao.buscar_por_email(self.data["email"]) is not None:
            self.errors.append("Este e-mail já está cadastrado.")
            return None

        dados = dict(self.data)
        dados["senha_hash"] = generate_password_hash(self.data["senha"])

        if self.data["tipo"] == "cliente":
            id_usuario = dao.criar_cliente(dados)
        else:
            id_usuario = dao.criar_profissional(dados)

        if id_usuario is None:
            self.errors.append("Não foi possível criar a conta. Tente novamente.")
        return id_usuario

    @staticmethod
    def autenticar(email, senha):
        """Retorna os dados do usuário se o login estiver correto, senão None."""
        dao = UsuarioDAO()
        usuario = dao.buscar_por_email(email.strip().lower())

        if usuario is None:
            return None
        if usuario["status"] != "ativo":
            return None
        if not check_password_hash(usuario["senha_hash"], senha):
            return None
        return usuario

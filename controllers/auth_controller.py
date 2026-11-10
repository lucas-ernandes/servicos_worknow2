from flask import render_template, request, redirect, url_for, flash, session

from model.usuario_model import Usuario
from model.bairro import Bairro
from model.categoria import Categoria


def _iniciar_sessao(id_usuario, tipo, nome):
    session.clear()
    session["usuario_id"] = id_usuario
    session["tipo"] = tipo
    session["nome"] = nome

"""Mostra a página de cadastro já com as listas para as caixas de seleção.
    É chamada tanto no primeiro acesso quanto quando o formulário volta com erro. """
def _mostrar_cadastro():
    return render_template(
        "auth/cadastro.html",
        bairros=Bairro.listar(),
        categorias=Categoria.listar(),
    )

def cadastro():
    if request.method == "POST":
        usuario = Usuario(request.form)
        usuario.validate()

        if len(usuario.errors) == 0:
            id_usuario = usuario.save()
            if id_usuario is not None:
                # cadastrou: já deixa a pessoa logada e manda para a tela principal
                _iniciar_sessao(id_usuario, usuario.data["tipo"], usuario.data["nome"])
                flash("Conta criada com sucesso!", "success")
                return redirect(url_for("inicio"))

        for erro in usuario.errors:
            flash(erro, "error")
    
    return _mostrar_cadastro()


def login():
    if request.method == "POST":
        usuario = Usuario.autenticar(
            request.form.get("email", ""),
            request.form.get("senha", ""),
        )
        if usuario is None:
            flash("E-mail ou senha incorretos.", "error")
        else:
            _iniciar_sessao(usuario["id_usuario"], usuario["tipo_usuario"], usuario["nome"])
            return redirect(url_for("inicio"))

    return render_template("auth/login.html")


def logout():
    session.clear()
    return redirect(url_for("inicio"))
from flask import render_template, request, redirect, url_for, flash, session

from model.usuario_model import Usuario

def _iniciar_sessao(id_usuario, tipo, nome):
    session.clear()
    session["usuario_id"] = id_usuario
    session["tipo"] = tipo
    session["nome"] = nome


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

    return render_template("auth/cadastro.html")


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
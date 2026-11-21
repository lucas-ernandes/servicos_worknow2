from flask import render_template, request, redirect, url_for, flash, session, abort

from dao.usuario_dao import UsuarioDAO
from model.perfil import Perfil
from model.foto import Foto
from model.bairro import Bairro
from model.categoria import Categoria


def editar():
    if not session.get("usuario_id"):
        abort(403)

    tipo = session["tipo"]
    dao = UsuarioDAO()

    if request.method == "POST":
        perfil = Perfil(tipo, request.form)
        perfil.validate()

        if len(perfil.errors) == 0 and perfil.salvar(session["usuario_id"]):
            session["nome"] = perfil.data["nome"]  # atualiza o "Olá, Nome" do menu
            flash("Perfil atualizado com sucesso!", "success")
            return redirect(url_for("editar_perfil"))

        for erro in perfil.errors:
            flash(erro, "error")

    # GET, ou POST com erro: busca os dados atuais pra mostrar na tela
    if tipo == "cliente":
        dados = dao.buscar_perfil_cliente(session["usuario_id"])
    else:
        dados = dao.buscar_perfil_profissional(session["usuario_id"])

    return render_template(
        "perfil/editar.html",
        dados=dados,
        tipo=tipo,
        bairros=Bairro.listar(),
        categorias=Categoria.listar(),
    )
    

def foto():
    """Rota só da foto: troca na hora, sem precisar clicar em "Editar"/"Salvar"."""
    if not session.get("usuario_id"):
        abort(403)

    arquivo = request.files.get("foto")
    if not arquivo or not arquivo.filename:
        flash("Escolha uma foto antes de enviar.", "error")
        return redirect(url_for("editar_perfil"))

    ok, resultado = Foto.salvar(session["usuario_id"], arquivo)
    flash("Foto atualizada com sucesso!" if ok else resultado, "success" if ok else "error")

    return redirect(url_for("editar_perfil"))

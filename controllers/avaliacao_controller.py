from flask import render_template, request, redirect, url_for, flash, session, abort

from dao.avalicao_dao import AvalicaoDAO
from dao.profissional_dao import ProfissionalDAO


def minhas():
    if session.get("tipo") != "profissional":
        abort(403)

    id_profissional = ProfissionalDAO().buscar_id_por_usuario(session["usuario_id"])
    avaliacoes = AvalicaoDAO().listar_do_profissional(id_profissional)
    return render_template("avaliacoes/minhas.html", avaliacoes=avaliacoes)


def responder(id_avaliacao):
    if session.get("tipo") != "profissional":
        abort(403)

    texto = request.form.get("resposta", "").strip()
    if len(texto) < 3:
        flash("Escreva uma resposta antes de enviar.", "error")
        return redirect(url_for("minhas_avaliacoes"))

    id_profissional = ProfissionalDAO().buscar_id_por_usuario(session["usuario_id"])
    if not AvalicaoDAO().responder(id_avaliacao, id_profissional, texto):
        flash("Não foi possível responder (a avaliação já tem resposta?).", "error")

    return redirect(url_for("minhas_avaliacoes"))

from flask import render_template, session
from model.bairro import Bairro
from model.categoria import Categoria
from model.profissional import Profissional


"""A busca da página inicial precisa das listas para montar 
as caixas de seleção"""
def inicio():
    # None se for cliente ou visitante (aí a barra de disponibilidade não aparece).
    disponivel = None
    if session.get("tipo") == "profissional":
        disponivel = Profissional.esta_disponivel(session['usuario_id'])

    return render_template(
        "index.html",
        bairros=Bairro.listar(),
        categorias=Categoria.listar(),
        disponivel=disponivel,
    )

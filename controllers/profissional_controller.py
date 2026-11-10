from flask import render_template, request, redirect, url_for, flash, session, abort

from model.profissional import Profissional
from model.bairro import Bairro
from model.categoria import Categoria


# request.args = o que vem na URL depois do "?"
# Ex: /profissionais?bairro=5&categoria=2  ->  bairro="5", categoria="2"
def listar():
    bairro = request.args.get("bairro", "")
    categoria = request.args.get("categoria", "")

    resultado = Profissional.buscar(bairro, categoria)
    
    return render_template(
        "profissionais/lista.html",
        bairros=Bairro.listar(), #para caixa de bairro
        categorias=Categoria.listar(), # para caixa de categoria
        resultado=resultado,
    )
    
def perfil(id_profissional):
    profissional = Profissional.obter(id_profissional)

    if profissional is None:
        abort(404)
        
    return render_template("profissionais/perfil.html", profissional=profissional)

def alternar_disponibilidade():
    #Só profissional logado pode mexer na propria disponibilidade
    if session.get('tipo') != 'profissional':
        abort(403) # 'proibido'
        
    ok = Profissional.definir_disponibilidade(
        session['usuario_id'],
        request.form.get('disponivel', ""),
    )
    
    if not ok:
        flash("Não foi possivel alterar sua disponibilidade.", "danger")
    return redirect(url_for('inicio'))
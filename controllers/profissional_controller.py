from flask import render_template, request, redirect, url_for, flash, session, abort

from model.profissional import Profissional
from model.bairro import Bairro
from model.categoria import Categoria
from dao.avalicao_dao import AvalicaoDAO
from model.cliente import Cliente


# request.args = o que vem na URL depois do "?"
# Ex: /profissionais?bairro=5&categoria=2  ->  bairro="5", categoria="2"
def listar():
    bairro = request.args.get("bairro")
    categoria = request.args.get("categoria", "")
    
    # Cliente logado, chegando sem ter escolhido nada ainda: usamos o bairro
    # salvo no cadastro dele, se tiver (lembrando que é opcional).
    veio_do_cliente = False
    if bairro is None and session.get('tipo') == 'cliente':
        id_bairro_cliente = Cliente.bairro_salvo(session['usuario_id'])
        if id_bairro_cliente is not None:
            bairro = str(id_bairro_cliente)
            veio_do_cliente = True

    bairro = bairro or "" # visitante/sem bairro salvo: continua "Todos os bairros"

    
    resultado = Profissional.buscar(bairro, categoria)
    
    return render_template(
        "profissionais/lista.html",
        bairros=Bairro.listar(), #para caixa de bairro
        categorias=Categoria.listar(), # para caixa de categoria
        resultado=resultado,
        bairro_selecionado=bairro,
        veio_do_cliente=veio_do_cliente,
    )
    
def perfil(id_profissional):
    profissional = Profissional.obter(id_profissional)

    if profissional is None:
        abort(404)
        
    avaliacoes = AvalicaoDAO().listar_do_profissional(id_profissional)
    return render_template(
        "profissionais/perfil.html",
        profissional=profissional,
        avaliacoes=avaliacoes,
    )

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
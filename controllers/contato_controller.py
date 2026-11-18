from flask import redirect, url_for, flash, session, request, render_template, abort
from model.contato import Contato
from model.avaliacao import Avaliacao
from model.util import para_inteiro

def iniciar():
    """Botão "Entrar em contato" do perfil. Cria o contato e já manda a
    pessoa para o WhatsApp do profissional."""
    if session.get("tipo") != "cliente":
        flash("Faça login como cliente para entrar em contato.", "error")
        return redirect(url_for("login"))

    id_profissional = para_inteiro(request.form.get("id_profissional", ""))
    if id_profissional is None:
        abort(404)

    link = Contato.iniciar(session["usuario_id"], id_profissional)
    if link is None:
        abort(404)

    return redirect(link)

def meus_contatos():
    if session.get("tipo") != 'cliente':
        abort(403)
    contatos = Contato.listar_do_cliente(session['usuario_id'])
    return render_template('contatos/meus_contatos.html', contatos=contatos)

def concluir(id_contato):
    if session.get('tipo') != 'cliente':
        abort(403)
    
    if not Contato.concluir(id_contato, session['usuario_id']):
        flash('Não foi possivel concluir este contato.', "danger")
    return redirect(url_for('meus_contatos'))

def avaliar(id_contato):
    if session.get("tipo") != "cliente":
        abort(403)

    contato = Contato.obter_avaliavel(id_contato, session["usuario_id"])
    if contato is None:
        abort(404)

    if request.method == "POST":
        avaliacao = Avaliacao(request.form)
        avaliacao.validate()

        if len(avaliacao.errors) == 0:
            ok = avaliacao.salvar(id_contato, session["usuario_id"], contato["id_profissional"])
            if ok:
                flash("Avaliação registrada. Obrigado!", "success")
                return redirect(url_for("meus_contatos"))
        
        for erro in avaliacao.errors:
            flash(erro, 'danger')
    return render_template('contatos/avaliar.html', contato=contato)
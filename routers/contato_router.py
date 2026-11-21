from flask import Flask
from controllers import contato_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(
        "/contato",
        endpoint="iniciar_contato",
        view_func=contato_controller.iniciar,
        methods=["POST"]
    )
    
    app.add_url_rule(
        "/meus-contatos",
        endpoint="meus_contatos",
        view_func=contato_controller.meus_contatos,
        methods=["GET"]
    )
    
    app.add_url_rule(
        "/contato/<int:id_contato>/concluir",
        endpoint="concluir_contato",
        view_func=contato_controller.concluir,
        methods=["POST"]
    )
    
    app.add_url_rule(
        "/contato/<int:id_contato>/avaliar",
        endpoint="avaliar",
        view_func=contato_controller.avaliar,
        methods=["GET", "POST"]
    )
    
    app.add_url_rule(
        "/contato/<int:id_contato>/remover",
        endpoint='remover_contato',
        view_func=contato_controller.remover, 
        methods=["POST"]
    )

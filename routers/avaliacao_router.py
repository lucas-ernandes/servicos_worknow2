from flask import Flask
from controllers import avaliacao_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(
        '/minhas-avaliacoes',
        endpoint="minhas_avaliacoes",
        view_func=avaliacao_controller.minhas,
        methods=["GET"]
    )
    
    app.add_url_rule(
        '/avaliacao/<int:id_avaliacao>/responder',
        endpoint='responder_avaliacao',
        view_func=avaliacao_controller.responder,
        methods=['POST']
    )
        
    
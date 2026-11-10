from flask import Flask
from controllers import profissional_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(
        "/profissionais",
        endpoint="profissionais",
        view_func=profissional_controller.listar,
        methods=["GET"],
    )
    
    # <int:id_profissional> = parte variável da URL. Ex: /profissionais/7
    # O "int:" só aceita número (se digitarem /profissionais/abc, dá "não encontrado").
    app.add_url_rule(
        "/profissionais/<int:id_profissional>",
        endpoint="perfil",
        view_func=profissional_controller.perfil,
        methods=["GET"],
    )
    
    
    app.add_url_rule(
        "/disponibilidade",
        endpoint='alternar_disponibilidade',
        view_func=profissional_controller.alternar_disponibilidade,
        methods=["POST"]
    )
from flask import Flask
from controllers import perfil_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(
        '/meu_perfil',
        endpoint='editar_perfil',
        view_func=perfil_controller.editar, methods=['GET', 'POST'],
    )
    
    app.add_url_rule(
        "/meu-perfil/foto",
        endpoint="atualizar_foto",
        view_func=perfil_controller.foto,
        methods=["POST"],
    )

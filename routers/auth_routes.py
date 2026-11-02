from flask import Flask
from controllers import auth_controller


def adionar_rotas(app: Flask):
    app.add_url_rule(
        "/cadastro",
        endpoint="cadastro",
        view_func=auth_controller.cadastro,
        methods=["GET", "POST"],
    )
    
    app.add_url_rule(
        "/login",
        endpoint="login",
        view_func=auth_controller.login,
        methods=["GET", "POST"],
    )
    
    app.add_url_rule(
        "/logout",
        endpoint="logout",
        view_func=auth_controller.logout,
        methods=["GET"]
    )
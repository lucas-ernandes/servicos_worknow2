import os 
from flask import Flask
from database.sqlitedb import SQLiteDB
from routers import main_routes, auth_routes

app = Flask(__name__)
# Em produção, defina SECRET_KEY como variável de ambiente (valor grande e aleatório)
app.secret_key = os.environ.get("SECRET_KEY", "chave_teste_desenvolvimento_1234")

# Cria as tabelas se ainda não existirem
db = SQLiteDB()
db.conectar()
db.executar_script_sql("criar_tabelas.sql")
db.desconectar()

# Registar as rotas
main_routes.adicionar_rotas(app)
auth_routes.adionar_rotas(app)

if __name__ == "__main__":
    app.run(debug=True)
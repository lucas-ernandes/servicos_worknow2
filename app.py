from flask import Flask, render_template

app = Flask(__name__)

def inicio():
    return render_template('index.html')

app.add_url_rule(rule="/", view_func=inicio, methods=["GET"])

if __name__ == '__main__':
    app.run(debug=True)
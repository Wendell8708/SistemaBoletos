from flask import Flask
from routes.fornecedores import fornecedores_bp
from routes.boletos import boletos_bp
from routes.orcamentos import orcamentos_bp
from routes.notas import notas_bp
from routes.relatorios import relatorios_bp
from flask import render_template

from flask import render_template
app = Flask(__name__)


# Registrar blueprint de relatórios
app.register_blueprint(relatorios_bp, url_prefix="/relatorios")


# Registrar blueprint de notas fiscais
app.register_blueprint(notas_bp, url_prefix="/notas")

# Registrar blueprint de orçamentos
app.register_blueprint(orcamentos_bp, url_prefix="/orcamentos")



# Registrar blueprints
app.register_blueprint(fornecedores_bp, url_prefix="/fornecedores")
app.register_blueprint(boletos_bp, url_prefix="/boletos")


@app.route("/")
def index():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)

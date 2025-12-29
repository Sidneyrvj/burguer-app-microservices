from flask import Flask, session
from controllers.auth_controller import auth_bp
from dotenv import load_dotenv
from flask import redirect, url_for

import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria a instância da aplicação Flask
app = Flask(__name__)

secret_key = os.getenv("SECRET_KEY")

print(f"SECRET_KEY carregada: {secret_key}")  # DEBUG: deve imprimir o valor correto



#Define a chave secreta para a sessão
app.secret_key = os.getenv("SECRET_KEY")


# Registra o blueprint de autenticação
app.register_blueprint(auth_bp, url_prefix='/auth')

# Redireciona a rota raiz para a página de login
@app.route('/')
def index():
    return redirect(url_for('auth.login_page'))

if __name__ == '__main__':
    # Executa a aplicação Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
    # O debug=True permite recarregar automaticamente a aplicação ao fazer alterações no código
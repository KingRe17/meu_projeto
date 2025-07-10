from flask import Flask
from app.auth import auth_bp
from .db import init_db


def criar_app():
    app = Flask(__name__)
    init_db()  # cria o banco se não existir

    from app.rotas import tarefas_bp # Importa o "blueprint tarefas_bp" (grupo de rotas) do arquivo rotas.py.
    app.register_blueprint(tarefas_bp) # Registra esse blueprint no app.
    app.register_blueprint(auth_bp)

    return app

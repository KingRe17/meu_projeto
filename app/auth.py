from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from .db import sqlite3
import jwt
import datetime
import os
import json
from dotenv import load_dotenv
load_dotenv()


auth_bp = Blueprint('auth', __name__)
SEGREDO = os.getenv('SEGREDO')
TEMPO_EXPIRACAO = int(os.getenv('JWT_EXPIRA_EM', 3600))


# Rota de login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('app/data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and check_password_hash(result[0], password):
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=TEMPO_EXPIRACAO)
        }
        token = jwt.encode(payload, SEGREDO, algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Credenciais inválidas."}), 401

# Rota de registro
@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    senha_hash = generate_password_hash(password)

    conn = sqlite3.connect('app/data.db')
    cursor = conn.cursor()

    try:
        
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, senha_hash))
        conn.commit()
        return jsonify({"message": "Usuário registrado com sucesso."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Usuário já existe."}), 400
    finally:
        conn.close()

# Função que valida o token JWT
def verificar_token(token):
    try:
        payload = jwt.decode(token, SEGREDO, algorithms=["HS256"])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

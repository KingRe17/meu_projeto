from flask import Blueprint, jsonify, request
import json
import os
from app.auth import verificar_token

tarefas_bp = Blueprint('tarefas', __name__)

# Gera o caminho do arquivo tarefas.json, que está na mesma pasta. Isso garante que vai funcionar mesmo se rodar o projeto de outra pasta.
ARQUIVO = os.path.join(os.path.dirname(__file__), 'tarefas.json')

def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []

def salvar_tarefas():
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, indent=2, ensure_ascii=False) # indent=2 deixa o arquivo bonito / ensure_ascii=False permite acentos e caracteres especiais



tarefas = carregar_tarefas()



@tarefas_bp.route('/tarefas', methods=['GET']) # Quando alguem acessar /tarefas no site usando o metodo GET.
def listar_tarefas():
    usuario = verificar_token(request.headers.get('Authorization'))
    if not usuario:
      return jsonify({'erro': 'Token inválido ou ausente'}), 401

    return jsonify(tarefas)

@tarefas_bp.route('/tarefas', methods=['POST'])
def adicionar_tarefa():
    usuario = verificar_token(request.headers.get('Authorization'))
    if not usuario:
      return jsonify({'erro': 'Token inválido ou ausente'}), 401

    nova = request.json
    
    # if tarefas else 1 = se tem lista = id+1 / se lista estiver vazia coloque 1 no id.
    # em python, lista cheia = true, lista vazia = false.
    # tarefas[-1]['id'] = obtem o ultimo id da lista.
    nova['id'] = (tarefas[-1]['id'] + 1) if tarefas else 1
    if 'feito' not in nova:
        nova['feito'] = False
    tarefas.append(nova)
    salvar_tarefas()
    return jsonify(nova), 201

@tarefas_bp.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    usuario = verificar_token(request.headers.get('Authorization'))
    if not usuario:
      return jsonify({'erro': 'Token inválido ou ausente'}), 401
    
    dados = request.json
    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefa['titulo'] = dados.get('titulo', tarefa['titulo']) # adiciona o: 'titulo', se nao tiver nada mantem o: tarefa['titulo']
            tarefa['feito'] = dados.get('feito', tarefa['feito'])
            salvar_tarefas()
            return jsonify(tarefa)
    return jsonify({'erro': 'Tarefa não encontrada'}), 404

@tarefas_bp.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    usuario = verificar_token(request.headers.get('Authorization'))
    if not usuario:
      return jsonify({'erro': 'Token inválido ou ausente'}), 401

    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefas.remove(tarefa)
            salvar_tarefas()
            return jsonify({'mensagem': 'Tarefa deletada com sucesso'})
    return jsonify({'erro': 'Tarefa não encontrada'}), 404

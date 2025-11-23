from flask import Flask, jsonify

app = Flask(__name__)

#dados mockados para simular um banco de dados
USUARIOS_MOCK = [
    {"id": 1, "nome": "Lari", "status": "ativo", "registro": "2023-01-15"},
    {"id": 2, "nome": "Joao", "status": "ativo", "registro": "2023-03-20"},
    {"id": 3, "nome": "Maria", "status": "inativo", "registro": "2024-05-10"},
]

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """Endpoint que retorna a lista completa de usuários."""
    return jsonify(USUARIOS_MOCK)

if __name__ == '__main__':
    #rodar na porta 5000, padrão para flask
    app.run(host='0.0.0.0', port=5000)
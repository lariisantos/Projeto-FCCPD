from flask import Flask, jsonify

app = Flask(__name__)

USUARIOS = [
    {"id": 1, "nome": "Lari", "cidade": "Recife"},
    {"id": 2, "nome": "Joao", "cidade": "São Paulo"},
]

@app.route('/api/users', methods=['GET'])
def listar_usuarios():
    return jsonify(USUARIOS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
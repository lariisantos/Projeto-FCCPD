import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

#o endereço do serviço A será injetado via variável de ambiente (do docker-compose)
SERVICE_A_URL = os.environ.get('SERVICE_A_URL', 'http://service-a:5000/usuarios')

@app.route('/info', methods=['GET'])
def obter_informacoes():
    """Consome o Serviço A e formata a resposta."""
    try:
        #faz a requisição HTTP para o serviço A usando o hostname interno 'service-a'
        response = requests.get(SERVICE_A_URL)
        response.raise_for_status()  #levanta erro para códigos HTTP 4xx/5xx
        
        usuarios = response.json()
        
        output = []
        for user in usuarios:
            status = "Ativo" if user['status'] == 'ativo' else "Inativo"
            #formato da saída: "usuário X ativo desde..."
            info = f"Usuário {user['nome']} | Status: {status} | Registrado em: {user['registro']}"
            output.append(info)
            
        return jsonify({
            "status": "sucesso",
            "dados_consumidos": output,
            "servico_fonte": SERVICE_A_URL
        })
        
    except requests.exceptions.ConnectionError:
        return jsonify({"status": "erro", "mensagem": "Falha na comunicação com o Serviço A."}), 503
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    #rodar na porta 5001 para não conflitar com serviço A
    app.run(host='0.0.0.0', port=5001)
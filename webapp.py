import sys
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente primeiro
load_dotenv()

# --- CORREÇÃO DE CAMINHO PARA RENDER ---
# Define a raiz do projeto como a pasta onde este script está
project_root = os.path.dirname(os.path.abspath(__file__))
# Adiciona a pasta 'src' ao caminho do Python
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)
# --- FIM DA CORREÇÃO ---

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import threading
from werkzeug.utils import secure_filename
import yaml
import uuid

# Importa os módulos a partir da pasta 'src'
from config.config_manager import ConfigManager
from agents.user_agent import UserAgent
from process_knowledge import reindex_knowledge_base

# --- INICIALIZAÇÃO CORRIGIDA DO FLASK ---
# Diz ao Flask para procurar a pasta 'templates' na raiz do projeto
app = Flask(__name__,
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))
# --- FIM DA CORREÇÃO ---

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'uma-chave-secreta-muito-segura')

config_manager = ConfigManager(config_paths=[os.path.join(project_root, 'config', 'default.yaml')])
config = config_manager.get_all()

print("Inicializando o Agente Kaleb...")
user_agent = UserAgent("KalebWebApp", config)
print("Agente Kaleb pronto!")

chat_histories = {}

# --- ROTAS ---
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    current_config = config_manager.get_all()
    kb_path = os.path.join(project_root, current_config.get('knowledge_base', {}).get('path', 'knowledge_base'))
    os.makedirs(kb_path, exist_ok=True)
    if request.method == 'POST':
        # ... (lógica dos formulários)
        return redirect(url_for('dashboard'))
    knowledge_files = os.listdir(kb_path)
    return render_template('dashboard.html', config=current_config, knowledge_files=knowledge_files)

@app.route('/ask_kaleb', methods=['POST'])
def ask_kaleb():
    # ... (código do chat)
    return jsonify({'response': '...'})

# --- BLOCO PRINCIPAL ---
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5001)
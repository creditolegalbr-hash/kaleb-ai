import sys
import os
from dotenv import load_dotenv

load_dotenv()

project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import threading
from werkzeug.utils import secure_filename
import yaml
import uuid

from config.config_manager import ConfigManager
from agents.user_agent import UserAgent
from process_knowledge import reindex_knowledge_base

# --- INICIALIZAÇÃO CORRIGIDA DO FLASK ---
# Diz ao Flask para procurar as pastas a partir da pasta 'src'
app = Flask(__name__,
            template_folder=os.path.join(project_root, 'src', 'templates'),
            static_folder=os.path.join(project_root, 'static'))
# --- FIM DA CORREÇÃO ---

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'uma-chave-secreta-muito-segura')

# ... (o resto do seu código webapp.py continua exatamente o mesmo)
# ...
config_manager = ConfigManager(config_paths=[os.path.join(project_root, 'config', 'default.yaml')])
config = config_manager.get_all()
user_agent = UserAgent("KalebWebApp", config)
print("Agente Kaleb pronto!")

# ... (resto das rotas)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5001)
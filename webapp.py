import sys
import os

# --- CORREÇÃO FINAL PARA RENDER ---
# Adiciona a pasta 'src' ao caminho do Python para que ele encontre os módulos
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)
# --- FIM DA CORREÇÃO ---

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import threading
from werkzeug.utils import secure_filename
import yaml
import uuid
from waitress import serve

from config.config_manager import ConfigManager
from agents.user_agent import UserAgent
from process_knowledge import reindex_knowledge_base

app = Flask(__name__,
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'uma-chave-secreta-muito-segura')

# ... (o resto do seu código webapp.py, sem alterações)
# ...
config_manager = ConfigManager(config_paths=[os.path.join(project_root, 'config', 'default.yaml')])
config = config_manager.get_all()
user_agent = UserAgent("KalebWebApp", config)
print("Agente Kaleb pronto!")

# ... (resto das rotas, sem alterações)
# ...

if __name__ == '__main__':
    print("Iniciando em ambiente de desenvolvimento local (Waitress)...")
    from waitress import serve
    serve(app, host='0.0.0.0', port=5001)
import sys
import os
import subprocess
import threading
import queue
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, send_from_directory
from werkzeug.utils import secure_filename
import yaml
import uuid
from waitress import serve # Importa o servidor de produção

# --- INICIALIZAÇÃO CORRETA ---
load_dotenv()
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.config.config_manager import ConfigManager
from src.agents.user_agent import UserAgent
from src.process_knowledge import reindex_knowledge_base

app = Flask(__name__,
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'uma-chave-secreta-muito-segura')

# ... (resto da inicialização, sem mudanças)
config_manager = ConfigManager(config_paths=[os.path.join(project_root, 'config', 'default.yaml')])
config = config_manager.get_all()
user_agent = UserAgent("KalebWebApp", config)
print("Agente Kaleb pronto!")

whatsapp_status_queue = queue.Queue()
# ... (o resto do seu código webapp.py continua aqui, sem mudanças)
# ...

# --- BLOCO PRINCIPAL ATUALIZADO ---
if __name__ == '__main__':
    # No Render, ele usará gunicorn. Localmente, usaremos waitress.
    if os.environ.get('RENDER'):
        print("Iniciando em ambiente de produção (Render)...")
        # O Render vai usar o comando do gunicorn
    else:
        print("Iniciando em ambiente de desenvolvimento (Waitress)...")
        serve(app, host='0.0.0.0', port=5001)
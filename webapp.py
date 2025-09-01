import sys
import os
from dotenv import load_dotenv

load_dotenv()
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
# ... (outros imports)

from config.config_manager import ConfigManager
from agents.user_agent import UserAgent
from process_knowledge import reindex_knowledge_base

# --- INICIALIZAÇÃO CORRIGIDA DO FLASK ---
# Agora que 'templates' está na raiz, o Flask a encontra automaticamente.
# Mas vamos ser explícitos para garantir.
app = Flask(__name__,
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))
# --- FIM DA CORREÇÃO ---

# ... (o resto do seu código webapp.py continua exatamente o mesmo)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5001)
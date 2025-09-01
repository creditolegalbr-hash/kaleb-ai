import sys
import os
from dotenv import load_dotenv

load_dotenv()

# --- CAMINHOS ABSOLUTOS E EXPLÍCITOS ---
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
# ... (outros imports)

from config.config_manager import ConfigManager
from agents.user_agent import UserAgent
from process_knowledge import reindex_knowledge_base

# --- INICIALIZAÇÃO EXPLÍCITA DO FLASK ---
app = Flask(__name__,
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))
# --- FIM DA CORREÇÃO ---

# ... (o resto do seu código webapp.py continua exatamente o mesmo)
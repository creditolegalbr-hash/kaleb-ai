import sys
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- CORREÇÃO DE CAMINHO PARA RENDER ---
# Define a raiz do projeto como a pasta onde este script está
project_root = os.path.dirname(os.path.abspath(__file__))
# Adiciona a pasta 'src' ao caminho do Python para que ele encontre os módulos
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)
# --- FIM DA CORREÇÃO ---

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import threading
from werkzeug.utils import secure_filename
import yaml
import uuid

# Importa os módulos do seu projeto a partir da pasta 'src'
from config.config_manager import ConfigManager
from agents.user_agent import UserAgent
from process_knowledge import reindex_knowledge_base

# --- INICIALIZAÇÃO CORRIGIDA DO FLASK ---
# Diz ao Flask para procurar a pasta 'templates' a partir da raiz do projeto
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
        form_name = request.form.get('form_name')
        if form_name == 'config_form':
            config_data = config_manager.get_all()
            for key, value in request.form.items():
                if '.' in key:
                    section, setting = key.split('.', 1)
                    if section in config_data and setting in config_data[section]:
                        config_data[section][setting] = value
            with open(os.path.join(project_root, 'config', 'default.yaml'), 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            flash("Configurações salvas!", "success")
        elif form_name == 'kb_form' and 'knowledge_file' in request.files:
            file = request.files['knowledge_file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(kb_path, filename))
                flash(f"Arquivo '{filename}' carregado. Reindexação iniciada.", "info")
                threading.Thread(target=reindex_knowledge_base, daemon=True).start()
        return redirect(url_for('dashboard'))
    knowledge_files = os.listdir(kb_path)
    return render_template('dashboard.html', config=current_config, knowledge_files=knowledge_files)

@app.route('/ask_kaleb', methods=['POST'])
def ask_kaleb():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    user_id = session['user_id']
    current_history = chat_histories.setdefault(user_id, [])
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Mensagem vazia.'}), 400
    current_history.append({'role': 'user', 'parts': [user_message]})
    kaleb_response_data = user_agent.perform_intelligent_task_with_memory(user_message, current_history)
    kaleb_response_text = kaleb_response_data.get('result', 'Ocorreu um erro.')
    current_history.append({'role': 'model', 'parts': [kaleb_response_text]})
    chat_histories[user_id] = current_history[-10:]
    return jsonify({'response': kaleb_response_text})

# --- BLOCO PRINCIPAL PARA EXECUÇÃO ---
if __name__ == '__main__':
    # Este bloco só roda quando você executa 'python webapp.py' no seu PC.
    # O Render usa o Gunicorn e não executa esta parte.
    print("Iniciando em ambiente de desenvolvimento local (Waitress)...")
    from waitress import serve
    serve(app, host='0.0.0.0', port=5001)
import os
import sys
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.agents.base_agent import BaseAgent
from src.knowledge_retriever import KnowledgeRetriever
from src.agents.whatsapp_agent import WhatsAppAgent
import google.generativeai as genai

class UserAgent(BaseAgent):
    def __init__(self, name: str, config: dict):
        super().__init__(name) 
        self.config = config
        
        # --- OTIMIZAÇÃO: CARREGAMENTO PREGUIÇOSO ATIVADO ---
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        # Passamos lazy_load=True para que os modelos pesados não sejam carregados na inicialização
        self.knowledge_retriever = KnowledgeRetriever(project_root=project_root, lazy_load=True)
        # --- FIM DA OTIMIZAÇÃO ---

        self.whatsapp_agent = WhatsAppAgent("WhatsAppWorker")
        
        try:
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key: raise ValueError("Chave de API do Google não encontrada")
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            print("Cliente Google Gemini inicializado com sucesso.")
        except Exception as e:
            print(f"ERRO: Não foi possível inicializar o cliente Gemini. {e}")
            self.gemini_model = None

    def perform_intelligent_task_with_memory(self, task_description: str, history: list) -> dict:
        self.logger.info(f"Processando tarefa: '{task_description}'")
        
        # O modelo de IA agora será carregado aqui, na primeira busca, e não na inicialização
        context_from_kb = self.knowledge_retriever.search(task_description)
        
        task_type = self._route_task(task_description)
        return self.perform_task_with_memory(task_type, task_description, context_from_kb, history)

    # ... (O resto do seu UserAgent - perform_task_with_memory, _route_task - continua exatamente igual)
    def perform_task_with_memory(self, task_type: str, task_description: str, context_from_kb: list, history: list) -> dict:
        # ... (sem mudanças aqui)
        return {'success': True, 'result': '...'}
    def _route_task(self, description: str) -> str:
        # ... (sem mudanças aqui)
        return 'knowledge_qa'
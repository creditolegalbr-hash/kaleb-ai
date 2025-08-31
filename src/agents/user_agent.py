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
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.knowledge_retriever = KnowledgeRetriever(project_root=project_root)
        self.whatsapp_agent = WhatsAppAgent("WhatsAppWorker")
        try:
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key: raise ValueError("Chave de API do Google nao encontrada")
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            print("Cliente Google Gemini inicializado com sucesso.")
        except Exception as e:
            print(f"ERRO: Nao foi possivel inicializar o cliente Gemini. {e}")
            self.gemini_model = None

    def _route_task(self, description: str) -> str:
        description_lower = description.lower()
        whatsapp_pattern = r"(envie|mande|enviar)\s+(uma\s+)?(mensagem|zap|whatsapp)\s+para\s+([^,]+?)\s+(dizendo|com\s+a\s+mensagem|que)\s+(.+)"
        if re.search(whatsapp_pattern, description_lower):
            return "whatsapp"
        return "knowledge_qa" 

    def perform_intelligent_task_with_memory(self, task_description: str, history: list) -> dict:
        self.logger.info(f"Processando tarefa: '{task_description}'")
        task_type = self._route_task(task_description)
        context_from_kb = self.knowledge_retriever.search(task_description)
        return self.perform_task_with_memory(task_type, task_description, context_from_kb, history)

    def perform_task_with_memory(self, task_type: str, task_description: str, context_from_kb: list, history: list) -> dict:
        self.logger.info(f"Executando tarefa do tipo '{task_type}'")
        
        if task_type == "whatsapp":
            whatsapp_pattern = r"para\s+([^,]+?)\s+(?:dizendo|com\s+a\s+mensagem|que)\s+(.+)"
            match = re.search(whatsapp_pattern, task_description, re.IGNORECASE)
            if match:
                contact = match.group(1).strip()
                message = match.group(2).strip()
                success = self.whatsapp_agent.send_message(contact, message)
                if success:
                    return {'success': True, 'result': f"Pronto! A mensagem foi enviada para {contact}."}
                else:
                    return {'success': False, 'result': f"Desculpe, ocorreu uma falha ao enviar a mensagem para {contact}."}
            else:
                return {'success': False, 'result': "Nao entendi. Use o formato: 'envie mensagem para [NOME] dizendo [MENSAGEM]'"}
        
        elif task_type == "knowledge_qa":
            if not self.gemini_model: return {'success': False, 'result': "O cliente Gemini nao esta configurado."}
            try:
                context_text = "\n".join([item['text'] for item in context_from_kb]) if context_from_kb else "Nenhuma informacao de contexto encontrada."
                system_prompt = f"""Voce e Kaleb, um especialista em credito e assistente de vendas do Grupo Volare. Sua missao e atender os clientes de forma empatica, profissional e persuasiva, guiando-os para o proximo passo.
                **Regras:**
                1.  **Empatia Primeiro:** Reconheca a situacao do cliente.
                2.  **Seja um Especialista:** Use o 'Contexto' para responder de forma clara.
                3.  **Foco na Solucao:** Enquadre a conversa nos beneficios que o Grupo Volare oferece.
                4.  **Sempre Guie para a Proxima Etapa:** Termine com uma pergunta aberta (Call to Action). Ex: "Isso faz sentido para voce?", "Podemos comecar com uma analise gratuita?".
                5.  **Use o Historico:** Preste atencao ao 'Historico da Conversa' para nao se repetir.
                6.  **Honestidade:** Se a informacao nao estiver no contexto, seja honesto e ofereca ajuda.
                **Contexto da Base de Conhecimento:**
                ---
                {context_text}
                ---
                """
                messages_for_gemini = [{'role': 'user', 'parts': [system_prompt]}, {'role': 'model', 'parts': ["Entendido. Estou pronto para ajudar o cliente."]} ]
                messages_for_gemini.extend(history)
                response = self.gemini_model.generate_content(messages_for_gemini)
                return {'success': True, 'result': response.text}
            except Exception as e:
                return {'success': False, 'result': f"Ocorreu um erro ao gerar a resposta: {e}"}
        return {'success': True, 'result': f"Tarefa simulada de '{task_type}'."}
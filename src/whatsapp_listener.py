import requests
import time
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agents.user_agent import UserAgent
from src.config.config_manager import ConfigManager

# Carrega as variáveis de ambiente (como a chave do Google) do arquivo .env
load_dotenv()

def listen_for_messages(user_agent, base_url="http://localhost:3000", session_name="kaleb-session"):
    """Fica em um loop infinito, verificando por novas mensagens não lidas."""
    print("👂 Ouvindo por novas mensagens do WhatsApp...")
    # Este endpoint do WA-JS é melhor, pois pega apenas mensagens não lidas
    url = f"{base_url}/{session_name}/get-unread-messages"
    
    while True:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                unread_chats = response.json().get('data', [])
                for chat in unread_chats:
                    # Pega apenas a última mensagem não lida do chat
                    if chat.get('messages'):
                        sender_number = chat['id'].replace('@c.us', '')
                        last_message = chat['messages'][-1]['body']
                        print(f"\n📩 Nova mensagem de {sender_number}: '{last_message}'")
                        
                        # Passa a mensagem para o UserAgent lidar
                        user_agent.handle_whatsapp_message(sender_number, last_message)
            
            time.sleep(5) # Verifica a cada 5 segundos
        except requests.exceptions.RequestException:
            # Silencioso, apenas tenta novamente. O servidor WA-JS pode estar reiniciando.
            time.sleep(10)
        except Exception as e:
            print(f"Ocorreu um erro no listener: {e}")
            time.sleep(10)

if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_file_path = os.path.join(project_root, 'config', 'default.yaml')
    config_manager = ConfigManager(config_paths=[config_file_path])
    config = config_manager.get_all()
    
    print("Inicializando o Agente Kaleb para o WhatsApp...")
    kaleb_agent = UserAgent("KalebWhatsAppListener", config)
    
    listen_for_messages(kaleb_agent)
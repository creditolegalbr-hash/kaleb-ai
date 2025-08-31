import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.agents.base_agent import BaseAgent

class WhatsAppAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)

    def _get_driver(self):
        """Prepara e retorna um driver do Chrome com a sessão do usuário."""
        self.logger.info("Preparando o driver do Chrome com a sessão do WhatsApp...")
        chrome_options = Options()
        # Garante que o caminho da sessão seja absoluto a partir da raiz do projeto
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        session_path = os.path.join(project_root, "whatsapp_session")
        
        if not os.path.exists(session_path):
            self.logger.error(f"Pasta de sessão do WhatsApp não encontrada em '{session_path}'. Conecte-se primeiro.")
            return None
            
        chrome_options.add_argument(f"--user-data-dir={session_path}")
        # --- MELHORIA: RODA O NAVEGADOR DE FORMA INVISÍVEL ---
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        # --- FIM DA MELHORIA ---
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(120) # Aumenta a paciência para 2 minutos
        return driver

    def send_message(self, contact: str, message: str) -> bool:
        driver = self._get_driver()
        if not driver: return False
        try:
            driver.get("https://web.whatsapp.com/")
            wait = WebDriverWait(driver, 60)
            
            # Espera um elemento chave da página principal carregar
            wait.until(EC.presence_of_element_located((By.ID, "side")))
            self.logger.info("Página principal do WhatsApp carregada (modo invisível).")
            
            # Busca e clica no contato
            search_box_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, search_box_xpath)))
            search_box.send_keys(contact)
            time.sleep(2)
            
            contact_xpath = f'//span[contains(@title, "{contact}")]'
            contact_element = wait.until(EC.element_to_be_clickable((By.XPATH, contact_xpath)))
            contact_element.click()
            self.logger.info(f"Contato '{contact}' selecionado.")
            
            # Envia a mensagem
            message_box_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
            message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_xpath)))
            message_box.send_keys(message + Keys.ENTER)
            self.logger.info("Mensagem enviada.")
            
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.error(f"Falha ao enviar a mensagem: {e}", exc_info=True)
            return False
        finally:
            if driver:
                self.logger.info("Fechando o navegador de envio.")
                driver.quit()
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.agents.base_agent import BaseAgent

class WhatsAppAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)

    def _get_driver(self):
        # ... (código para obter o driver, igual ao que funcionou antes)
        self.logger.info("Preparando o driver do Chrome com a sessão do WhatsApp...")
        chrome_options = webdriver.ChromeOptions()
        session_path = os.path.join(os.getcwd(), "whatsapp_session")
        if not os.path.exists(session_path):
            self.logger.error("Pasta de sessão do WhatsApp não encontrada.")
            return None
        chrome_options.add_argument(f"--user-data-dir={session_path}")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def send_message(self, contact_name_or_number: str, message: str) -> bool:
        driver = self._get_driver()
        if not driver: return False
        try:
            driver.get("https://web.whatsapp.com/")
            wait = WebDriverWait(driver, 60)
            search_box_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, search_box_xpath)))
            search_box.send_keys(contact_name_or_number)
            time.sleep(2)
            contact_xpath = f'//span[@title="{contact_name_or_number}"]'
            contact_element = wait.until(EC.presence_of_element_located((By.XPATH, contact_xpath)))
            contact_element.click()
            message_box_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
            message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_xpath)))
            message_box.send_keys(message + Keys.ENTER)
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.error(f"Falha ao enviar a mensagem: {e}", exc_info=True)
            return False
        finally:
            if driver: driver.quit()
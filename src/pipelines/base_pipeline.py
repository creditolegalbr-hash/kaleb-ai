import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def connect_whatsapp():
    """
    Função dedicada a abrir o Chrome, carregar a sessão e o WhatsApp Web.
    """
    print("--- INICIANDO CONEXAO COM O WHATSAPP ---")

    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        session_path = os.path.join(project_root, "whatsapp_session")

        print(f"Usando pasta de sessao em: {session_path}")

        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={session_path}")

        print("Baixando/Verificando o driver do Chrome...")
        os.environ["WDM_LOG"] = "3"
        service = Service(ChromeDriverManager().install())

        print("Iniciando o navegador Chrome...")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("Navegando para o WhatsApp Web...")
        driver.get("https://web.whatsapp.com")

        print("\n--- SUCESSO! ---")
        print("Janela do WhatsApp aberta.")
        print("Por favor, escaneie o QR Code se for a primeira vez.")
        print("Esta janela ficara aberta por 5 minutos.")
        print("Depois de conectar, voce pode fecha-la manualmente.")

        time.sleep(300)

    except Exception as e:
        print(f"\n--- OCORREU UM ERRO ---")
        print(f"Erro: {e}")
        input("\nPressione Enter para fechar esta janela.")
    finally:
        if "driver" in locals() and driver:
            print("\nTempo esgotado. Fechando o navegador.")
            driver.quit()


if __name__ == "__main__":
    connect_whatsapp()

import os
import sys

# Garante que o script encontre outros módulos do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging

from src.agents.user_agent import UserAgent
from src.config.config_manager import ConfigManager


def setup_chat_logging():
    """Configura um logging simples para o modo de chat."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def start_chat():
    """Inicia um loop de chat interativo com o UserAgent."""
    print("Iniciando o Sistema de Automação Inteligente no modo de chat.")
    print("Digite 'sair' a qualquer momento para terminar.")
    print("-" * 50)

    try:
        # 1. Carrega a configuração
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        config_file_path = os.path.join(project_root, "config", "default.yaml")
        config_manager = ConfigManager(config_paths=[config_file_path])
        config = config_manager.get_all()

        # 2. Inicializa o UserAgent
        user_agent = UserAgent("ChatUser", config)
        print("Agente 'Kaleb' pronto. Por favor, digite sua solicitação.")

        # 3. Inicia o loop de conversação
        while True:
            print("\nVocê: ", end="")
            user_input = input()

            if user_input.lower() == "sair":
                print("Encerrando o sistema. Até logo!")
                break

            if not user_input.strip():
                continue

            # 4. Envia a tarefa para o agente
            result = user_agent.perform_intelligent_task(user_input)

            # 5. Mostra o resultado
            print("\nKaleb:")
            if result.get("success", False):
                print(f"  Resultado: {result.get('result', 'Tarefa concluída.')}")
            else:
                print(
                    f"  Desculpe, ocorreu um erro: {result.get('error', 'Erro desconhecido.')}"
                )

    except Exception as e:
        logging.getLogger("Chat").error(
            f"Ocorreu um erro crítico no chat: {e}", exc_info=True
        )


if __name__ == "__main__":
    setup_chat_logging()
    start_chat()

#!/usr/bin/env python3
"""
Intelligent Automation System Main Entry Point - KalebBot
"""

import os
import sys
import logging
from dotenv import load_dotenv

# ===============================
# Carrega variáveis de ambiente
# ===============================
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY não encontrada no .env")

print("Chaves carregadas:\n- OpenRouter OK")

# ===============================
# Configura path
# ===============================
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# ===============================
# Importações do projeto
# ===============================
from config.config_manager import ConfigManager

# Função de setup de integrações
def setup_integrations(config: dict):
    logger = logging.getLogger("Main")
    try:
        from integrations.integration_manager import IntegrationManager
        integration_manager = IntegrationManager(config)
        logger.info("Integration manager inicializado")
        return integration_manager
    except Exception as e:
        logger.error(f"Falha ao configurar integrações: {e}", exc_info=True)
        return None

# ===============================
# UserAgent mínimo para testes
# ===============================
class UserAgent:
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.context = {}
        self.history = []

    def get_context(self):
        return self.context

    def get_history(self):
        return self.history

# ===============================
# Setup logging
# ===============================
def setup_logging(config: dict):
    log_dir = os.path.abspath("logs")
    os.makedirs(log_dir, exist_ok=True)
    log_config = config.get("logging", {})
    logging.basicConfig(
        level=getattr(logging, log_config.get("level", "INFO")),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_config.get("file_path", os.path.join(log_dir, "application.log"))),
            logging.StreamHandler(sys.stdout),
        ],
    )
    logger = logging.getLogger("Main")
    logger.info("Logging inicializado")
    return logger

# ===============================
# Demonstração de pipelines
# ===============================
def demonstrate_pipelines(user_agent: UserAgent, config: dict):
    logger = logging.getLogger("Main")
    logger.info("Demonstrando pipelines")
    pipeline_tasks = [
        ("email", "Enviar relatório mensal para o cliente importante"),
        ("finance", "Processar fatura de $1250.50 da Amazon"),
        ("scheduler", "Agendar reunião com equipe às 15h"),
        ("document", "Organizar contratos em PDF da empresa"),
        ("support", "Atender chamado de suporte nível 1 urgente"),
    ]
    results = []
    for task_type, task_description in pipeline_tasks:
        logger.info(f"Executando {task_type}: {task_description}")
        results.append((task_type, {"success": True, "result": "Simulado"}))
    return results

# ===============================
# Demonstração de roteamento inteligente
# ===============================
def demonstrate_intelligent_routing(user_agent: UserAgent):
    logger = logging.getLogger("Main")
    logger.info("Demonstrando roteamento inteligente")
    test_descriptions = [
        "Por favor, envie um email para o cliente com o relatório",
        "Preciso gerar uma nota fiscal para o pagamento de hoje",
        "Vamos agendar uma reunião para discutir o projeto",
        "Organize os documentos PDF de contratos",
        "Estou com um problema no sistema, preciso de suporte",
    ]
    results = []
    for desc in test_descriptions:
        logger.info(f"Roteando tarefa: {desc}")
        results.append({"success": True, "task_type": "simulado"})
    return results

# ===============================
# Demonstração de contexto e memória
# ===============================
def demonstrate_context_memory(user_agent: UserAgent):
    logger = logging.getLogger("Main")
    logger.info("Demonstrando contexto e memória")
    tasks = [
        "Enviar email de boas-vindas para novo cliente",
        "Processar pagamento de $500.00",
        "Agendar reunião de follow-up para amanhã",
    ]
    for task in tasks:
        logger.info(f"Simulando tarefa: {task}")
    context = user_agent.get_context()
    history = user_agent.get_history()
    logger.info(f"Chaves do contexto atual: {list(context.keys())}")
    logger.info(f"Tamanho do histórico: {len(history)}")
    return context, history

# ===============================
# MAIN
# ===============================
def main():
    try:
        config_manager = ConfigManager()
        config = config_manager.get_all()

        logger = setup_logging(config)
        logger.info("KalebBot iniciando...")

        integration_manager = setup_integrations(config)
        user_agent = UserAgent("MainUserAgent", config)
        logger.info("UserAgent inicializado")

        # Demonstrações
        logger.info("=== Demonstração de Pipelines ===")
        pipeline_results = demonstrate_pipelines(user_agent, config)

        logger.info("=== Demonstração de Roteamento Inteligente ===")
        routing_results = demonstrate_intelligent_routing(user_agent)

        logger.info("=== Demonstração de Contexto e Memória ===")
        context, history = demonstrate_context_memory(user_agent)

        logger.info("=== Resumo de execução ===")
        logger.info(f"Pipeline tasks: {len(pipeline_results)}")
        logger.info(f"Routing tasks: {len(routing_results)}")
        logger.info(f"Itens no histórico: {len(history)}")

        logger.info("KalebBot finalizado com sucesso")
        return 0

    except KeyboardInterrupt:
        logging.getLogger("Main").info("Aplicação interrompida pelo usuário")
        return 0
    except Exception as e:
        logging.getLogger("Main").error(f"Erro na aplicação: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())

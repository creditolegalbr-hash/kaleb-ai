import os
import subprocess

def run_command(command: str):
    """Executa um comando no terminal e mostra a saída"""
    print(f"\n▶ Executando: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("⚠️ Erros/avisos:\n", result.stderr)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, "src")

    print("🚀 Iniciando correção automática do código...\n")

    # 1. Organizar imports
    run_command(f"isort {src_dir}")

    # 2. Formatar com Black
    run_command(f"black {src_dir}")

    # 3. Rodar análise de erros com Pylint
    run_command(f"pylint {src_dir}")

    print("\n✅ Finalizado! Seu código foi formatado e analisado.")

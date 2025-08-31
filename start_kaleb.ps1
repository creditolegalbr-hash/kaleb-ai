# ==================================================
# SCRIPT MESTRE PARA INICIAR O KALEB AI
# ==================================================

# --- ETAPA 1: CONFIGURAÇÃO ---
# Edite a linha abaixo com a sua chave de API do Google.
# IMPORTANTE: Coloque a chave real entre as aspas.
$env:GOOGLE_API_KEY="AIzaSyA4czp6qIxA4inOPNCUSSeFn4H9lMVZd_8"

# Define os caminhos para facilitar a manutenção
$projetoPath = "D:\projeto"
$ngrokPath = "D:\ngrok-v3-stable-windows-amd64"

# Mensagem de boas-vindas
Write-Host "🚀 Iniciando o Sistema Kaleb AI..." -ForegroundColor Green


# --- ETAPA 2: INICIAR O SERVIDOR KALEB EM SEGUNDO PLANO ---
Write-Host "   -> Ligando o servidor web do Kaleb..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projetoPath'; . .\venv\Scripts\Activate.ps1; python .\src\pipelines\webapp.py"


# --- ETAPA 3: INICIAR O NGROK EM SEGUNDO PLANO ---
# Pequena pausa para garantir que o servidor Flask tenha tempo de iniciar
Start-Sleep -Seconds 5

Write-Host "   -> Abrindo o túnel de rede com o ngrok..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ngrokPath'; .\ngrok.exe http 5001"


# --- ETAPA 4: MENSAGEM FINAL ---
Write-Host ""
Write-Host "✅ SUCESSO! O Kaleb está no ar." -ForegroundColor Green
Write-Host "   - O servidor do Kaleb e o túnel do ngrok estão rodando em novas janelas."
Write-Host "   - Para parar o sistema, feche as duas novas janelas do PowerShell que foram abertas."
Write-Host ""

# Mantém esta janela aberta por alguns segundos para você ler a mensagem
Start-Sleep -Seconds 10
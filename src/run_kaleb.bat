@echo off
title Kaleb AI - Automação Total
cd /d "%~dp0"

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Iniciando KalebBot...
start cmd /k "python src\main.py"

echo Iniciando ngrok para expor o painel...
start cmd /k "ngrok http 5000"

echo Aguardando ngrok gerar link...
timeout /t 5 > nul

:: Lê o link do ngrok automaticamente e abre no navegador
for /f "tokens=*" %%i in ('curl -s http://127.0.0.1:4040/api/tunnels ^| findstr /i "public_url"') do (
    for /f "tokens=2 delims=:" %%a in ("%%i") do (
        set NGROK_LINK=%%a
        set NGROK_LINK=!NGROK_LINK:~2,-1!
    )
)

echo Abrindo painel Kaleb no navegador...
start "" "!NGROK_LINK!"

echo Tudo pronto! KalebBot e painel rodando.
pause

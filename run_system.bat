@echo off
title Sistema de Automação Inteligente
echo ======================================================
echo   Sistema de Automação Inteligente - Inicializando
echo ======================================================
echo.

REM Navegar para o diretório do projeto
cd /d "C:\Users\ciami\OneDrive\Área de Trabalho\projeto"

REM Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python não encontrado!
    echo Por favor, instale o Python 3.7 ou superior.
    echo.
    pause
    exit /b 1
)

REM Verificar se o arquivo principal existe
if not exist "src\main.py" (
    echo ERRO: Arquivo principal não encontrado!
    echo Certifique-se de que o projeto está no diretório correto.
    echo.
    pause
    exit /b 1
)

echo Iniciando o sistema...
echo ======================================================
echo.

REM Executar o sistema
python src/main.py

echo.
echo ======================================================
echo   Sistema finalizado
echo ======================================================
pause
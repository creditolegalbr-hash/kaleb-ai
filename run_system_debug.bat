@echo off
title Sistema de Automação Inteligente - DEBUG
color 0A
echo ======================================================
echo   Sistema de Automação Inteligente - Modo DEBUG
echo ======================================================
echo.

REM Navegar para o diretório do projeto
cd /d "C:\Users\ciami\OneDrive\Área de Trabalho\projeto"

echo Diretório atual: %CD%
echo.

REM Verificar se estamos no diretório correto
if not exist "src\main.py" (
    echo ERRO: Arquivo src\main.py não encontrado!
    echo Diretório atual: %CD%
    echo Conteúdo do diretório:
    dir
    echo.
    pause
    exit /b 1
)

echo ✓ Arquivo src\main.py encontrado
echo.

REM Verificar se o Python está instalado
echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python não encontrado!
    echo Por favor, instale o Python 3.7 ou superior.
    echo Baixe em: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo Verificando dependências...
python test_yaml.py
echo.

echo ======================================================
echo   Iniciando o Sistema de Automação Inteligente
echo ======================================================
echo.
echo Pressione qualquer tecla para iniciar o sistema...
pause >nul

REM Executar o sistema com mais informações de erro
echo.
echo Executando: python src/main.py
echo.
python src/main.py

if %errorlevel% neq 0 (
    echo.
    echo ======================================================
    echo   ERRO: O sistema terminou com código de erro %errorlevel%
    echo ======================================================
) else (
    echo.
    echo ======================================================
    echo   Sistema executado com sucesso!
    echo ======================================================
)

echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul
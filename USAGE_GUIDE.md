# Guia de Uso - Sistema de Automação Inteligente

## 🏠 Local Principal de Uso

O **local principal** para usar o sistema é:

**`C:\Users\ciami\OneDrive\Área de Trabalho\projeto`**

Este é o diretório onde todo o sistema está instalado e pode ser executado.

## 🚀 Formas de Acessar e Usar o Sistema

### 1. 🖱️ Método Mais Fácil: Atalho na Área de Trabalho

1. **Execute o arquivo `run_system.bat`** que está na pasta do projeto
2. Ou **crie um atalho na área de trabalho** executando:
   ```
   python create_desktop_shortcut.py
   ```

### 2. ⌨️ Método via Linha de Comando

1. **Abra o Prompt de Comando** (cmd) ou PowerShell
2. **Navegue até o diretório do projeto**:
   ```cmd
   cd "C:\Users\ciami\OneDrive\Área de Trabalho\projeto"
   ```
3. **Execute o sistema**:
   ```cmd
   python src/main.py
   ```

### 3. 📂 Estrutura do Diretório Principal

```
C:\Users\ciami\OneDrive\Área de Trabalho\projeto\
├── src\                    # Código fonte principal
│   ├── main.py            # ARQUIVO PRINCIPAL PARA EXECUTAR
│   ├── agents\            # Agentes especializados
│   ├── pipelines\         # Pipelines de processamento
│   ├── integrations\      # Integrações externas
│   └── config\            # Gerenciador de configuração
├── config\                # Arquivos de configuração
├── docs\                  # Documentação
├── tests\                 # Testes automatizados
├── logs\                  # Arquivos de log (criados ao executar)
├── run_system.bat         # ARQUIVO PARA EXECUÇÃO FÁCIL
├── run_system_debug.bat   # ARQUIVO PARA DIAGNÓSTICO
├── requirements.txt       # Dependências do Python
└── README.md              # Documentação principal
```

## 🎯 Arquivos Mais Importantes para Uso Diário

1. **`run_system.bat`** - Arquivo para execução fácil (clique duas vezes)
2. **`run_system_debug.bat`** - Arquivo para diagnóstico de problemas
3. **`src/main.py`** - Arquivo principal do sistema
4. **`config/default.yaml`** - Configurações do sistema
5. **`logs/application.log`** - Arquivo de log (gerado após execução)

## 📋 Passos para Uso Imediato

1. **Localize a pasta do projeto**:
   `C:\Users\ciami\OneDrive\Área de Trabalho\projeto`

2. **Execute de uma das formas**:
   - **Opção 1**: Clique duas vezes em `run_system.bat`
   - **Opção 2**: Clique duas vezes em `run_system_debug.bat` (para diagnóstico)
   - **Opção 3**: Execute no cmd:
     ```cmd
     cd "C:\Users\ciami\OneDrive\Área de Trabalho\projeto"
     python src/main.py
     ```

3. **Veja o sistema em ação**:
   - O sistema demonstrará todos os agentes
   - Mostrará processamento por pipelines
   - Exibirá roteamento inteligente de tarefas
   - Gerará logs no diretório `logs/`

## 🛠️ Personalização

Para personalizar o sistema, edite:
- **`config/default.yaml`** - Ativar/desativar agentes e pipelines
- **`src/main.py`** - Modificar o comportamento principal (avançado)

## 📚 Documentação Completa

- **`docs/implemented_features.md`** - Documentação técnica completa
- **`README.md`** - Guia de início rápido
- **`PROJECT_SUMMARY.md`** - Resumo executivo

## 🆘 Solução de Problemas

### Se o sistema não executar:

1. **Tente o modo debug**:
   - Clique duas vezes em `run_system_debug.bat`
   - Este modo mostra mensagens detalhadas de erro

2. **Verifique dependências**:
   ```cmd
   cd "C:\Users\ciami\OneDrive\Área de Trabalho\projeto"
   pip install -r requirements.txt
   ```

3. **Verifique se o Python está instalado**:
   ```cmd
   python --version
   ```

### Comportamento Normal:
- Ao clicar em `run_system.bat`, **o prompt de comando abre** - isso é normal!
- O sistema **executa dentro do prompt** e mostra os resultados
- A janela **permanece aberta** para que você possa ver os resultados
- Pressione **QUALQUER TECLA** para fechar a janela

## 🎯 RESPOSTA DIRETA AO SEU PROBLEMA:

**O sistema ESTÁ funcionando corretamente!**

Quando você clica em `run_system.bat`:
1. ✅ **O prompt de comando abre** - isso é esperado
2. ✅ **O sistema executa dentro do prompt** - você deve ver as mensagens
3. ✅ **A janela permanece aberta** - para você ver os resultados
4. ✅ **Pressione qualquer tecla** para fechar

Se você NÃO está vendo mensagens no prompt, tente:
1. Clique em `run_system_debug.bat` em vez disso
2. Ou execute no cmd:
   ```cmd
   cd "C:\Users\ciami\OneDrive\Área de Trabalho\projeto"
   python src/main.py
   ```

**O local principal de uso é sempre: `C:\Users\ciami\OneDrive\Área de Trabalho\projeto`**
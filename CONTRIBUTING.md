# Guia de Contribuição

Obrigado por considerar contribuir para o Sistema de Automação Inteligente! Este documento fornece diretrizes para contribuir com o projeto.

## Código de Conduta

Ao contribuir para este projeto, você concorda em seguir nosso [Código de Conduta](CODE_OF_CONDUCT.md).

## Como Contribuir

### Relatando Problemas

Antes de criar uma nova issue, por favor:

1. Verifique se o problema já não foi relatado pesquisando nas issues existentes
2. Certifique-se de usar a última versão do código

Ao criar uma issue, inclua:

- Uma descrição clara e concisa do problema
- Passos para reproduzir o problema
- Versão do sistema operacional e Python
- Qualquer mensagem de erro relevante

### Sugerindo Melhorias

Você pode sugerir melhorias criando uma issue com:

- Uma descrição clara da melhoria proposta
- Justificativa para a melhoria
- Exemplos de como a melhoria seria usada

### Contribuindo com Código

#### Configuração do Ambiente de Desenvolvimento

1. Fork o repositório
2. Clone seu fork:
   ```bash
   git clone https://github.com/seu-usuario/intelligent-automation-system.git
   ```
3. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov
   ```

#### Diretrizes de Codificação

- Siga o estilo de código PEP 8
- Escreva docstrings para todas as funções, classes e módulos
- Mantenha funções e classes pequenas e focadas
- Use nomes descritivos para variáveis e funções
- Adicione comentários explicativos onde necessário

#### Testes

- Escreva testes unitários para novas funcionalidades
- Certifique-se de que todos os testes existentes passem:
  ```bash
  python tests/run_tests.py
  ```
- Mantenha uma cobertura de teste acima de 80%

#### Processo de Pull Request

1. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b feature/nome-da-feature
   ```
2. Faça suas alterações
3. Adicione ou atualize testes conforme necessário
4. Certifique-se de que todos os testes passam
5. Atualize a documentação se necessário
6. Faça commit das alterações:
   ```bash
   git commit -m "Adiciona feature X"
   ```
7. Envie para seu fork:
   ```bash
   git push origin feature/nome-da-feature
   ```
8. Crie um Pull Request no repositório original

#### Convenções de Mensagens de Commit

- Use o tempo verbal presente ("Adiciona feature" não "Adicionada feature")
- A primeira linha deve ter no máximo 72 caracteres
- Referencie issues e pull requests quando relevante

Exemplos:
```
Adiciona pipeline de processamento para documentos PDF
Corrige erro de roteamento em UserAgent
Atualiza documentação do sistema de configuração
```

## Estrutura do Projeto

- `src/` - Código fonte principal
  - `agents/` - Agentes especializados
  - `pipelines/` - Pipelines de processamento
  - `integrations/` - Adaptadores de integração
  - `config/` - Gerenciamento de configuração
- `tests/` - Testes unitários e de integração
- `docs/` - Documentação
- `config/` - Arquivos de configuração

## Padrões de Codificação

### Python

- Use Python 3.7+ 
- Siga PEP 8
- Use type hints quando apropriado
- Prefira f-strings para formatação de strings

### Documentação

- Documente todas as funções públicas
- Use docstrings no estilo Google
- Mantenha a documentação em português
- Atualize docs/implemented_features.md quando adicionar novas funcionalidades

## Processo de Revisão

Pull Requests são revisados por mantenedores do projeto. O processo de revisão inclui:

1. Verificação de estilo de código
2. Revisão de lógica e implementação
3. Verificação de cobertura de testes
4. Revisão de documentação
5. Testes automatizados

## Comunidade

- Junte-se a nós no [canal de discussão] (se aplicável)
- Participe das discussões nas issues
- Ajude outros contribuidores

## Agradecimentos

Suas contribuições são valiosas para o projeto. Obrigado por ajudar a melhorar o Sistema de Automação Inteligente!
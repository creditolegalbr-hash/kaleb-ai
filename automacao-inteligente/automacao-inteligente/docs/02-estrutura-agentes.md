# Estrutura Modular Técnica por Agente

Cada agente será um módulo independente com responsabilidades específicas:

- **EmailAgent** → Processar emails recebidos, extrair informações relevantes e acionar pipelines.  
- **FinanceAgent** → Organizar dados financeiros, validar relatórios e gerar insights.  
- **SchedulerAgent** → Gerenciar calendários, prazos e lembretes automáticos.  
- **DocumentAgent** → Extrair, classificar e interpretar documentos (OCR, PDFs, contratos).  
- **SupportAgent** → Responder clientes, triagem de chamados e encaminhamento.  

📌 **Regra:** cada agente **não deve ser acoplado** diretamente aos outros → comunicação sempre via pipelines/mensageria.  

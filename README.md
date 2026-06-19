# bbi-cases
Repositório para cases do bradesco

Case 1 — Earnings Call Intelligence Tracker
1. Arquitetura

Três arquivos Python: prompts.py guarda o prompt, engine.py faz a leitura da transcrição, chama a API e gera os outputs, main.py é a entrada do usuário. A transcrição fica em transcricao/ e os outputs em outputs/.
2. Decisões de prompt engineering

O prompt pede JSON com estrutura exata e fixa. As regras obrigatórias no final do prompt (ex: "exatamente 3 itens em perguntas_analistas") reduzem alucinação e garantem consistência. Temperature 0.2 para respostas mais determinísticas. A instrução de citação literal nos red flags e trechos evita que o modelo parafraseie.
3. Tempo gasto

Aproximadamente 5 horas.
4. Por que me aprofundei nesse case

Escolhi entregar os dois cores sem extensões. O Case 1 é mais complexo por exigir análise linguística com citações literais, então priorizei garantir que funcionasse bem antes de adicionar extensões.
5. Três limitações mais sérias

A transcrição usada é parcialmente reconstituída — o Q&A real completo não estava disponível gratuitamente
O modelo às vezes usa o nome da chave JSON diferente do especificado no prompt, exigindo ajuste manual
Sem comparação com trimestres anteriores reais, o campo de mudanças de guidance depende apenas do que está na transcrição

6. Com mais 2 semanas

Adicionaria comparação temporal automática entre trimestres, busca automática de transcrições via web, e um self-critique loop onde o modelo revisa sua própria análise antes de retornar o JSON final.

Case 2 — Macro Scenario Engine
1. Arquitetura

Mesma estrutura: prompts.py, engine.py e main.py. O usuário digita o cenário no terminal, a API retorna JSON estruturado, e o sistema salva JSON e markdown em outputs/.
2. Decisões de prompt engineering

Prompt com estrutura JSON explícita e regras obrigatórias de quantidade (exatamente 5 setores, 3 tickers). Instrução de usar apenas tickers reais da B3 reduz alucinação. Temperature 0.3 para equilíbrio entre consistência e qualidade analítica.
3. Tempo gasto

Aproximadamente 6 horas.
4. Por que me aprofundei nesse case

Mesmo raciocínio — priorizei entregar os dois cores funcionando corretamente a aprofundar só um.
5. Três limitações mais sérias

O modelo não tem acesso a dados de mercado em tempo real, então as justificativas de tickers são baseadas em conhecimento estático
Sem validação se os tickers retornados existem de fato na B3
A análise não considera correlações entre setores — um setor beneficiado pode ter efeito negativo em outro

6. Com mais 2 semanas

Adicionaria validação automática dos tickers via API da B3, confidence scoring por setor, e comparação entre cenários para o analista ver o delta entre dois cenários macro diferentes.

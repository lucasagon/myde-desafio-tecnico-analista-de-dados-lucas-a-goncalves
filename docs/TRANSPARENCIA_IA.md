# Transparência — Uso de IA

**Participante:** Lucas Almeida Gonçalves  
**Repositório:** [github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves](https://github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves)  
**Notion:** [Hub MYDE](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445)

## Ferramenta e consumo de contexto

| Campo | Valor |
|---|---|
| IDE / agente | **Cursor** (modo Agent / chat) |
| Repositório | `myde` |
| Tamanho de contexto | **200K** tokens |
| Tokens utilizados (sessão principal) | **~172,7K** |

> Os valores de contexto referem-se ao uso agregado da sessão de desenvolvimento assistido no Cursor durante este projeto (jun/2026). Não incluem necessariamente outras ferramentas ou sessões fora do Cursor.

## Escopo do apoio da IA

| Área | Apoio da IA | Responsabilidade do participante |
|---|---|---|
| SQL (`consultas.sql`, views star) | Estrutura, queries, validação via script | Revisão, execução e interpretação |
| Power BI | Guia ODBC, modelo, medidas DAX, documentação | Conexão ODBC, relacionamentos, visuais, `.pbix` |
| Python (bônus) | Notebook, pipeline, `docs/PYTHON.md` | Execução e leitura dos resultados |
| Documentação | `README`, `docs/*`, plano, insights | Revisão final e decisões de entrega |

O PDF do desafio permite documentação e ferramentas de apoio; este arquivo explicita **como** a IA foi usada.

## Arquivos Power BI no repositório

| Arquivo | Função |
|---|---|
| [`powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix`](../powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix) | **Entrega principal** — relatório completo com dados em modo **Import** (~21,7 MB). O avaliador abre no Power BI Desktop e vê KPIs, gráficos e filtros sem precisar reconectar ao MariaDB. |
| [`powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbit`](../powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbit) | **Template do modelo** — mesma estrutura (tabelas, relações, medidas, layout), **sem dados** embutidos (~2,5 MB). Serve para versionar o esqueleto ou reimportar dados via ODBC/CSV em outra máquina. |
| [`powerbi/bgs/`](../powerbi/bgs/) | Logo MYDE (SVG) e fundos PNG usados no layout (3 páginas). |
| [`powerbi/medidas.dax`](../powerbi/medidas.dax) | Medidas DAX versionadas (fonte para a tabela `_medidas` no modelo). |
| [`powerbi/PBIX_BUILD.txt`](../powerbi/PBIX_BUILD.txt) | Resumo do fluxo de construção do painel. |
| [`powerbi/analyze_pbit.py`](../powerbi/analyze_pbit.py) | Script para inspecionar tabelas, relações e medidas no `.pbit`. |
| [`powerbi/analyze_report.py`](../powerbi/analyze_report.py) | Script para listar páginas e visuais no `.pbit`. |

**Qual enviar / abrir para avaliação:** o **`.pbix`**. O **`.pbit`** é complementar (modelo reutilizável).

## Referências

- Guia Power BI: [`docs/POWERBI.md`](POWERBI.md)
- Checklist de entrega: [`docs/ENTREGA.md`](ENTREGA.md)
- Runbook de testes: [`docs/RUNBOOK.md`](RUNBOOK.md)
- Troubleshooting: [`docs/TROUBLESHOOTING.md`](TROUBLESHOOTING.md)
- Insights de negócio: [`docs/INSIGHTS.md`](INSIGHTS.md)
- Sessões Cursor (local): `C:\Users\lucas\.cursor\projects\d-Projects-myde` (ver `prompts_location.md`)

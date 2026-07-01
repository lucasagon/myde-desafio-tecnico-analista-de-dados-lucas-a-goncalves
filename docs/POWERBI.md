# Parte 2 — Power BI

**Notion:** [Hub MYDE](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445) · **Runbook:** [`RUNBOOK.md`](RUNBOOK.md) · **Troubleshooting:** [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)

Arquivo alvo: `powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix`  
Template: `powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbit`

## Arquivos `.pbix` e `.pbit`

| Arquivo | Função |
|---|---|
| `.pbix` | Relatório **com dados** (Import) — **entrega** para o avaliador |
| `.pbit` | **Template** do modelo (sem dados) — versionar estrutura e reimportar em outro ambiente |

Transparência sobre uso de IA: `docs/TRANSPARENCIA_IA.md`

## Abordagem do projeto

O Power BI consome a **camada semântica SQL** (`sql/views/`) **diretamente no MariaDB**, colando o `SELECT` de cada view na conexão. Transformação no SQL, modelo star no PBI, sem merges no Power Query.

```text
[Caminho usado]      MariaDB → ODBC (MariaDB 3.2) + SQL nativo → Import → relacionamentos FK → DAX → visuais

[Alternativa]        MariaDB → conector MySQL + Connector/NET 8.0 x64 (se ODBC falhar)

[Fallback offline]   MariaDB → export_views.py → CSV → Import no PBI
```

> **CSV** só se conexão instável, trabalho offline ou `fact_trans` muito lenta na 1ª carga.

---

## Pré-requisitos

- Power BI Desktop (64-bit)
- **MariaDB Connector/ODBC 3.2 Driver (64-bit)** — verificado em *Fontes de dados ODBC (64 bits)* (`odbcad32.exe`)
- Credenciais do dataset Berka (públicas)

| Parâmetro | Valor |
|---|---|
| Servidor | `relational.fel.cvut.cz` |
| Porta | `3306` |
| Banco | `financial` |
| Usuário | `guest` |
| Senha | `ctu-relational` |

### Por que ODBC e não o conector “MariaDB” do PBI?

No Windows, o conector **MariaDB** embutido no Power BI pode pedir `{MariaDB ODBC 3.1 Driver}`, que não estava instalado. O driver disponível era **MariaDB ODBC 3.2 (64-bit)**. A conexão via **Obter dados → ODBC** com o nome correto do driver funcionou de forma estável.

O conector **MySQL** nativo exige **MySQL Connector/NET 8.0.x (64-bit)** em `HKLM:\SOFTWARE\MySQL AB` — só a versão 32-bit (`WOW6432Node`) não é reconhecida pelo Power BI Desktop.

---

## Conexão ODBC (caminho utilizado)

### 1. Configurar o Power BI Desktop

Arquivo → Opções → **Dados globais** → desmarque **Detectar automaticamente relações de coluna**.

Recomendado também: em **Carga de dados**, desmarque **Detecção automática de data/hora** (evita `LocalDateTable_*` e permite usar uma única tabela `Calendario`).

### 2. String de conexão (sem usuário/senha)

**Obter dados → ODBC** → marque **Cadeia de conexão** e cole:

```
DRIVER={MariaDB ODBC 3.2 Driver};SERVER=relational.fel.cvut.cz;PORT=3306;DATABASE=financial
```

> **Não inclua `UID` nem `PWD` na string.** O Power BI exige credenciais na janela de autenticação (`The connection property 'uid' can only be provided using credentials`).

### 3. Credenciais

Na janela que abrir após **OK**:

| Campo | Valor |
|---|---|
| Tipo de autenticação | **Banco de dados** |
| Usuário | `guest` |
| Senha | `ctu-relational` |

### 4. Modo de armazenamento

Pelo conector **ODBC**, o fluxo é **Import** (padrão): os dados passam pelo Power Query e, ao clicar em **Fechar e aplicar**, ficam dentro do `.pbix`. Não há opção DirectQuery nesse caminho.

Para confirmar: **Modo de exibição de modelo** → selecione uma tabela → **Modo de armazenamento: Importar**.

### 5. Importar cada view (uma consulta ODBC por tabela)

Repita para **cada** arquivo em `sql/views/dim/` e `sql/views/fact/`:

1. **Obter dados → ODBC** (mesma cadeia de conexão)
2. **Opções avançadas → Instrução SQL** → cole o `SELECT` completo do `.sql` (sem `;` no final; remova linhas `--` de comentário se o driver reclamar)
3. **OK** → credenciais `guest` / `ctu-relational`
4. No Power Query, renomeie a consulta conforme a tabela abaixo
5. **Fechar e aplicar**

| Arquivo SQL | Nome sugerido no modelo |
|---|---|
| `sql/views/dim/vw_dim_district.sql` | `dim_district` |
| `sql/views/dim/vw_dim_client.sql` | `dim_client` |
| `sql/views/dim/vw_dim_account.sql` | `dim_account` |
| `sql/views/dim/vw_dim_disp.sql` | `dim_disp` |
| `sql/views/dim/vw_dim_card.sql` | `dim_card` |
| `sql/views/fact/vw_fact_loan.sql` | `fact_loan` |
| `sql/views/fact/vw_fact_trans.sql` | `fact_trans` |
| `sql/views/fact/vw_fact_card_account.sql` | `fact_card_account` |
| `sql/views/fact/vw_fact_agg_carteira.sql` | `fact_agg_carteira` |

**Não importe** as 8 tabelas brutas (`account`, `loan`, etc.).  
**Não faça** merges/joins no Power Query — os joins já estão nas views SQL.

#### Exemplo: teste de conexão

```sql
SELECT district_id, A2 AS district_name FROM district LIMIT 5
```

#### Exemplo: `dim_district`

Cole o conteúdo integral de `sql/views/dim/vw_dim_district.sql` (apenas o `SELECT`).

### 6. Entrega e refresh

| Formato | Uso |
|---|---|
| `.pbix` | Entrega final — dados em **Import** ficam no arquivo; o avaliador abre sem precisar reconectar |
| `.pbit` | Template — estrutura sem dados; útil para versionar o modelo |

Para **atualizar** dados em outra máquina: instalar **MariaDB ODBC 3.2 (64-bit)** e usar as mesmas credenciais. DSN local (`DSN=...`) não é portável — prefira sempre a cadeia com `DRIVER={...}`.

---

## Alternativa: conector MySQL nativo

Se o Connector/NET 64-bit estiver instalado:

1. **Obter dados → Banco de dados MySQL**
2. Servidor `relational.fel.cvut.cz` | Banco `financial` | Modo **Importar**
3. Desmarque conexão criptografada
4. **Opções avançadas** → cole o SQL da view

---

## `fact_trans` (~1M linhas)

- A 1ª carga via ODBC pode demorar vários minutos.
- Se travar, monte o primeiro rascunho só com `fact_loan` + `fact_agg_carteira` + dims.
- Fallback: `python powerbi/export_views.py` → CSV em `powerbi/data/`.

---

## Relacionamentos (star schema por FK)

Modo **Modelo** → relações **1:N** (dimensão → fato), filtro **single direction** (simples):

| De | Para | Coluna |
|---|---|---|
| `fact_loan` | `dim_district` | `district_id` |
| `fact_loan` | `dim_account` | `account_id` |
| `fact_loan` | `dim_calendar` | `loan_date` → `Date` (ativa) |
| `fact_trans` | `dim_account` | `account_id` |
| `fact_trans` | `dim_calendar` | `trans_date` → `Date` (inativa) |
| `fact_card_account` | `dim_account` | `account_id` |
| `fact_card_account` | `dim_card` | `card_id` |
| `fact_agg_carteira` | `dim_district` | `district_id` |
| `dim_client` | `dim_district` | `district_id` |
| `dim_disp` | `dim_client` | `client_id` |
| `dim_disp` | `dim_account` | `account_id` |
| `dim_card` | `dim_disp` | `disp_id` |

**Atenção após importação automática:** o PBI pode criar relações **inativas** ou **bidirecionais**. Revise e corrija:

- Ativar: `dim_card` → `dim_disp`, `dim_disp` → `dim_client`
- Trocar bidirecional → **simples** em fatos ↔ dims
- Se `fact_loan[district_id]` ficar inativo por ambiguidade com `account → district`, manter um caminho ativo consistente para filtros por região

---

## Tabela de datas — `dim_calendar` (`CalendarAuto()`)

O modelo usa **`dim_calendar`**, criada com:

```dax
dim_calendar = CalendarAuto()
```

Configuração aplicada:

| Relação | Status |
|---|---|
| `dim_calendar[Date]` → `fact_loan[loan_date]` | **Ativa** (slicers e evolução de concessões) |
| `dim_calendar[Date]` → `fact_trans[trans_date]` | **Inativa** (evita ambiguidade no modelo) |

Para transações por data, use a medida `Valor Transações no Período` em `_medidas` (com `USERELATIONSHIP`).

**Opcional:** ocultar `LocalDateTable_*` e `DateTableTemplate_*` na exibição do modelo.

---

## Medidas DAX — tabela `_medidas`

As medidas ficam na tabela **`_medidas`** (padrão recomendado no PBI). Lista no modelo:

| Medida | Formato sugerido |
|---|---|
| Valor Total Emprestado | Moeda **CZK** (`Kč`) |
| Ticket Médio Empréstimo | Moeda CZK |
| Taxa Inadimplência | **%** (2 casas) |
| Taxa Inadimplência Região | % |
| Qtd Empréstimos / Contas / Clientes / Cartões | Número inteiro |
| Concessões no Período | Inteiro |
| Valor Concedido no Período | Moeda CZK |

Fonte DAX versionada: `powerbi/medidas.dax`

> Dataset Berka = **coroa tcheca (CZK)**. Não use R$ nos visuais.

### Validação rápida (cartões KPI)

| Medida | Valor esperado |
|---|---|
| `Qtd Empréstimos` | **682** |
| `Taxa Inadimplência` | **~0,1114** (11,14% formatado) |

---

## Status do modelo e relatório

| Item | Status |
|---|---|
| Conexão ODBC MariaDB 3.2 + 9 views SQL | Feito |
| Modo Import (dados no `.pbix`) | Feito |
| Tabelas `dim_*` / `fact_*` | Feito |
| `dim_calendar` + relações (loan ativo, trans inativo) | Feito |
| Medidas DAX em `_medidas` (12 medidas) | Feito |
| Página **Início** (layout + logo/fundo) | Feito |
| Página **Visão Geral** (KPIs, linha, slicers) | Feito |
| Página **Risco por Região** (barras, tabela agg) | Feito |
| Assets visuais em `powerbi/bgs/` | Feito |
| Formatação CZK (`Kč`) e % nas medidas | Feito |
| KPIs validados (682 empréstimos / ~11,14% inadimplência) | Feito |
| Entrega via repositório Git | Feito |

Análise automática:

```powershell
python powerbi/analyze_pbit.py      # modelo + medidas + relações
python powerbi/analyze_report.py    # páginas e visuais
```

---

## Estrutura do relatório (implementado)

**3 páginas** — assets-fonte em `powerbi/bgs/` (logo SVG + PNGs de fundo).

### Página Início

Layout de abertura com logo MYDE e fundo (`bmg-bg-like-homepage.png`). Sem KPIs analíticos.

### Página Visão Geral

| Visual | Campos |
|---|---|
| 3× Cartão KPI | `Valor Total Emprestado`, `Taxa Inadimplência`, `Qtd Empréstimos` |
| Gráfico de linhas | `Valor Concedido no Período` × `dim_calendar` (Ano) |
| Segmentadores | Ano (`dim_calendar`), `fact_loan[status]`, `fact_loan[faixa_valor]` |

Fundo: `bmg-bg-like-layout1.png`

### Página Risco por Região

| Visual | Campos |
|---|---|
| Segmentadores | Ano, `status`, `faixa_valor` |
| Barras | `Valor Total Emprestado` por `dim_district[district_name]` |
| Barras | `Taxa Inadimplência Região` por `district_name` |
| Tabela | `district_name`, `periodo_mes`, `status`, `faixa_valor`, `qtd_emprestimos`, `valor_total`, `valor_medio`, `taxa_inadimplencia_pct` |

Fundo: `bmg-bg-like-layout2.png`

A tabela usa `fact_agg_carteira` + `dim_district` e reage aos filtros dos outros visuais (filtros cruzados).

### Filtro de `status` — loan vs agg

| Visual | Slicer / filtro |
|---|---|
| Gráficos e KPIs (`fact_loan`) | `fact_loan[status]` |
| Tabela analítica (`fact_agg_carteira`) | `fact_agg_carteira[status]` |

**Não há relação** entre `fact_loan` e `fact_agg_carteira`. Um slicer só em `fact_loan` **não filtra a tabela**.

**Solução (recomendada):** **Sincronizar slicers** na página Risco por Região:

1. Coloque (ou mantenha) slicer com `fact_loan[status]`
2. Adicione um segundo slicer com `fact_agg_carteira[status]` (pode **ocultar** depois: formato → desligar título, fundo transparente, ou posicionar fora da área visível)
3. Menu **Exibir → Sincronizar slicers** → marque os dois campos `status` na mesma página → ative sincronização entre eles
4. O usuário usa só o slicer de `fact_loan`; o de `agg` acompanha e filtra a tabela

**Gráfico Taxa Inadimplência Região não filtra:** em **Formato do slicer → Editar interações**, clique no slicer e no gráfico escolha o ícone de **filtro** (não o “nenhum”). Confirme a medida `Taxa Inadimplência Região` sem `REMOVEFILTERS` (ver `powerbi/medidas.dax`).

> **Leitura da coluna `taxa_inadimplencia_pct` na tabela:** o grain inclui `status`; por linha a taxa tende a 0% (A/C) ou 100% (B/D). Para taxa consolidada por região, use o gráfico de barras com a medida DAX.

---

## Medidas DAX (referência)

Ver `powerbi/medidas.dax` — alinhado com `dim_calendar` e tabela `_medidas`.

---

## Visuais — requisito do PDF

O PDF pede **1 a 2 páginas** analíticas; o projeto entrega **2 páginas de análise** (Visão Geral + Risco por Região) mais **1 página Início** (apresentação). Elementos obrigatórios cobertos:

| Requisito PDF | Onde está |
|---|---|
| KPIs carteira / inadimplência / nº empréstimos | Visão Geral — cartões |
| Evolução concessões no tempo | Visão Geral — linha + slicer Ano |
| Inadimplência por região | Risco por Região — barras `Taxa Inadimplência Região` |
| Ranking por volume | Risco por Região — barras `Valor Total Emprestado` |
| Segmentadores período / status / faixa | Visão Geral e Risco por Região |
| Tabela analítica com filtros cruzados | Risco por Região — `fact_agg_carteira` |

**Opcional (PDF):** KPIs `Qtd Contas`, `Qtd Clientes`, `Qtd Cartões` — medidas existem em `_medidas`, mas não estão nos visuais atuais.

---

## Validação do modelo

Script local (inspeciona `.pbit` / `.pbix`):

```powershell
python powerbi/analyze_pbit.py
python powerbi/analyze_report.py
python powerbi/validate_pbit.py
```

| Métrica | SQL | PBI esperado |
|---|---|---|
| Taxa inadimplência | 11,14% | ~11,14% |
| Total empréstimos | 682 | 682 |
| Com cartão vs sem | 2,94% vs 13,87% | consistente |

---

## CSV (fallback offline)

```powershell
python powerbi/export_views.py
```

**Obter dados → Texto/CSV** → `powerbi/data/` → mesmos passos de relacionamento e DAX.

---

## Tabelas do modelo

| Tabela PBI | Origem SQL | Linhas (aprox.) |
|---|---|---|
| dim_district | vw_dim_district | 77 |
| dim_client | vw_dim_client | 5.369 |
| dim_account | vw_dim_account | 4.500 |
| dim_disp | vw_dim_disp | 5.369 |
| dim_card | vw_dim_card | 892 |
| fact_loan | vw_fact_loan | 682 |
| fact_trans | vw_fact_trans | 1.056.320 |
| fact_card_account | vw_fact_card_account | 4.500 |
| fact_agg_carteira | vw_fact_agg_carteira | 648 |
| dim_calendar | `CalendarAuto()` | auto |
| _medidas | DAX (tabela de medidas) | — |

---

## Referência rápida

- Resumo: `powerbi/PBIX_BUILD.txt`
- Assets: `powerbi/bgs/` (logo + fundos)
- Medidas: `powerbi/medidas.dax`
- Views SQL: `sql/views/dim/`, `sql/views/fact/`
- Validar modelo: `powerbi/validate_pbit.py`
- Analisar relatório: `powerbi/analyze_report.py`
- Export CSV (fallback): `powerbi/export_views.py`

## Troubleshooting ODBC / MySQL no Windows

| Erro | Causa | Solução |
|---|---|---|
| `Requested value 'None' was not found` | Connector/NET ausente ou só 32-bit | Instalar Connector/NET 8.0.x **64-bit** ou usar ODBC |
| `MariaDB ODBC 3.1 Driver` não encontrado | Conector MariaDB do PBI vs driver 3.2 instalado | Usar **ODBC** com `DRIVER={MariaDB ODBC 3.2 Driver}` |
| `uid can only be provided using credentials` | UID/PWD na string ODBC | Remover da string; informar na janela **Banco de dados** |

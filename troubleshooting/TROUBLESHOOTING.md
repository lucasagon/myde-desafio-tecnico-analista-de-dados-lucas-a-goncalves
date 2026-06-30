# Troubleshooting — efizion-server-ops

Este guia define o padrão de diagnóstico e registro de incidentes da infraestrutura Efizion (`191.96.251.9`).

Antes de qualquer correção, confirme em qual camada o problema ocorre: DNS, proxy (Traefik), firewall, container Docker, banco de dados ou configuração do cliente.

## Como usar este documento

1. Identifique a camada afetada (ver mapa abaixo).
2. Execute a checagem mínima da seção correspondente.
3. Se não resolver, abra um novo registro em `troubleshooting/NN_<titulo>.md` usando o template deste arquivo.
4. Após corrigir, atualize `projects_memory.md` e, se necessário, `env.md`.

## Índice de incidentes registrados

| # | Arquivo | Resumo |
|---|---------|--------|
| 01 | [01_db_efizion_prontoplast_powerbi_odbc.md](01_db_efizion_prontoplast_powerbi_odbc.md) | Cliente Prontoplast sem acesso ao PostgreSQL via Power BI ODBC em `db.efizion.com.br:443` |

## Mapa rápido de falhas

| Camada | Sintomas comuns | Onde olhar |
|--------|-----------------|------------|
| DNS | Domínio não resolve, IP errado | Cloudflare, registro A de `db.efizion.com.br` |
| Proxy (Traefik) | 404 HTTP, timeout TCP, cert inválido | `/opt/prod/infra/traefik_dynamic.yml`, logs `traefik-prod` |
| Firewall | Porta aberta no container, timeout externo | `iptables DOCKER-USER`, `ufw status` |
| PostgreSQL | Auth failed, database does not exist | `pg_hba.conf`, roles, logs `postgres-prod` |
| Cliente (ODBC/app) | Timeout, SSL error, credencial | Parâmetros host/porta/database/SSL |

## Checagens mínimas por camada

### 1) DNS e conectividade

```bash
getent hosts db.efizion.com.br
nc -zv db.efizion.com.br 443
nc -zv db.efizion.com.br 5435   # esperado: bloqueado externamente
```

**Esperado:**
- `db.efizion.com.br` → `191.96.251.9` (DNS direto, sem proxy Cloudflare)
- Porta 443 aberta; portas PostgreSQL nativas (5435/5434) bloqueadas externamente

### 2) Traefik (proxy reverso oficial)

```bash
ssh root@191.96.251.9
docker ps --format 'table {{.Names}}\t{{.Ports}}' | grep traefik
docker exec traefik-prod cat /etc/traefik/dynamic.yml | grep -A20 '^tcp:'
docker logs traefik-prod --tail 50
```

**Esperado:**
- `traefik-prod` em `0.0.0.0:80` e `0.0.0.0:443`
- TCP router `postgres_db` com `HostSNI(\`db.efizion.com.br\`)` → `postgres-prod:5432`

### 3) PostgreSQL

```bash
docker exec postgres-prod psql -U admin -d postgres -c "SHOW ssl;"
docker exec postgres-prod psql -U admin -d postgres -c "\du <usuario>"
docker exec postgres-prod psql -U admin -d postgres -c "\l" | grep <database>
docker logs postgres-prod --tail 50
```

### 4) Teste de conexão externa (simula cliente)

```bash
psql "postgresql://<user>:<pass>@db.efizion.com.br:443/<database>?sslmode=require&connect_timeout=10" -c "SELECT 1;"
```

### 5) Firewall no host

```bash
iptables -L DOCKER-USER -n -v
ufw status verbose
```

**Esperado:** apenas 80/443 liberados de entrada em `eth0`; demais portas DROP.

---

## Template de registro de incidente

Copie este bloco para cada ocorrência nova em `troubleshooting/NN_<titulo_curto>.md`:

```md
# Incidente NN — <titulo_curto>

| Campo | Valor |
|-------|-------|
| Data | YYYY-MM-DD |
| Servidor | 191.96.251.9 |
| Serviço afetado | <ex: postgres-prod, traefik-prod> |
| Impacto | <quem/o que deixou de funcionar> |
| Status | investigando / corrigido / monitorando |

## Contexto do problema

<o que estava sendo executado, por quem, com qual objetivo>

## Sintoma relatado

<sintoma observado pelo usuário ou cliente>

## Investigação

### Hipóteses avaliadas

- [ ] DNS / Cloudflare
- [ ] Traefik (HTTP ou TCP)
- [ ] Firewall / porta bloqueada
- [ ] PostgreSQL (pg_hba, SSL, permissões)
- [ ] Configuração do cliente (driver, senha, database)

### Evidências

<comandos executados, outputs relevantes, horários>

## Causa raiz

<explicação técnica objetiva>

## Decisão tomada

<ação escolhida para corrigir>

## Motivo técnico da decisão

<por que essa ação era a mais adequada>

## Correções aplicadas

- [ ] <item 1>
- [ ] <item 2>

## Validação pós-correção

<comandos e resultados que confirmam o fix>

## Parâmetros corretos para o cliente (se aplicável)

| Campo | Valor |
|-------|-------|
| Host | |
| Porta | |
| Database | |
| Usuário | |
| SSL | |

> Credenciais sensíveis: registrar em `env.md`, não duplicar aqui se possível.

## Consequência prática

<resultado obtido, impacto, trade-offs>

## Prevenção / próximos passos

<o que documentar, monitorar ou automatizar para evitar recorrência>

## Referências

- `env.md`
- `projects_memory.md`
- arquivos de config no servidor: <paths>
```

---

## Convenções de nomenclatura

- Arquivos de incidente: `NN_<area>_<resumo>.md` (ex: `02_traefik_cert_expirado.md`)
- Numeração sequencial, sem reutilizar números
- Atualizar a tabela "Índice de incidentes" neste arquivo ao criar novo registro

## Referências do projeto

- [`env.md`](../env.md) — acessos, credenciais, connection strings
- [`projects_memory.md`](../projects_memory.md) — estado consolidado da infra
- [`diretrizes.md`](../diretrizes.md) — processo operacional dos agentes

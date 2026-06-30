# [PROJETO] — Descritivo de Ambiente

## Identificação

| Campo | Valor |
|---|---|
| Projeto | Desafio técnico MYDE — Analista de Dados |
| REPO_GIT | git@github.com:lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves.git |
| Branch | main |
| Última atualização | 2026-06-30 |

## Banco de Dados — Berka / PKDD'99 (financial)

| Campo | Valor |
|---|---|
| Host | relational.fel.cvut.cz |
| Porta | 3306 |
| Database | financial |
| Usuário | guest (somente leitura) |
| Senha | ver `.env` (`DB_PASSWORD`) |
| Dataset | https://relational.fel.cvut.cz/dataset/Financial |

### Tabelas

account, card, client, disp, district, loan, order, trans

---

## Hardware

| Recurso | Detalhe |
|---|---|
| CPU | |
| RAM | |
| Swap | |
| Disco principal | |

---

## Acessos

### Usuários do sistema

| Usuário | UID | Shell | Sudo |
|---|---|---|---|
| `root` | 0 | `/bin/bash` | — |
| `` | | | |

### SSH

- Porta: **22**
- Root login: 
- Autenticação por senha: 
- Autenticação por chave pública: 

### VPN (Tailscale / WireGuard / outro)

| Node | IP VPN | OS |
|---|---|---|
| `este servidor` | `` | |
| `` | `` | |

---

## Portas abertas

| Porta | Serviço |
|---|---|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| | |

---

## Reverse Proxy

- **Ferramenta**: (Traefik / Caddy / Nginx / outro)
- **TLS**: (Let's Encrypt / manual / nenhum)
- **Config**: ``

### Domínios mapeados

| Domínio | Destino / Container |
|---|---|
| `` | `` |

---

## Banco de Dados

### [Nome do banco / engine]

- **Imagem / versão**: ``
- **Container**: ``
- **Porta host**: `` → `` interno
- **Volume**: ``
- **Network**: ``

### Schemas / Databases

| Schema / Database | Serviço que usa |
|---|---|
| `` | `` |

### Cache / Outros

- Redis: 
- Outros: 

---

## Containers / Serviços Docker

### [Nome do stack] (`/opt/...`)

| Container | Porta interna | Descrição |
|---|---|---|
| `` | | |

### Outros serviços referenciados

- `` — descrição
- `` — descrição

---

## APIs

| API | URL | Tecnologia | Descrição |
|---|---|---|---|
| `` | `` | `` | `` |

---

## Redes Docker

| Rede | Uso |
|---|---|
| `app_network` | Rede principal compartilhada |
| `` | `` |

---

## CI/CD

- **Diretório**: ``
- **Ferramenta**: (GitHub Actions / GitLab CI / outro)
- **Usuário de deploy**: ``
- **Observações**: 

---

## Serviços Systemd Relevantes

| Serviço | Descrição |
|---|---|
| `docker.service` | Docker Engine |
| `ssh.service` | OpenSSH |
| `` | `` |

---

## Cron Jobs

| Horário | Comando / Descrição |
|---|---|
| `` | `` |

---

## Volumes Persistentes

| Volume | Uso |
|---|---|
| `` | `` |

---

## Observações Gerais

- 
- 

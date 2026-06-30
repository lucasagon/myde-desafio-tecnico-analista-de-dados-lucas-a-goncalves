# Runbook: <NOME_DO_SERVICO / APP>

> Status: `ativo` | `deprecated` | `em-construcao`
> Última atualização: AAAA-MM-DD — por: <autor>
> Tags: `#docker` `#vps` `#webapp` `#db` `#cron`

---

## 1. Visão geral

| Item | Valor |
|---|---|
| Nome do serviço | |
| Descrição (1 linha) | |
| Responsável / Owner | |
| Criticidade | `baixa` / `média` / `alta` |
| Repositório | |
| Domínio / URL | |
| Ambiente | `prod` / `staging` / `dev` |

---

## 2. Infraestrutura

| Item | Valor |
|---|---|
| VPS / Host | <provedor, IP, hostname> |
| SO | |
| Acesso (SSH) | `ssh user@host -p <porta>` |
| Stack | <ex: Docker Compose, Nginx, Postgres> |
| Caminho do projeto no host | `/srv/...` |
| Reverse proxy | <Nginx / Traefik / Caddy> |
| TLS / Certbot | <auto-renew? caminho?> |

### Containers / Serviços

| Container | Imagem | Porta(s) | Volume(s) | Depende de |
|---|---|---|---|---|
| | | | | |

---

## 3. Variáveis de ambiente / Secrets

> ⚠️ Nunca colar valores reais aqui. Apenas chave + onde está armazenado.

| Variável | Onde está | Observação |
|---|---|---|
| `DATABASE_URL` | `.env` / cofre / etc | |
| | | |

---

## 4. Deploy / Atualização

### Pré-requisitos
- [ ] 
- [ ] 

### Passos
```bash
# 1. acessar host
ssh user@host

# 2. atualizar código
cd /srv/app && git pull

# 3. rebuild / restart
docker compose pull
docker compose up -d --build

# 4. verificar
docker compose ps
docker compose logs -f --tail=100
```

### Rollback
```bash
# como reverter para versão anterior
git checkout <tag/commit>
docker compose up -d --build
```

---

## 5. Operação do dia a dia

| Ação | Comando |
|---|---|
| Status | `docker compose ps` |
| Logs | `docker compose logs -f <serviço>` |
| Restart serviço | `docker compose restart <serviço>` |
| Entrar no container | `docker compose exec <serviço> sh` |
| Uso de recursos | `docker stats` |

---

## 6. Backup & Restore

| Item | Detalhe |
|---|---|
| O que é salvo | <banco, volumes, configs> |
| Frequência / Cron | `<expressão cron>` |
| Onde fica | <local / bucket> |
| Retenção | |

```bash
# backup
<comando de backup>

# restore
<comando de restore>
```

---

## 7. Jobs agendados (cron)

| Job | Expressão | Comando | Observação |
|---|---|---|---|
| | `* * * * *` | | |

---

## 8. Monitoramento & Health checks

| Item | Como verificar |
|---|---|
| Health endpoint | `curl https://.../health` |
| Métricas | |
| Alertas | |

---

## 9. Troubleshooting

### Sintoma: <descrição>
- **Causa provável:** 
- **Diagnóstico:** 
  ```bash
  
  ```
- **Solução:** 

### Sintoma: <descrição>
- **Causa provável:** 
- **Diagnóstico:** 
- **Solução:** 

---

## 10. Procedimentos de emergência

| Cenário | Ação imediata |
|---|---|
| Serviço fora do ar | |
| Disco cheio | `df -h` → limpar logs / `docker system prune` |
| Vazamento de credencial | rotacionar secret, redeploy |

---

## 11. Dependências externas

| Serviço / API | Uso | Contato / Docs |
|---|---|---|
| | | |

---

## 12. Histórico de mudanças

| Data | Autor | Mudança |
|---|---|---|
| AAAA-MM-DD | | |

---

## 13. Referências
- 
-
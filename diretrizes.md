# Fonte única de verdade para agentes

  

Este documento é a referência compartilhada entre todas as IAs do projeto. Qualquer ajuste deve ser feito aqui; os arquivos `CLAUDE.md`, `AGENTS.md` ou outros arquivos de guideles de outras IAs, nos repositórios downstream devem apontar de alguma forma para esta fonte via symlink.
  

---

  

## Setup Inicial Obrigatório dos Projetos

  

- O projeto que você está trabalhando possui um repositório GIT próprio e ele está na variável REPO_GIT do arquivo [[env]] que está aqui na pasta do projeto.  Os projetos precisam ter sempre um repositório GIT, caso você não encontre a informação, pergunte ao usuário e parta do princípio que o acesso será via SSH sempre;

- O projeto que você está trabalhando possui um arquivo chamado [[projects_memory]]  para que sejam salvos os snapshots do projeto - Caso ele não exista, você precisa gerar.

- O proejto que você está trabalhando possui um arquivo chamado [[prompts_location]] para que sejam informados os caminhos em que cada agente de IA registra as suas sessões - Caso ele não exista, você precisa gerar incluíndo as variáveis: 
	- CLAUDE_SESSIONS_DIR;
	- CODEX_SESSIONS_DIR;
	- CURSOR_SESSIONS_DIR;
	- GEMINI_SESSIONS_DIR;
	- DEEPSEEK_SESSIONS_DIR;

- Como os agentes utilizam cada um um arquivo de diretrizes específico, crie os arquivos seguindo a necessidade de cada agente:
	- Claude: CLAUDE.md
	- Codex: AGENTS.md
	- Cursor: .cursor/rules/
	
	Peça para o usuário reiniciar o prompt para carregar esses novos arquivos após eles terem sido criados. Eles devem ser Symlink desse arquivo de diretriz.

- Salve a localização que você utiliza nas variáveis do arquivo [[prompts_location]] focando apenas no seu agente. Se é a primeira vez que você está sendo executado, verifique se a sua DIR está salva no arquivo e se não tiver, já inclua.

- Utilize o arquivo [[env]] como referência de acessos aos servidores do projeto e localizações em geral. Caso ele não exista, crie.

- Caso o projeto possua servidor, é necessário inserir no arquivo [[env]]  as informações que ele pede e que estarão possívelmente vazias. O que você não tiver, solicitar ao usuário.

  

## Papel do Agente

  

Você é um agente técnico no contexto do projeto atual. Atue com foco em:

  

- qualidade técnica

- consistência arquitetural

- rastreabilidade

- documentação viva

- segurança de mudanças

  

---

  

## Regra Crítica de Memória do Projeto

  

Existe um arquivo obrigatório de memória consolidada do projeto:

  

`projects_memory.md`

  

### Regra complementar

  

1. Se `projects_memory.md` for um apontador para outra fonte:

- ler também a fonte apontada

- tratar essa memória como autoridade do projeto


2. Ignorar os arquivos project_memory, prompts_location e .env no gitignore.

3. Quando eu lhe pedir para criar tarefas ou lembretes, peço que considere que a lista que eu disser é a mesma coisa que o projectID, que ele precisa ser considerado na criação da tarefa e o projectID da lista "Trabalho" é 692925e93d072922bf0ac205. i.e.: Eu posso te pedir: "crie uma tarefa de lembrete para a lista Trabalho" e você entenderá que irá enviar o projectID dele.  - essas tarefas serão criadas com o auxílio do MCP configurado. Caso não tenha, informe ao usuário ou pergunte qual será caso queira saber. 

4. Ao criar tarefas, usar como título da tarefa algo que represente o que estamos fazendo

5. Ao criar tarefas, caso o usuário não informe a tag da tarefa, peça a ele antes de criar.

### Regra de localização de conversa

  

O projeto deve manter `prompts_location.md` na raiz com os caminhos locais relevantes de conversas e sessões. Esse arquivo deve ser ignorado pelo Git e lido antes de retomar contexto operacional quando existir.

  

### Regra Obrigatória (sempre)

  

ANTES de qualquer tarefa de análise ou execução (criar, editar, refatorar, excluir, migrar, otimizar):

  

1. Ler `projects_memory.md`

2. Ler a fonte indicada por `projects_memory.md`, quando houver apontador

3. Perguntar ao usuário se ele está vindo de outro agente e qual é o agente. Se tiver, leia a session do projeto em `prompts_location.md`  para se inteirar sobre ele.

4. Entender o estado atual consolidado:

   - arquitetura

   - componentes

   - fluxos

   - padrões

   - dependências

   - regras de negócio

   - decisões técnicas vigentes

5. Só então executar alterações.

### Regra Obrigatória Complementar (sempre)

1. Sempre que fizer troubleshooting, registrar na pasta /troubleshooting, seguindo o modelo imposto pelo arquivo TROUBLESHOOTING.md - você pode adicionar mais tópicos fugindo do padrão, porém faça e depois avise ao usuário sobre a mudança para ele aplicar no arquivo-modelo -, com a nomenclatura no seguinte padrão {numero-do-troubleshooting}_{plataforma/solucao}_{resumo-curto-do-troubleshooting}-{date-time-de-last-update-do-arquivo}.md
	1.1. Caso você realize outro troubleshooting relacionado porque o primeiro não resolveu, apenas atualize o arquivo, inclua as atualizações/alterações, tenha sensibilidade de entender se o mesmo arquivo serve e se for o caso modifique apenas o {date-time-de-last-update-do-arquivo} no nome do arquivo se não, apague o arquivo antigo e gere um novo.

2. Sempre que fizer alguma implementação, registrar os runbooks necessários para poder fazer troubleshooting ou outras operações na pasta /runbooks- você pode adicionar mais tópicos fugindo do padrão, porém faça e depois avise ao usuário sobre a mudança para ele aplicar no arquivo-modelo -, seguindo o modelo imposto pelo arquivo RUNBOOKS.md, com a nomenclatura no seguinte padrão {numero-do-runbook}_{plataforma/solucao}_{resumo-curto-do-runbook}-{date-time-de-last-update-do-arquivo}.md
	2.1. Caso você crie outra implementação etc relacionado ao arquivo já criado, apenas atualize o arquivo, inclua as atualizações/alterações, tenha sensibilidade de entender se o mesmo arquivo serve e se for o caso modifique apenas o {date-time-de-last-update-do-arquivo} no nome do arquivo se não, apague o arquivo antigo e gere um novo.

3. Os arquivos de documentação devem ficar na pasta /docs - Documentação é todo tipo de arquivo que traz luz sobre o uso do serviço/aplicação/implementação do projeto.
	3.1. Os arquivos de planos devem ficar obrigatóriamente na pasta /docs/plans

4. Sempre que a IA criar um plano no modo /plan ou outro modo compatível, ela deve gerar um arquivo na pasta /docs/plans com o seguinte padrão de nomenclatura: {numero-do-plano}_{plataforma/solucao}_{resumo-curto-do-plano}-{date-time-de-last-update-do-arquivo}.md
	4.1. Caso você precise atualizar o plano por conta de modificações nele, apenas atualize o arquivo, inclua as atualizações/alterações, tenha sensibilidade de entender se o mesmo arquivo serve e se for o caso modifique apenas o {date-time-de-last-update-do-arquivo} no nome do arquivo se não, apague o arquivo antigo e gere um novo.
	4.2. Quando um plano for implementado, tenha a sensibilidade de entender se durante a sua execução houveram modificações impostas pelo usuário e também atualize o arquivo relacionado àquele plano.

Se a tarefa envolver ambiente, infra ou integrações, ler também `/docs/.env` como referência de configuração (apenas leitura, nunca sobrescrever este arquivo).

  

---

  

## Atualização Obrigatória Pós-Mudança

  

Após qualquer modificação no projeto, atualizar `projects_memory.md` para refletir o novo estado real consolidado. A memória deve ser mantida como estado atual válido do sistema, não como histórico incremental.

  

Regras de atualização:

- refletir o novo estado real consolidado

- remover conteúdo obsoleto

- reescrever trechos impactados

- evitar duplicidade e histórico incremental morto

  

---

  

## Processo Obrigatório

  

Seguir esta ordem:

  
0. Perguntar qual branch estamos atuando
   
1. Ler `projects_memory.md`

2. Ler a fonte indicada por `projects_memory.md`, quando houver apontador

3. Perguntar ao usuário se ele está vindo de outro agente e qual é o agente. Se tiver, leia a session do projeto em `prompts_location.md`  para se inteirar sobre ele.

4. Ler `/docs/.env`, quando a tarefa envolver ambiente, infra ou integrações

5. Avaliar impacto e dependências

6. Executar mudança

7. Executar rebuild e redeploy em produção

8. Validar consistência e efeitos colaterais

9. Atualizar `projects_memory.md`

10. Executar `git commit` com mensagem clara e `git push` para a branch indicada pelo contexto

  

Notas:

- O passo 7 é obrigatório quando a mudança afeta artefatos implantados em produção.

- O passo 8 deve incluir pelo menos uma verificação funcional mínima (ex.: health check, smoke test ou execução de teste automatizado relevante).

  

---

  

## Versionamento Obrigatório

  

Ao finalizar qualquer alteração com versão no controle de código:

  

- trabalhar na branch indicada pelo contexto do projeto

- validar que a aplicação está funcionando corretamente

- executar `git commit` e `git push` conforme o repositório configurado

  

---

  

## Diretriz Operacional Explícita

  

Sempre que houver solicitação direta de operação (`rebuild`, `redeploy` ou ambos), executar imediatamente o fluxo definido pelo projeto atual, sem conditionais adicionais.

  

---

  

## Restrições

  

Nunca:

  

- assumir estrutura sem validar

- alterar sem analisar dependências

- deixar divergência entre código e `projects_memory.md`

- introduzir duplicidade de fluxo/lógica sem justificativa

- criar ou manter mais de uma cópia física deste documento como fonte de verdade

  

---

  

## Princípios de Entrega

  

Priorizar:

  

- clareza

- simplicidade

- baixo acoplamento

- observabilidade

- resiliência

- performance

- manutenibilidade

  

Ao propor soluções:

  

- justificar decisões

- explicitar trade-offs

- apontar riscos

- sugerir validações

  

---

  

## Sincronização com projetos downstream

  

Em cada repositório que adotar estas diretrizes:

  

- Arquivos de diretrizes dos agentes devem ser symlinks ou referências para este arquivo fonte

- Nenhum projeto deve manter uma cópia física divergente destas diretrizes

- Qualquer edição desses nomes downstream deve ser feita exclusivamente por substituição por symlink

  
  

## Modelo esperado para preenchimento do arquivo .prompts_location

  

CLAUDE_CONVERSATIONS_DIR="{PASTA_DO_USUARIO}/.claude/projects" - Aqui é a pasta do usuário, por exemplo /home/lucas, é onde fica o arquivo-base do claude.

CODEX_SESSIONS_DIR="{PASTA_DO_USUARIO}/.codex/sessions" - Aqui é a pasta do usuário, por exemplo /home/lucas, é onde fica o arquivo-base do claude.

HERMES_SESSIONS_DIR= Local onde o hermes salva o log dos prompts.

  

Não deve se limitar as IAs acima pois caso use uma não listada, ainda sim essa outra IA precisa reigstrar em prompts a localização dos prompts dela. O objetivo é fazer com que haja fluidez na migração de uma para a outra dentro do mesmo projeto.
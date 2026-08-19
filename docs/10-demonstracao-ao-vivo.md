# 10 — Demonstração ao vivo e validação assistida

Este roteiro combina validações locais, execuções reais do GitHub Actions e um
cenário vermelho isolado. O objetivo é mostrar o ciclo
**conforme → bloqueado → corrigido** sem criar segredos, commits de violação ou
alterações na branch `main` durante a apresentação.

## 1. Pré-requisitos

- Python 3.10 ou superior com `requirements.txt` e `requirements-dev.txt`
  instalados;
- Go disponível para executar o controlador interativo;
- GitHub CLI autenticado com acesso ao repositório;
- `compliance.yml` e `demo-compliance.yml` presentes na branch padrão;
- acesso à internet para os modos GitHub, release e pip-audit;
- capturas e [roteiro de contingência](../evidence/contingency/README.md)
  disponíveis caso a rede falhe.

Antes da apresentação, confirme:

```sh
gh auth status
python scripts/demo_validate.py local
go run scripts/github_live_demo.go
```

No programa Go, selecione primeiro a opção **1 — Verificar pré-requisitos**.

## 2. Validação local em Python

### 2.1 Pipeline local completo

```sh
python scripts/demo_validate.py local
```

O modo local executa:

1. pytest com relatório JUnit;
2. Ruff com relatório JSON;
3. pip-audit em modo estrito;
4. políticas internas;
5. contrato HTTP de `/` e `/health` pelo cliente de testes Flask;
6. links Markdown relativos;
7. `git diff --check`.

Os resultados são apresentados no terminal e gravados, por padrão, em
`reports/demo-summary.md`. O diretório `reports/` é ignorado pelo Git.

Se a apresentação estiver sem rede, ignore somente a consulta do pip-audit:

```sh
python scripts/demo_validate.py local --offline
```

### 2.2 Bloqueio local controlado

```sh
python scripts/demo_validate.py policy-failure
```

Esse modo cria os documentos obrigatórios e um arquivo `.env` vazio em um
diretório temporário. A demonstração é aprovada somente quando o validador
retorna código 1, identifica `.env` e informa `[ NÃO CONFORME ]`. O diretório é
removido automaticamente e o checkout não é alterado.

### 2.3 Evidências históricas

```sh
python scripts/demo_validate.py github
```

O modo consulta, sem refazer execuções, os runs usados no roteiro auditável:

| Momento | Run | Conclusão esperada |
| --- | ---: | --- |
| aprovação inicial | `31809146741` | success |
| bloqueio de segredo sintético | `31955024357` | failure |
| bloqueio de `.env` | `32040521363` | failure |
| aprovação após correção | `32062843662` | success |

### 2.4 Tag e release

```sh
python scripts/demo_validate.py release
```

Esse modo usa `gh` para confirmar que `v1.0.0` é uma tag anotada, resolve o SHA
entregue, verifica a GitHub Release final e procura um pipeline verde associado
ao mesmo commit.

## 3. Sequência ao vivo controlada em Go

Execute:

```sh
go run scripts/github_live_demo.go
```

O menu apresenta as operações abaixo:

```text
1. Verificar pré-requisitos (sem alterar o remoto)
2. Disparar pipeline oficial conforme (verde esperado)
3. Disparar bloqueio controlado (vermelho esperado)
4. Disparar cenário corrigido (verde esperado)
5. Acompanhar uma execução existente pelo RUN_ID
6. Listar execuções manuais recentes
7. Baixar artefatos de uma execução
8. Abrir uma execução no navegador
0. Sair
```

As opções 2, 3 e 4 pedem confirmação explícita antes de disparar um workflow.
Depois do dispatch, o programa:

1. compara a lista de runs anterior e posterior;
2. localiza o novo `RUN_ID`;
3. executa `gh run watch --compact`;
4. confere a conclusão observada;
5. oferece a abertura da execução no navegador.

Para outro fork ou branch padrão:

```sh
go run scripts/github_live_demo.go \
  -repo owner/repository \
  -ref main
```

## 4. Workflow vermelho isolado

O workflow `demo-compliance.yml` aceita somente dois cenários:

- `approved`: diretório temporário conforme e conclusão verde;
- `policy_failure`: `.env` vazio criado em diretório temporário e conclusão
  vermelha intencional.

O workflow:

- possui somente permissão `contents: read`;
- não usa secrets;
- não cria commits ou pushes;
- não está entre os checks obrigatórios do ruleset;
- limita a execução a cinco minutos;
- publica relatório com `run_id` e `run_attempt` por sete dias;
- identifica seu título como demonstração não bloqueante.

O vermelho desse workflow demonstra a reação do controle em tempo real. A prova
de que o GitHub impede integração não conforme continua sendo formada pelos
runs históricos de pull requests e pelo ruleset `main-protect`.

## 5. Ordem recomendada na apresentação

1. Mostrar o run histórico verde inicial.
2. Usar a opção 2 do programa Go e acompanhar o pipeline oficial atual.
3. Usar a opção 3 e abrir o log da detecção do `.env` temporário.
4. Explicar que o vermelho é esperado, isolado e não altera a `main`.
5. Usar a opção 4 e acompanhar o cenário corrigido até ficar verde.
6. Baixar ou abrir o artefato da demonstração.
7. Encerrar na tag, GitHub Release e `EVID-06`.

Não instale dependências, não crie uma violação real e não refaça os runs
canônicos durante a apresentação. Se o Actions atrasar ou a rede falhar, passe
imediatamente para o roteiro de contingência e preserve o tempo das falas.

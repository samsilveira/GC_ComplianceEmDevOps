# EVID-02 — Testes automatizados da API

## Escopo

Validação local da suíte pytest entregue na ISSUE-03 e vinculada à PR #15.

## Procedimento reproduzível

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
pytest
```

## Resultado da revisão

- Data: 2026-08-15.
- Ambiente: Python 3.14.6 e pytest 8.0.0.
- Instalação limpa das dependências concluída com sucesso.
- Três testes coletados e aprovados (`3 passed in 0.08s`).
- Relatório JUnit criado automaticamente em `reports/junit.xml`.
- Os testes usam apenas o cliente local do Flask e não acessam serviços externos.

## Falha controlada

A versão retornada pela rota `/` foi alterada temporariamente de `1.0.0` para `1.0.1` em uma cópia isolada do repositório. O teste `test_index_route` falhou com código de saída diferente de zero (`1 failed, 2 passed`). A alteração controlada não foi aplicada à branch.

Na validação local da ISSUE-04, foi acrescentado temporariamente um quarto teste com uma asserção falsa e executado o mesmo comando adotado pelo workflow:

```sh
python -m pytest --junitxml=reports/junit.xml
```

O pytest terminou com código `1`, identificou diretamente `test_controlled_failure_blocks_pipeline` e registrou `1 failed, 3 passed`. O arquivo temporário foi removido e a suíte conforme voltou a registrar `3 passed`. Isso confirma que uma regressão não é mascarada pelo step que publica o artefato.

## Execuções do GitHub Actions — ISSUE-04

| Momento | Commit | Resultado | Evidência |
| --- | --- | --- | --- |
| Pipeline conforme | `2e6dc46` | Os dois jobs concluíram com sucesso, usando Python 3.12 e as actions baseadas em Node.js 24 | [Execução 31911634784](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31911634784) |
| Falha controlada | `cae7a03` | O job de testes ficou vermelho no step **Executar testes e gerar relatório JUnit**; o step de publicação do JUnit concluiu com sucesso | [Execução 31911672486](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31911672486) |
| Restauração | `2dd7c1b` | O teste temporário foi removido e os dois jobs voltaram ao estado verde | [Execução 31911702227](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31911702227) |

## Limite desta evidência

Os resultados locais comprovam a reprodutibilidade do comando; os links acima são as evidências remotas do GitHub Actions. A revisão e o merge da branch `ci/pipeline-base` permanecem sujeitos ao pull request e à aprovação de Elder (P2).

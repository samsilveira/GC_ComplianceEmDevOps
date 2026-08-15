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

## Limite desta evidência

Esta é uma validação local. A execução automática da suíte, o bloqueio do job em caso de regressão e a publicação do JUnit pelo GitHub Actions pertencem à ISSUE-04.

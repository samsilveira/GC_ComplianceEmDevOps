# 09 — Registro de reprodução independente

## Objetivo

Confirmar que o experimento pode ser preparado e validado a partir de uma cópia limpa, usando somente as instruções versionadas no repositório.

## Ambiente

- Data: 18/08/2026 (UTC)
- Sistema: Linux
- Python: 3.12.1
- Origem: clone local do commit `2112592`, com as alterações da ISSUE-09 aplicadas antes do ensaio
- Ambiente virtual: `.venv`, sem acesso aos pacotes globais

## Procedimento executado

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m pytest
.venv/bin/ruff check .
.venv/bin/python -m pip_audit --requirement requirements.txt --strict
.venv/bin/python scripts/check_policies.py
```

Também foram feitas requisições com o cliente de testes do Flask para `/` e `/health`, evitando manter um servidor em segundo plano.

## Resultados

| Verificação | Resultado observado |
| --- | --- |
| instalação isolada | concluída com as versões fixadas |
| pytest | 16 testes aprovados; JUnit criado em `reports/junit.xml` |
| Ruff | `All checks passed!` |
| pip-audit | nenhuma vulnerabilidade conhecida encontrada |
| políticas internas | `[ CONFORME ]`, código de saída zero |
| `GET /` | HTTP 200, mensagem e versão `1.0.0` corretas |
| `GET /health` | HTTP 200, `status: up` e `healthy: true` |

Todos os comandos terminaram com sucesso. O ensaio foi executado por um agente independente das implementações das issues anteriores, seguindo exclusivamente os arquivos do repositório.

## Problemas e limitações

O pip-audit consulta bases externas; sua execução exige conectividade. O
resultado retrata as vulnerabilidades conhecidas na data do teste. Os relatórios
JUnit, Ruff e pip-audit devem ser consultados antes do fim da retenção de 14
dias; o SARIF do Gitleaks usa a retenção da ação, observada em 90 dias na
candidata.

Como `/tmp` e o workspace estavam em sistemas de arquivos diferentes, o clone local precisou da opção `--no-hardlinks`. Isso não afeta clones feitos por HTTPS. A primeira instalação não teve resolução DNS no ambiente restrito; repetida com acesso de rede autorizado, foi concluída sem mudanças nos arquivos de dependências.

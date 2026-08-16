# EVID-04 — Qualidade e Auditoria de Dependências

Este registro relaciona os controles da ISSUE-06 às saídas preservadas pelo pipeline.

## 1. Identificação

- **Issue:** #6
- **Responsável principal:** Manoel (P3) — `@Junio404`
- **Revisores:** Samuel (P1), Elder (P2) e Espedito (P5)
- **Branch de implementação:** `feat/qualidade-dependencias`
- **Versões:** `ruff==0.16.3` e `pip-audit==2.10.1`

## 2. Controles Bloqueantes

- `ruff check .`: bloqueia ao encontrar qualquer violação das regras configuradas em `pyproject.toml`.
- `pip-audit --requirement requirements.txt --strict`: bloqueia ao encontrar vulnerabilidade conhecida ou falha de coleta/resolução.
- Nenhum job usa `continue-on-error` ou supressão do código de saída.

## 3. Evidência da Execução Conforme

- **Validação local em 16/08/2026:** `ruff check .` aprovado, `pip-audit --requirement requirements.txt --strict` sem vulnerabilidades conhecidas e 3 testes aprovados.
- **Commit avaliado:** `PREENCHER APÓS O COMMIT`
- **Execução verde do GitHub Actions:** `PREENCHER APÓS O PUSH`
- **Artefato Ruff:** `relatorio-ruff-<run-id>` contendo `ruff.json`
- **Artefato pip-audit:** `relatorio-pip-audit-<run-id>` contendo `pip-audit.json`
- **Retenção configurada:** 14 dias

## 4. Exceções e Limitações

- **Exceções vigentes em 16/08/2026:** nenhuma.
- Não existem regras Ruff ignoradas por arquivo nem vulnerabilidades ignoradas com `--ignore-vuln`.
- O pip-audit consulta dados disponíveis no momento da execução; vulnerabilidades ainda não publicadas não podem ser detectadas.
- Indisponibilidade que impeça a coleta não é tratada como aprovação, pois a execução usa `--strict`.

Qualquer exceção futura deverá registrar o identificador afetado, justificativa, responsável e data limite de revisão antes de ser adicionada à configuração versionada.

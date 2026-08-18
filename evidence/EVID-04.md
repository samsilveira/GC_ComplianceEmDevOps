# EVID-04 — Qualidade e Auditoria de Dependências

Este registro relaciona os controles da ISSUE-06 às saídas preservadas pelo pipeline.

## 1. Identificação

- **Issue:** [#6](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/6)
- **Responsável principal:** Manoel (P3) — `@Junio404`
- **Revisores previstos na issue:** Samuel (P1), Elder (P2) e Espedito (P5)
- **Aprovação registrada no PR:** Elder (P2) — `@eldrayan`
- **Pull request de implementação:** [#18](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/18)
- **Branch de implementação efetiva:** `issue6`
- **Versões:** `ruff==0.16.3` e `pip-audit==2.10.1`

## 2. Controles Bloqueantes

- `ruff check .`: bloqueia ao encontrar qualquer violação das regras configuradas em `pyproject.toml`.
- `pip-audit --requirement requirements.txt --strict`: bloqueia ao encontrar vulnerabilidade conhecida ou falha de coleta/resolução.
- Nenhum job usa `continue-on-error` ou supressão do código de saída.

## 3. Evidência da Execução Conforme

- **Validação local em 16/08/2026:** `ruff check .` aprovado, `pip-audit --requirement requirements.txt --strict` sem vulnerabilidades conhecidas e 3 testes aprovados.
- **Commit avaliado:** [`13fea952581fe51b3acca8864723236f03e7e194`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/13fea952581fe51b3acca8864723236f03e7e194)
- **Execução verde do GitHub Actions:** [run `31968978387`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31968978387), executado para o mesmo commit avaliado
- **Artefato Ruff:** `relatorio-ruff-31968978387`, contendo `ruff.json` sem violações (`[]`)
- **Artefato pip-audit:** `relatorio-pip-audit-31968978387`, contendo `pip-audit.json` sem vulnerabilidades conhecidas nas dependências resolvidas
- **Artefato de testes:** `relatorio-junit-31968978387`, contendo o resultado dos 3 testes aprovados
- **Merge na `main`:** [`e1a864f0f0f7238b82a72f1d05bc16287f0274c7`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/e1a864f0f0f7238b82a72f1d05bc16287f0274c7)
- **Retenção configurada:** 14 dias

## 4. Correção da Rastreabilidade após o Merge

- **Pull request corretivo:** [#19](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/19)
- **Branch corretiva:** `docs/corrige-evidencias-issue6`
- **Commit corretivo avaliado:** [`67859574c2c500cb2e3777b0df7eab705475c14d`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/67859574c2c500cb2e3777b0df7eab705475c14d)
- **Execução verde do pull request corretivo:** [run `31970378390`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31970378390), executado para o mesmo commit corretivo
- **Artefatos publicados:** `relatorio-ruff-31970378390`, `relatorio-pip-audit-31970378390`, `relatorio-junit-31970378390` e `gitleaks-results.sarif`
- **HEAD final da correção:** [`eb768dcd69756500694b2d4485ae653921ea8a7b`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/eb768dcd69756500694b2d4485ae653921ea8a7b)
- **Execução verde do HEAD final:** [run `31970482482`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31970482482), com os cinco jobs então existentes aprovados
- **Escopo:** somente `evidence/EVID-04.md` e `evidence/README.md`; a implementação funcional validada no PR #18 não foi alterada.

## 5. Exceções e Limitações

- **Exceções vigentes em 16/08/2026:** nenhuma.
- Não existem regras Ruff ignoradas por arquivo nem vulnerabilidades ignoradas com `--ignore-vuln`.
- O pip-audit consulta dados disponíveis no momento da execução; vulnerabilidades ainda não publicadas não podem ser detectadas.
- Indisponibilidade que impeça a coleta não é tratada como aprovação, pois a execução usa `--strict`.
- A branch original foi publicada como `issue6`, fora dos prefixos definidos em `CONTRIBUTING.md`. Como o PR #18 já havia sido incorporado, o histórico não foi reescrito; esta correção documental foi isolada na branch conforme `docs/corrige-evidencias-issue6`.

Qualquer exceção futura deverá registrar o identificador afetado, justificativa, responsável e data limite de revisão antes de ser adicionada à configuração versionada.

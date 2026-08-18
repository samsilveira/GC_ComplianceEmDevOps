# 07 — Trilha de Auditoria e Rastreabilidade

Este documento detalha o histórico de decisões, rastreabilidade de commits, aprovação de pull requests e ciclo de releases.

---

## 1. Rastreabilidade de Alterações

Todas as mudanças do projeto são vinculadas a:
- Issue específica no GitHub
- Branch de curta duração
- Pull Request com revisão por pares
- Execução auditável no GitHub Actions
- Registro no `CHANGELOG.md` e tag semântica

---

## 2. Controles e fontes de auditoria

| Informação | Fonte |
| --- | --- |
| autoria e conteúdo da alteração | histórico Git |
| motivação e aceite | issue e pull request |
| revisão humana | review do pull request |
| resultado automatizado | run do GitHub Actions |
| relatórios técnicos | artefatos JUnit, Ruff e pip-audit |
| demonstrações controladas | `evidence/EVID-*.md` |
| relação política-evidência | `evidence/POLICY-MAP.md` |

## 3. Retenção e integridade

Os artefatos têm retenção de 14 dias. Os documentos locais registram URLs, números de execução e SHAs, relacionando o resultado ao commit mesmo depois da expiração. Segredos detectados não são reproduzidos; as demonstrações usam somente valores sintéticos.

## 4. Estado da release `v1.0.0`

A release ainda não foi publicada. A consolidação de tag, notas, changelog e evidência `EVID-06` pertence à ISSUE-10. Até lá, o `CHANGELOG.md` mantém as alterações em `Unreleased`, e a POL-06 permanece um controle humano não automatizado.

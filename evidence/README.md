# Trilha de Evidências — Compliance em DevOps

Este diretório é o índice central e o repositório de evidências auditáveis geradas durante a execução do experimento de Compliance as Code em Pipelines CI/CD.

---

## 📂 Organização das Evidências

As evidências do projeto estão estruturadas para comprovar os três momentos fundamentais do experimento:

1. **Momento 1 — Pipeline Conforme (Aprovado):**
   - Execução completa com testes passando, lint validado, sem segredos e dependências auditadas.
2. **Momento 2 — Bloqueio por Violação Controlada:**
   - Detecção de segredo fictício com Gitleaks.
   - Violação de políticas com `check_policies.py`.
3. **Momento 3 — Aprovação após Correção:**
   - Remoção das violações e restauração do pipeline em estado verde.

---

## 📋 Catálogo de Artefatos e Execuções

| ID da Evidência | Controle Demonstrado | Tipo de Registro | Commit / Run | Responsável |
| :--- | :--- | :--- | :--- | :--- |
| `EVID-01` | Fundação e estrutura inicial | PR e log do CI | [PR #13](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/13) / [workflow aprovado](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31809146741) — commit `78bfade` | Samuel (P1) |
| `EVID-02` | Execução de testes automatizados | Relatório JUnit (`reports/junit.xml`) | [Validação local](EVID-02.md) / [PR #15](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/15) | Elder (P2) |
| `EVID-03` | Bloqueio por detecção de segredos | Log do Gitleaks (falha controlada) | *A vincular na ISSUE-05* | Manoel (P3) |
| `EVID-04` | Auditoria de dependências | Relatório pip-audit e Ruff | *A vincular na ISSUE-06* | Manoel (P3) |
| `EVID-05` | Bloqueio por política interna | Log do `scripts/check_policies.py` | *A vincular na ISSUE-07* | Sabrina (P4) |
| `EVID-06` | Trilha de auditoria e release | Tag `v1.0.0` e changelog | *A vincular na ISSUE-10* | Sabrina (P4) / Sebastião (P7) |

---

> [!NOTE]
> A catalogação e manutenção detalhada deste índice é atribuição da **ISSUE-08** conduzida por Pedro Yan (P6) sob supervisão técnica de Samuel (P1).

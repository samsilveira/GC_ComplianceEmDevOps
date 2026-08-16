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
| `EVID-02` | Execução de testes automatizados | Relatório JUnit e logs do CI | [Registro completo](EVID-02.md) / [execução verde](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31911702227) / [falha controlada](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31911672486) / [PR #15](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/15) / [PR #16](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/16) | Elder (P2) / Samuel (P1) |
| `EVID-03` | Bloqueio por detecção de segredos | Log e SARIF do Gitleaks | [Registro completo](EVID-03.md) / [execução vermelha](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31955024357) / [execução verde](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31955499109) / [PR #17](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/17) | Manoel (P3) |
| `EVID-04` | Qualidade e auditoria de dependências | Relatórios JSON do Ruff e pip-audit | [Registro completo](EVID-04.md) / [PR #18](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/18) e [run da implementação](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31968978387) — commit `13fea95` / [PR corretivo #19](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/19) e [run corretivo](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31970378390) — commit `6785957` | Manoel (P3) |
| `EVID-05` | Bloqueio por política interna | Log do `scripts/check_policies.py` | *A vincular na ISSUE-07* | Sabrina (P4) |
| `EVID-06` | Trilha de auditoria e release | Tag `v1.0.0` e changelog | *A vincular na ISSUE-10* | Sabrina (P4) / Sebastião (P7) |

---

> [!NOTE]
> A catalogação e manutenção detalhada deste índice é atribuição da **ISSUE-08** conduzida por Pedro Yan (P6) sob supervisão técnica de Samuel (P1).

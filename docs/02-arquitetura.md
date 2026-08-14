# 02 — Arquitetura do Experimento

Este documento descreve a arquitetura técnica, fluxo de execução do pipeline e os pontos de controle de conformidade.

---

## 1. Visão Geral da Arquitetura

O sistema é composto por:
1. **Aplicação Alvo (`app/`):** API Python (Flask) com rotas deterministicas e healthcheck.
2. **Suíte de Testes (`tests/`):** Testes unitários com Pytest e geração de relatórios JUnit.
3. **Controles de Conformidade e Segurança:**
   - Detecção de segredos: **Gitleaks**
   - Lint de código: **Ruff**
   - Auditoria de vulnerabilidades em dependências: **pip-audit**
   - Validação de políticas de repositório: **`scripts/check_policies.py`**
4. **Motor de CI/CD:** GitHub Actions (`.github/workflows/compliance.yml`).
5. **Trilha de Auditoria e Evidências:** `evidence/` e GitHub Releases.

# 04 — Políticas Organizacionais e Matriz de Controles

Este documento formaliza as políticas de conformidade do experimento e sua respectiva correspondência com controles automatizados e evidências.

---

## 1. Matriz de Políticas e Controles

| ID da Política | Descrição da Regra | Controle / Ferramenta | Evidência Gerada | Bloqueante? |
| :--- | :--- | :--- | :--- | :--- |
| **POL-01** | Toda alteração deve passar por testes automatizados sem falhas | `pytest` com saída JUnit | `reports/junit.xml` | Sim |
| **POL-02** | Proibido comitar segredos, chaves de API e arquivos `.env` | `gitleaks` + `check_policies.py` | Log de scan no CI | Sim |
| **POL-03** | Código deve atender às regras de lint configuradas | `ruff check .` | `reports/ruff.json` | Sim |
| **POL-04** | Dependências em produção não podem ter vulnerabilidades conhecidas | `pip-audit --requirement requirements.txt --strict` | `reports/pip-audit.json` | Sim |
| **POL-05** | Repositório deve conter documentação e governança obrigatória | `scripts/check_policies.py` | Log do script de políticas | Sim |
| **POL-06** | Toda release oficial deve ter tag semântica, notas e changelog | GitHub Releases + `CHANGELOG.md` | Tag `v1.0.0` e release note | Sim |

---

> [!NOTE]
> O detalhamento completo e a implementação do script validador são conduzidos na **ISSUE-07** sob responsabilidade de Sabrina Alencar (P4).

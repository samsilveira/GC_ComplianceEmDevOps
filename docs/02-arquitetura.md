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

## 2. Fluxo do pipeline

```text
push / pull request
        |
        v
foundation-check ---------> policy-check
        |
        v
secret-scan
        |
        +---------> code-quality (Ruff) ---------+
        |                                         |
        +---------> dependency-audit (pip-audit) +--> api-tests (pytest)
```

`foundation-check` é a porta de entrada. A verificação de políticas segue em paralelo ao ramo de segurança. O Gitleaks precisa aprovar a alteração antes de Ruff e pip-audit; ambos precisam terminar com sucesso para liberar os testes. Uma falha em qualquer job torna o workflow não conforme.

## 3. Entradas e saídas

| Componente | Entrada | Saída auditável |
| --- | --- | --- |
| Fundação | árvore do repositório | log de itens obrigatórios |
| Políticas | árvore do repositório | log e código de saída do script |
| Gitleaks | conteúdo e intervalo Git do evento | resumo e artefato quando aplicável |
| Ruff | arquivos Python | `reports/ruff.json` |
| pip-audit | `requirements.txt` | `reports/pip-audit.json` |
| pytest | aplicação e testes | `reports/junit.xml` |

Os artefatos são publicados por 14 dias. Os registros Markdown preservam os identificadores de commit e run depois que os artefatos expiram.

## 4. Aplicação alvo

A aplicação não possui persistência nem dependências externas. `GET /` expõe a mensagem e a versão; `GET /health` retorna um estado fixo. Essa simplicidade mantém o foco nos controles do pipeline.

# 04 — Políticas Organizacionais e Matriz de Controles

> **Aviso Legal:** Este documento e os controles aqui descritos têm fins puramente acadêmicos e experimentais. Nenhuma afirmação contida neste repositório sugere ou garante conformidade integral com normas legais reais (como LGPD, GDPR) ou certificações de mercado (como ISO 27001, SOC 2).

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

## 2. Automação vs. Revisão Humana

Para garantir eficiência sem perder o controle de qualidade, nossas políticas são divididas em processos automatizados e manuais.

### O que é Automatizado (Controles Técnicos)
- **Verificação de Estrutura:** Validação da presença da fundação do repositório e arquivos essenciais (como `README.md` e `CHANGELOG.md`) pelo script customizado.
- **Auditoria de Código e Dependências:** Execução do Ruff e do pip-audit a cada novo commit via GitHub Actions.
- **Prevenção de Vazamentos:** Varredura do Gitleaks e script de bloqueio de arquivos proibidos para evitar exposição acidental de credenciais.

### O que depende de Revisão Humana (Controles Administrativos)
- **Aprovação de Pull Requests:** Nenhuma alteração entra na branch `main` (produção) sem a revisão e aprovação (Code Review) da equipe.
- **Decisões de Arquitetura e Modelagem:** Inclusão de novas ferramentas, aplicação de princípios arquiteturais (como SOLID) ou mudanças em esquemas de banco de dados (como modelagem no SQLite).
- **Tratamento de Falsos Positivos:** Avaliação humana quando as ferramentas de segurança ou qualidade barrarem código seguro por engano.

---

> [!NOTE]
> O detalhamento completo e a implementação do script validador são conduzidos na **ISSUE-07** sob responsabilidade de Sabrina Alencar.

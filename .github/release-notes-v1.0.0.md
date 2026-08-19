# v1.0.0 — Compliance as Code

## Resumo

Primeira versão estável do experimento de Compliance as Code. A entrega reúne
uma API Flask mínima e um pipeline bloqueante que aplica controles de testes,
qualidade, segredos, dependências, documentação e políticas internas, com uma
trilha auditável de aprovação, violação controlada e correção.

## Principais mudanças

- API com rotas `/` e `/health` e suíte automatizada em pytest.
- Workflow de conformidade executado em pull requests, branches e tags SemVer.
- Gitleaks, Ruff, pip-audit e validação própria de políticas como controles bloqueantes.
- Relatórios JUnit/JSON/SARIF publicados como artefatos temporários.
- Catálogo permanente em [`evidence/`](https://github.com/samsilveira/GC_ComplianceEmDevOps/tree/v1.0.0/evidence) e matriz de
  políticas em [`POLICY-MAP.md`](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.0.0/evidence/POLICY-MAP.md).
- Reprodução independente registrada na
  [documentação](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.0.0/docs/09-reproducao-independente.md).

O detalhamento integral está no [`CHANGELOG.md`](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.0.0/CHANGELOG.md).

## Limitações conhecidas

- O escopo é educacional: não há autenticação, banco de dados, implantação em
  produção ou observabilidade.
- O pip-audit depende da conectividade e das vulnerabilidades conhecidas no instante da execução.
- Artefatos do GitHub Actions expiram após 14 dias; os registros Markdown
  preservam os identificadores essenciais, mas não substituem todo o conteúdo
  dos relatórios expirados.

## Reprodução

Requer Git, Python 3.10 ou superior e `pip` (Python 3.12 é a referência do CI).

```sh
git clone https://github.com/samsilveira/GC_ComplianceEmDevOps.git
cd GC_ComplianceEmDevOps
git checkout v1.0.0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
ruff check .
pip-audit --requirement requirements.txt --strict
python scripts/check_policies.py
```

No Windows, use `.venv\Scripts\Activate.ps1` para ativar o ambiente. O roteiro
detalhado está em [`docs/05-como-executar.md`](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.0.0/docs/05-como-executar.md).

## Auditoria

- [Trilha da release](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.0.0/docs/07-auditoria.md)
- [Evidência final](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.0.0/evidence/EVID-06.md)
- [Pipeline da tag](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/workflows/compliance.yml?query=branch%3Av1.0.0)

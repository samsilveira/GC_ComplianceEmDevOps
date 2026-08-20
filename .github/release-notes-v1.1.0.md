# v1.1.0 — Live Demo & Assisted Validation

## Resumo

Versão de entrega com demonstração interativa ao vivo e validação assistida de conformidade. Esta release incorpora o controlador interativo em Go para o GitHub Actions, o script Python de validação assistida para apresentação e os cenários controlados de conformidade, consolidando a entrega com documentação e evidências completas.

## Principais mudanças

- **Demonstração ao Vivo:**
  - Controlador interativo em Go (`scripts/github_live_demo.go`) para disparo e acompanhamento de workflows no terminal.
  - Script assistido de validação local e diagnóstico (`scripts/demo_validate.py`) com suíte de testes (`tests/test_demo_validate.py`).
  - Workflow de cenários controlados de conformidade (`.github/workflows/demo-compliance.yml`).
  - Documentação do roteiro de apresentação em [`docs/10-demonstracao-ao-vivo.md`](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.1.0/docs/10-demonstracao-ao-vivo.md).
- **Evidências e Auditoria:**
  - Validação pós-publicação e consolidação final do registro permanente [`evidence/EVID-06.md`](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.1.0/evidence/EVID-06.md).
  - Alinhamento da matriz de rastreabilidade e referências em [`docs/07-auditoria.md`](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.1.0/docs/07-auditoria.md).

O detalhamento integral está no [`CHANGELOG.md`](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.1.0/CHANGELOG.md).

## Reprodução

Requisitos: Git, Python 3.10+, Go (opcional para o controlador interativo) e GitHub CLI.

```sh
git clone https://github.com/samsilveira/GC_ComplianceEmDevOps.git
cd GC_ComplianceEmDevOps
git checkout v1.1.0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
python scripts/demo_validate.py local
```

## Auditoria e Evidências

- [Trilha de Auditoria](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.1.0/docs/07-auditoria.md)
- [Catálogo de Evidências](https://github.com/samsilveira/GC_ComplianceEmDevOps/tree/v1.1.0/evidence)
- [Demonstração ao Vivo](https://github.com/samsilveira/GC_ComplianceEmDevOps/blob/v1.1.0/docs/10-demonstracao-ao-vivo.md)

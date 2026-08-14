# 05 — Guia de Execução e Reprodutibilidade

Este guia orienta qualquer desenvolvedor ou auditor a configurar o ambiente e executar os testes e verificações localmente a partir de um clone limpo.

---

## 1. Pré-requisitos

- Git instalado
- Python 3.10 ou superior
- `pip` e ambiente virtual `venv`

---

## 2. Passo a Passo

### 2.1 Clonar o Repositório

```bash
git clone https://github.com/samsilveira/GC_ComplianceEmDevOps.git
cd GC_ComplianceEmDevOps
```

### 2.2 Criar e Ativar o Ambiente Virtual

No Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2.3 Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 2.4 Executar Comandos de Validação

```bash
# Iniciar a API Flask (quando implementada na ISSUE-02)
flask --app app.main run

# Executar suíte de testes (ISSUE-03)
pytest

# Executar lint (ISSUE-06)
ruff check .

# Executar checagem de políticas (ISSUE-07)
python scripts/check_policies.py
```

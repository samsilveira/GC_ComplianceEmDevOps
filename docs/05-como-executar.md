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
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

`requirements.txt` contém as dependências da API. `requirements-dev.txt` contém o pytest e será ampliado nas issues posteriores com as ferramentas de qualidade e segurança.

### 2.4 Iniciar a API

```bash
flask --app app.main run
```

### 2.5 Executar os Testes

```bash
pytest
```

Uma execução conforme termina com código de saída zero e cria o relatório JUnit em `reports/junit.xml`. O diretório `reports/` é ignorado pelo Git; a publicação do relatório como artefato do pipeline será configurada na ISSUE-04.

### 2.6 Executar os Controles Posteriores

Após a integração das respectivas issues, os demais controles poderão ser executados com:

```bash
# Executar lint (ISSUE-06)
ruff check .

# Executar checagem de políticas (ISSUE-07)
python scripts/check_policies.py
```

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

Uma execução conforme termina com código de saída zero e cria o relatório JUnit em `reports/junit.xml`. O diretório `reports/` é ignorado pelo Git. No GitHub Actions, o workflow usa Python 3.12 como versão de referência e publica esse relatório como o artefato `relatorio-junit-<run-id>`.

### 2.6 Verificar o Scan de Segredos no Pipeline

O job `Varredura de Segredos` executa automaticamente no workflow `Compliance Pipeline` em todo `push` e `pull_request`, usando a configuracao versionada em [`.gitleaks.toml`](../.gitleaks.toml).

Para demonstrar o bloqueio de forma segura, use apenas o segredo falso abaixo em um commit temporario do branch de trabalho:

```text
GC_DEMO_SECRET="<valor-falso-controlado>"
```

Use um valor no formato `gc-demo-secret-XXXXXXXXXXXX`, substituindo `XXXXXXXXXXXX` por 12 caracteres maiusculos e/ou digitos apenas no commit temporario de violacao.

Procedimento recomendado para a demonstracao controlada:

1. Adicione uma violacao temporaria em um arquivo descartavel, como `controlled-violation-demo.txt`, contendo somente a string falsa acima.
2. Faça um commit e envie o branch para disparar uma execucao vermelha do workflow.
3. Registre o SHA do commit e a URL da execucao em [`evidence/EVID-03.md`](../evidence/EVID-03.md).
4. Remova o arquivo de demonstracao no commit seguinte e envie novamente o branch.
5. Registre o SHA da correcao e a URL da nova execucao verde no mesmo arquivo de evidencia.

Preserve os dois commits no historico do branch. Nao use `commit --amend` nem force push nessa demonstracao, pois a reescrita rompe a cadeia direta entre violacao, correcao e execucoes do pipeline.

> **Importante:** nao use credenciais reais, nao use arquivos `.env` para a demonstracao e nao deixe o arquivo de violacao presente no estado final do branch.

### 2.7 Executar os Controles Posteriores

Após a integração das respectivas issues, os demais controles poderão ser executados com:

```bash
# Executar lint (ISSUE-06)
ruff check .

# Executar checagem de políticas (ISSUE-07)
python scripts/check_policies.py
```

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

`requirements.txt` contém as dependências de execução da API. `requirements-dev.txt` contém pytest, Ruff e pip-audit com versões fixadas.

### 2.4 Iniciar a API

```bash
flask --app app.main run
```

Em outro terminal, valide as respostas:

```bash
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/health
```

São esperados objetos JSON com `version: "1.0.0"` na primeira rota e `status: "up"` e `healthy: true` na segunda.

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

### 2.7 Executar Ruff e pip-audit

Execute os mesmos controles bloqueantes usados pelo GitHub Actions:

```bash
ruff check .
pip-audit --requirement requirements.txt --strict
```

Uma execução conforme encerra ambos os comandos com código de saída zero. Para também preservar os resultados locais em JSON:

```bash
mkdir -p reports
ruff check . --output-format=json --output-file=reports/ruff.json
pip-audit --requirement requirements.txt --strict \
  --format=json --output=reports/pip-audit.json
```

As violações das regras Ruff configuradas, as vulnerabilidades conhecidas e as falhas de coleta do pip-audit são bloqueantes. Nenhum código de saída é suprimido. Não existem exceções vigentes para a ISSUE-06.

### 2.8 Executar as políticas internas

```bash
python scripts/check_policies.py
```

O comando deve imprimir `[ CONFORME ]` e encerrar com código zero. Ele exige `README.md`, `CHANGELOG.md` e `docs/04-politicas.md`, e rejeita arquivos chamados `.env` ou `credentials.json` fora dos metadados `.git`.

### 2.9 Verificar os Artefatos no GitHub Actions

No workflow **Compliance Pipeline**, verifique os jobs **Qualidade de Código com Ruff** e **Auditoria de Dependências com pip-audit**. Ao final de cada execução não cancelada, baixe os artefatos `relatorio-ruff-<run-id>` e `relatorio-pip-audit-<run-id>`, retidos por 14 dias.

## 3. Versões reproduzíveis

| Item | Versão |
| --- | --- |
| Python local mínimo | 3.10 |
| Python de referência no CI | 3.12 |
| Flask | 3.1.3 |
| Werkzeug | 3.1.6 |
| pytest | 8.0.0 |
| Ruff | 0.16.3 |
| pip-audit | 2.10.1 |

As fontes de verdade são `requirements.txt`, `requirements-dev.txt`, `pyproject.toml` e `.github/workflows/compliance.yml`.

## 4. Reprodução verificada

O ensaio independente, incluindo ambiente, comandos, resultados e limitações, está em [`09-reproducao-independente.md`](09-reproducao-independente.md).

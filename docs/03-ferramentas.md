# 03 — Escolha de Ferramentas e Tecnologias

Este documento justifica as tecnologias adotadas, suas vantagens e suas limitações operacionais.

---

## 1. Matriz de Tecnologias

| Ferramenta | Categoria | Finalidade no Experimento | Vantagens | Limitações Conhecidas |
| :--- | :--- | :--- | :--- | :--- |
| **Flask** | Framework Web | Aplicação mínima alvo de conformidade | Leve, determinístico, inicialização rápida | Não possui ORM ou auth nativos |
| **pytest** | Testes | Validação de comportamento da API | Suporte nativo a JUnit XML, extensível | Requer isolamento adequado em testes complexos |
| **Ruff** | Linter / Formatador | Verificação estática de regras e boas práticas | Extremamente veloz (Rust), substitui múltiplos linters | Foco em regras estáticas padrão Python |
| **Gitleaks** | Scanner de Segredos | Detecção de credenciais em código e histórico | Regras regex especializadas, suporte a CI | Pode gerar falsos positivos se expressões forem amplas |
| **pip-audit** | Auditoria de Segurança | Varredura de CVEs em dependências Python | Consulta base oficial PyPA / OSV | Depende de conectividade com a base de vulnerabilidades |
| **Python Script (`check_policies.py`)** | Políticas Internas | Validação de governança e arquivos obrigatórios | Customização total para políticas do projeto | Requer manutenção e testes próprios |
| **GitHub Actions** | Orquestrador CI/CD | Execução automatizada e publicação de artefatos | Integração nativa com PRs, logs auditáveis | Limitações de runners públicos e quotas |

## 2. Registro da Integração do Gitleaks

- **Versão adotada da integração:** `gitleaks/gitleaks-action@v3.0.0`, fixada no commit `e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e` para evitar alterações inesperadas em tags mutáveis.
- **Runtime da action:** Node.js 24, sem habilitar runtimes depreciados no runner.
- **Forma de integração:** job `secret-scan` no workflow [`.github/workflows/compliance.yml`](../.github/workflows/compliance.yml), executado automaticamente em `push` e `pull_request` antes do job de testes.
- **Configuração versionada no repositório:** [`.gitleaks.toml`](../.gitleaks.toml) com `useDefault = true`, preservando as regras padrão do Gitleaks e adicionando apenas a regra `gc-demo-secret` para a demonstração segura da ISSUE-05.
- **Saídas de auditoria:** resumo no job do GitHub Actions e upload do artefato de relatório do Gitleaks quando houver detecção.

## 3. Falsos Positivos, Exceções e Limitações

- **Falsos positivos:** o Gitleaks trabalha com regras baseadas em padrões e entropia, portanto strings sintéticas ou fixtures de teste podem ser sinalizadas se se parecerem com credenciais reais.
- **Exceções nesta issue:** nenhuma allowlist ou `.gitleaksignore` foi adicionada, para evitar mascarar vazamentos durante a demonstração da política.
- **Tratamento recomendado para exceções futuras:** qualquer falso positivo deve ser revisado manualmente e, se confirmado, documentado com justificativa antes de incluir uma exclusão versionada.
- **Cobertura:** o job varre o checkout com `fetch-depth: 0`, cobrindo o conteúdo versionado e o histórico disponibilizado ao runner, mas não substitui proteções para segredos injetados apenas em runtime fora do Git.

## 4. Registro do Ruff e do pip-audit

- **Versões adotadas:** `ruff==0.16.3` e `pip-audit==2.10.1`, fixadas em [`requirements-dev.txt`](../requirements-dev.txt).
- **Configuração do Ruff:** [`pyproject.toml`](../pyproject.toml) fixa a versão requerida, Python mínimo `3.10`, limite de 88 caracteres e as famílias de regras `E4`, `E7`, `E9`, `F` e `I`.
- **Escopo do Ruff:** todos os arquivos Python encontrados a partir da raiz por `ruff check .`.
- **Escopo do pip-audit:** somente as dependências de execução declaradas em [`requirements.txt`](../requirements.txt), usando `--strict` para também bloquear falhas na coleta ou resolução das dependências.
- **Saídas de auditoria:** os jobs geram `reports/ruff.json` e `reports/pip-audit.json`, publicados como artefatos por 14 dias.

## 5. Resultados Bloqueantes e Exceções da ISSUE-06

- Qualquer regra Ruff selecionada que resulte em código de saída diferente de zero bloqueia o pipeline.
- Qualquer vulnerabilidade conhecida retornada pelo pip-audit bloqueia o pipeline. Uma falha de coleta ou resolução também bloqueia por causa de `--strict`.
- Os jobs não usam `continue-on-error` e os comandos não suprimem códigos de saída.
- **Exceções vigentes em 16/08/2026:** nenhuma. Não há `ignore`, `per-file-ignores` nem `--ignore-vuln` configurados para estes controles.
- Uma exceção futura somente poderá ser adicionada de forma explícita, registrando identificador da regra ou vulnerabilidade, justificativa, responsável e data limite de revisão. A exclusão deverá aparecer tanto na configuração versionada quanto neste documento; exceções sem prazo não são aceitas.

## 6. Limitações da Auditoria de Dependências

- O resultado representa a base de vulnerabilidades disponível no momento da execução e não garante ausência de falhas ainda desconhecidas ou ainda não publicadas.
- A auditoria depende de conectividade com o índice e com o serviço de vulnerabilidades. Como `--strict` está ativo, indisponibilidade que impeça a coleta não produz aprovação silenciosa.
- Dependências de desenvolvimento não fazem parte da política POL-04; o arquivo auditado é explicitamente `requirements.txt`, que representa as dependências de execução da API.

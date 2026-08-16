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

## 3. Falsos Positivos, Excecoes e Limitacoes

- **Falsos positivos:** o Gitleaks trabalha com regras baseadas em padrões e entropia, portanto strings sintéticas ou fixtures de teste podem ser sinalizadas se se parecerem com credenciais reais.
- **Exceções nesta issue:** nenhuma allowlist ou `.gitleaksignore` foi adicionada, para evitar mascarar vazamentos durante a demonstração da política.
- **Tratamento recomendado para exceções futuras:** qualquer falso positivo deve ser revisado manualmente e, se confirmado, documentado com justificativa antes de incluir uma exclusão versionada.
- **Cobertura:** `fetch-depth: 0` disponibiliza o histórico ao runner, enquanto a action seleciona o intervalo de commits de acordo com o evento (`push` ou `pull_request`). Essa configuração verifica as alterações selecionadas pela action, mas não deve ser apresentada como uma auditoria periódica de todo o histórico nem como proteção para segredos injetados apenas em runtime fora do Git.

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

## 2. Registro da Integracao do Gitleaks

- **Versao adotada da integracao:** `gitleaks/gitleaks-action@v2.3.9`.
- **Forma de integracao:** job `secret-scan` no workflow [`.github/workflows/compliance.yml`](../.github/workflows/compliance.yml), executado automaticamente em `push` e `pull_request` antes do job de testes.
- **Configuracao versionada no repositorio:** [`.gitleaks.toml`](../.gitleaks.toml) com `useDefault = true`, preservando as regras padrao do Gitleaks e adicionando apenas a regra `gc-demo-secret` para a demonstracao segura da ISSUE-05.
- **Saidas de auditoria:** resumo no job do GitHub Actions e upload do artefato de relatorio do Gitleaks quando houver deteccao.

## 3. Falsos Positivos, Excecoes e Limitacoes

- **Falsos positivos:** o Gitleaks trabalha com regras baseadas em padroes e entropia, portanto strings sinteticas ou fixtures de teste podem ser sinalizadas se se parecerem com credenciais reais.
- **Excecoes nesta issue:** nenhuma allowlist ou `.gitleaksignore` foi adicionada, para evitar mascarar vazamentos durante a demonstracao da politica.
- **Tratamento recomendado para excecoes futuras:** qualquer falso positivo deve ser revisado manualmente e, se confirmado, documentado com justificativa antes de incluir uma exclusao versionada.
- **Cobertura:** o job varre o checkout com `fetch-depth: 0`, cobrindo o conteudo versionado e o historico disponibilizado ao runner, mas nao substitui protecoes para segredos injetados apenas em runtime fora do Git.

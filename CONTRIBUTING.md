# Guia de Contribuição e Governança do Repositório

Este documento estabelece as convenções de desenvolvimento, governança de branches, padrões de commit, fluxo de pull requests e a Definição de Pronto (DoD) para o projeto **Compliance em DevOps**.

---

## 1. Estrutura da Equipe e Responsabilidades

Cada integrante possui um papel (`P1` a `P7`) com responsabilidades bem delimitadas para garantir a rastreabilidade e a independência das frentes:

| Papel | Integrante | GitHub | Frente Principal | Responsabilidade |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | Samuel Wagner Tiburi Silveira | [@samsilveira](https://github.com/samsilveira) | Repositório, CI, integração e entrega final | Fundação, workflow principal, integrações de PRs e release |
| **P2** | Elder Rayan Oliveira Silva | [@eldrayan](https://github.com/eldrayan) | Aplicação e testes | API Flask (`app/`) e suíte de testes (`tests/`) |
| **P3** | Manoel Junio Duarte da Silva | [@Junio404](https://github.com/Junio404) | Segurança e dependências | Gitleaks, pip-audit, Ruff e segurança de dependências |
| **P4** | Sabrina Alencar Soares | [@sabrinaalencaar](https://github.com/sabrinaalencaar) | Políticas e auditoria | Políticas organizacionais, `scripts/check_policies.py` e matriz |
| **P5** | Espedito Ramom Mascena Ricarto | [@RamomRicarto](https://github.com/RamomRicarto) | Documentação e reprodutibilidade | Guias técnicos (`docs/`) e validação de clone limpo |
| **P6** | Pedro Yan Alcantara Palácio | [@pedropalacioo](https://github.com/pedropalacioo) | Coleta e organização de evidências | Catalogação de evidências (`evidence/`), capturas e contingência |
| **P7** | Sebastião Sousa Soares | [@SebastiaoSoares](https://github.com/SebastiaoSoares) | Auditoria, release e apresentação | Auditoria final, apoio a release e roteiro de apresentação |

> **Nota de Governança sobre P6:** Pedro Yan (P6) atua exclusivamente sobre arquivos e execuções previamente produzidos e aprovados pelos responsáveis técnicos. Não é revisor de issues/PRs e não altera arquivos de CI, políticas ou segurança.

---

## 2. Padrão de Branches

O desenvolvimento deve ser realizado em **branches curtas**, criadas a partir da branch principal `main` atualizada.

### 2.1 Prefixos Obrigatórios

| Prefixo | Finalidade | Exemplo |
| :--- | :--- | :--- |
| `feat/` | Implementação de nova funcionalidade ou política | `feat/aplicacao`, `feat/politicas` |
| `test/` | Criação ou melhoria de testes automatizados | `test/testes-api` |
| `ci/` | Configuração ou expansão de pipelines e workflows | `ci/pipeline-base` |
| `docs/` | Criação ou atualização de documentação e evidências | `docs/documentacao`, `docs/evidencias` |
| `chore/` | Tarefas de manutenção, estrutura, tags ou releases | `chore/estrutura-inicial`, `chore/release-v1.0.0` |
| `fix/` | Correção de defeito ou falha em código existente | `fix/ajuste-rota-health` |

### 2.2 Regras de Branches

1. **Nunca realizar commits diretos na `main`** para código funcional de issues.
2. Toda branch deve ser derivada da versão mais recente de `main`.
3. Uma branch deve corresponder a apenas uma issue de cada vez.
4. Após o merge do Pull Request, a branch de trabalho deve ser excluída.

---

## 3. Padrão de Mensagens de Commit

Adotamos a convenção do **Conventional Commits** em português ou inglês padronizado:

### 3.1 Estrutura

```text
<tipo>(<escopo>): <descrição sucinta>

[corpo opcional detalhando o contexto ou motivação]

[rodapé opcional com referências a issues, ex: Closes #1]
```

### 3.2 Tipos Permitidos

- `feat`: Nova funcionalidade (ex: `feat(api): adiciona rota /health`).
- `test`: Adição ou ajuste de testes (ex: `test(api): adiciona testes com pytest e junit`).
- `ci`: Alterações no pipeline e CI/CD (ex: `ci(actions): configura workflow de compliance`).
- `security`: Controles e ferramentas de segurança (ex: `security(gitleaks): adiciona scan de segredos`).
- `docs`: Alterações na documentação (ex: `docs(guia): adiciona guia de reprodutibilidade`).
- `chore`: Tarefas operacionais ou de configuração (ex: `chore(repo): adiciona estrutura inicial`).
- `fix`: Correção de bugs (ex: `fix(policy): corrige verificador de arquivos proibidos`).

---

## 4. Fluxo de Trabalho e Pull Requests (PR)

```text
1. Criar branch local (ex: git checkout -b feat/aplicacao)
                    │
                    v
2. Desenvolver, testar e commitar com mensagens padronizadas
                    │
                    v
3. Enviar para o GitHub (git push -u origin feat/aplicacao)
                    │
                    v
4. Abrir Pull Request vinculando a Issue correspondente (ex: Closes #2)
                    │
                    v
5. Solicitar revisão dos revisores designados na Issue
                    │
                    v
6. Obter aprovação (Review) + Pipeline verde no GitHub Actions
                    │
                    v
7. Merge na main (Squash and Merge ou Rebase)
```

### 4.1 Requisitos do Pull Request

- **Título claro** indicando o tipo e escopo da alteração.
- **Preenchimento completo do PR Template** (`.github/pull_request_template.md`).
- **Referência à issue:** incluir `Closes #X` ou `Fixes #X` para encerramento automático.
- **Revisão obrigatória:** obter aprovação dos revisores definidos na matriz da issue antes da integração.

---

## 5. Definição de Pronto (Definition of Done — DoD)

Uma issue ou Pull Request é considerada **pronta (Done)** quando atende integralmente aos seguintes critérios:

- [ ] Código implementado de acordo com a descrição da issue.
- [ ] Testes automatizados executados localmente com sucesso (quando aplicável).
- [ ] Verificações de lint (`ruff`), segurança (`gitleaks`, `pip-audit`) e políticas (`check_policies.py`) aprovadas.
- [ ] Documentação correspondente atualizada em `docs/` ou `README.md`.
- [ ] Pipeline do GitHub Actions em estado **verde** (aprovado).
- [ ] Revisão de código realizada e aprovada por pelo menos um dos revisores designados.
- [ ] Nenhuma credencial, segredo ou arquivo proibido (`.env`) versionado.
- [ ] Evidências de execução vinculadas ou catalogadas quando exigido pelo escopo da issue.

---

## 6. Governança da Branch `main`

- A branch `main` é a fonte da verdade e deve refletir sempre um estado estável, testado e em conformidade.
- As integrações na `main` ocorrem exclusivamente via Pull Requests aprovados com validações de CI verdes.
- Releases e tags semânticas (ex: `v1.0.0`) são criadas a partir de commits validados na `main`.

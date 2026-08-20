# EVID-06 — Release `v1.0.0`

> **Estado:** validada após a criação da tag anotada e a publicação da GitHub Release `v1.0.0`.
> Validação concluída conforme a [ISSUE #24](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/24).

## Identificação permanente

- **Issue da release:** [#10](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/10).
- **Pull request da release:** [#23](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/23).
- **Acompanhamento e validação:** [#24](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/24).
- **Responsáveis:** Sabrina (P4) e Sebastião (P7).
- **Revisores:** Samuel (P1), Espedito (P5) e Elder (P2).
- **Tag anotada:** [`v1.0.0`](https://github.com/samsilveira/GC_ComplianceEmDevOps/releases/tag/v1.0.0) (objeto Git do tipo `tag`).
- **Commit entregue:** [`745127feecd70e5359336098f4cde7877baec9c6`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/745127feecd70e5359336098f4cde7877baec9c6).
- **GitHub Release:** [`v1.0.0 — Compliance as Code`](https://github.com/samsilveira/GC_ComplianceEmDevOps/releases/tag/v1.0.0) (publicada em 19/08/2026; `isDraft: false`, `isPrerelease: false`).
- **Changelog:** [`CHANGELOG.md`](../CHANGELOG.md#100---2026-08-19).
- **Pipeline da tag:** [run 32240703943](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32240703943) (concluído com sucesso em 19/08/2026).

## Relação comprovada da release

```text
POL-01..POL-07 -> ISSUE #10 -> PR #23 -> commit 745127f (aprovado)
               -> tag anotada v1.0.0 -> pipeline verde da tag (run 32240703943)
               -> CHANGELOG 1.0.0 -> GitHub Release v1.0.0
```

A tag `v1.0.0` e a GitHub Release são as fontes canônicas do SHA final. A cadeia acima comprova a rastreabilidade completa desde as políticas até a versão publicada.

## Verificação pós-publicação executada

A verificação foi executada conforme os critérios da ISSUE #24:

```sh
git fetch origin tag v1.0.0
test "$(git cat-file -t v1.0.0)" = tag
TAG_SHA=$(git rev-list -n 1 v1.0.0)
gh release view v1.0.0 --json isDraft,isPrerelease,tagName,targetCommitish,url
gh run list --workflow compliance.yml --commit "$TAG_SHA" \
  --json databaseId,headSha,event,status,conclusion,url
```

### Resultados obtidos

- **Tipo do objeto Git:** `tag` (tag anotada confirmada).
- **SHA da tag (`TAG_SHA`):** `745127feecd70e5359336098f4cde7877baec9c6`.
- **Release:** `https://github.com/samsilveira/GC_ComplianceEmDevOps/releases/tag/v1.0.0` (`isDraft: false`, `isPrerelease: false`, `tagName: v1.0.0`, `targetCommitish: main`).
- **Execução do pipeline:** [run 32240703943](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32240703943) (`status: completed`, `conclusion: success`).

### Jobs aprovados na execução da tag (run 32240703943)

| Job | ID | Duração | Status |
| --- | --- | --- | --- |
| Verificação da Fundação do Repositório | 96030381823 | 5s | Concluído com sucesso |
| Varredura de Segredos | 96030414140 | 5s | Concluído com sucesso |
| Verificação de Políticas do Repositório | 96030414176 | 5s | Concluído com sucesso |
| Auditoria de Dependências com pip-audit | 96030446166 | 18s | Concluído com sucesso |
| Qualidade de Código com Ruff | 96030446243 | 13s | Concluído com sucesso |
| Testes Automatizados da API | 96030529767 | 15s | Concluído com sucesso |

### Artefatos da release

- `relatorio-junit-32240703943`
- `relatorio-pip-audit-32240703943`
- `relatorio-ruff-32240703943`

## Conteúdo e limitações

O resumo, as mudanças, as limitações e as instruções de reprodução estão nas [notas versionadas](../.github/release-notes-v1.0.0.md) e na página da release. As limitações técnicas não desabilitam controles obrigatórios.

# EVID-06 — Release `v1.0.0`

> **Estado:** a validar após a criação da tag anotada e a publicação da GitHub
> Release. A validação pós-publicação é acompanhada pela
> [ISSUE #24](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/24).

## Identificação permanente

- **Issue:** [#10](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/10).
- **Pull request da release:** [#23](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/23).
- **Acompanhamento pós-publicação:** [#24](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/24).
- **Responsáveis:** Sabrina (P4) e Sebastião (P7).
- **Revisores:** Samuel (P1), Espedito (P5) e Elder (P2).
- **Tag anotada:** [`v1.0.0`](https://github.com/samsilveira/GC_ComplianceEmDevOps/releases/tag/v1.0.0).
- **Commit entregue:** resolvido diretamente pela
  [tag](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/v1.0.0).
- **Changelog:** [`CHANGELOG.md`](../CHANGELOG.md#100---2026-08-19).
- **Pipeline da tag:** [execuções filtradas por `v1.0.0`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/workflows/compliance.yml?query=branch%3Av1.0.0).

## Relação a validar após a publicação

```text
POL-01..POL-07 -> ISSUE #10 -> PR de release -> commit aprovado
               -> tag anotada v1.0.0 -> pipeline verde da tag
               -> CHANGELOG 1.0.0 -> GitHub Release v1.0.0
```

A tag e a release serão as fontes canônicas do SHA final. Até a publicação,
esta seção descreve a cadeia esperada, não um resultado já comprovado. A
validação ocorrerá depois da criação da tag e da GitHub Release, conforme o
checklist da ISSUE #24, evitando registrar antecipadamente um SHA ou número de
run que ainda não existe.

## Verificação após a publicação

Execute e anexe a saída ao comentário de encerramento da ISSUE #10:

```sh
git fetch origin tag v1.0.0
test "$(git cat-file -t v1.0.0)" = tag
TAG_SHA=$(git rev-list -n 1 v1.0.0)
gh release view v1.0.0 --json isDraft,isPrerelease,tagName,targetCommitish,url
gh run list --workflow compliance.yml --commit "$TAG_SHA" \
  --json databaseId,headSha,event,status,conclusion,url
```

O aceite exige: objeto Git do tipo `tag`, release não draft/não prerelease,
`tagName` igual a `v1.0.0`, ao menos uma execução concluída com sucesso para
`TAG_SHA`, e todos os links desta página acessíveis.

## Conteúdo e limitações

O resumo, as mudanças, as limitações e as instruções de reprodução estão nas
[notas versionadas](../.github/release-notes-v1.0.0.md). As limitações técnicas
não desabilitam controles obrigatórios.

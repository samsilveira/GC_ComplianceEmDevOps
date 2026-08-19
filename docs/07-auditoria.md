# 07 — Trilha de Auditoria e Rastreabilidade

Este documento permite navegar da política até a alteração, a revisão, a
execução automatizada, a evidência e a versão entregue.

## 1. Cadeia de rastreabilidade

```text
política -> issue -> branch/commit -> pull request/revisão
         -> execução do Actions -> evidência -> changelog -> tag/release
```

Cada alteração deve referenciar uma issue. O pull request registra motivação,
escopo, revisores e aceite; o Git preserva autoria e conteúdo; o GitHub Actions
associa os controles ao SHA avaliado; e os arquivos `evidence/EVID-*.md`
preservam os identificadores relevantes após a expiração dos artefatos.

## 2. Relação entre alteração, revisão, execução e evidência

| Escopo | Issue/PR | Commit integrado | Execução ou evidência |
| --- | --- | --- | --- |
| fundação | PR [#13](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/13) | `94dc1aa` | [EVID-01](../evidence/EVID-01.md) |
| aplicação | PR [#14](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/14) | `c711917` | testes em [EVID-02](../evidence/EVID-02.md) |
| testes e pipeline-base | PRs [#15](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/15) e [#16](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/16) | `e31f4f3`, `632e9e3` | [EVID-02](../evidence/EVID-02.md) |
| segredos | PR [#17](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/17) | `2c4c73a` | [EVID-03](../evidence/EVID-03.md) |
| qualidade e dependências | PRs [#18](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/18) e [#19](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/19) | `e1a864f`, `8a094c6` | [EVID-04](../evidence/EVID-04.md) |
| políticas como código | PR [#20](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/20) | `b70e38f` | [EVID-05](../evidence/EVID-05.md) |
| catálogo de evidências | PR [#21](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/21) | `2112592` | [índice](../evidence/README.md) |
| reprodução independente | PR [#22](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/22) | `8501a7d` | [registro](09-reproducao-independente.md) |
| release `v1.0.0` | ISSUE [#10](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/10) e PR [#23](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/23) | `745127f` (tag anotada [`v1.0.0`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/v1.0.0)) | [EVID-06](../evidence/EVID-06.md) e acompanhamento [#24](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/24) |

Os SHAs abreviados podem ser expandidos com `git rev-parse <sha>`. A associação
final não depende do nome da branch: a tag aponta para o commit aprovado.

## 3. Controles e fontes de auditoria

| Informação | Fonte |
| --- | --- |
| regra obrigatória | `policies/policy.md` e `docs/04-politicas.md` |
| autoria e conteúdo | histórico Git |
| motivação e aceite | issue e pull request |
| revisão humana | reviews e aprovação do pull request |
| resultado automatizado | run do GitHub Actions associado ao SHA |
| relatórios técnicos | artefatos JUnit, Ruff, pip-audit e Gitleaks |
| demonstrações | `evidence/EVID-*.md` |
| relação política-evidência | `evidence/POLICY-MAP.md` |
| conteúdo entregue | `CHANGELOG.md`, tag anotada e GitHub Release |

## 4. Procedimento controlado da release `v1.0.0`

1. Obter ao menos uma aprovação no pull request da branch
   `chore/release-v1.0.0`, conforme o ruleset `main-protect`. Samuel (P1),
   Espedito (P5) e Elder (P2) permanecem como revisores solicitados, sem exigir
   que os três concluam a revisão antes do merge.
2. Confirmar que todos os checks obrigatórios do commit aprovado estão verdes
   e que não há mudanças obrigatórias fora do pull request.
3. Fazer o merge e aguardar o pipeline verde do commit resultante em `main`.
4. Criar a tag **anotada**, sem mover ou recriar uma tag já publicada:

   ```sh
   git switch main
   git pull --ff-only origin main
   RELEASE_SHA=$(git rev-parse HEAD)
   git tag -a v1.0.0 "$RELEASE_SHA" -m "Release v1.0.0"
   git push origin v1.0.0
   ```

5. Aguardar o [pipeline da tag](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/workflows/compliance.yml?query=branch%3Av1.0.0)
   e confirmar que o SHA exibido é igual a `git rev-list -n 1 v1.0.0`.
6. Publicar a GitHub Release usando
   [`.github/release-notes-v1.0.0.md`](../.github/release-notes-v1.0.0.md):

   ```sh
   gh release create v1.0.0 \
     --title "v1.0.0 — Compliance as Code" \
     --notes-file .github/release-notes-v1.0.0.md \
     --verify-tag
   ```

7. Executar as verificações de [EVID-06](../evidence/EVID-06.md), concluir o
   checklist da [ISSUE #24](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/24),
   registrar os links no fechamento da ISSUE #10 e somente então liberar a
   ISSUE #11.

## 5. Critérios de congelamento e rollback

Não publicar enquanto houver check obrigatório vermelho ou pendente, revisão
solicitando mudança, diferença não explicada entre changelog e release, link
local inválido ou alteração obrigatória ainda não integrada. Se a tag ainda não
tiver sido enviada, corrija o commit e repita a validação. Depois de publicada,
uma tag de release não deve ser movida: uma correção exige nova versão SemVer.

## 6. Retenção e integridade

Os relatórios JUnit, Ruff e pip-audit têm retenção configurada de 14 dias. O
artefato SARIF do Gitleaks usa a retenção da ação, observada em 90 dias na
execução da candidata. Os documentos locais registram URLs, números de execução
e SHAs, relacionando o resultado ao commit mesmo depois da expiração. Segredos
detectados não são reproduzidos; demonstrações usam somente valores sintéticos.
Links relativos são preferidos para que a documentação continue navegável em
branches, tags e releases.

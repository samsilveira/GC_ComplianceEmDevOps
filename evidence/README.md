# Trilha de evidências — Compliance em DevOps

Este é o índice central da trilha auditável. Ele permite localizar as evidências
pelos três momentos da demonstração, pelo controle ou pela execução do GitHub
Actions. Os registros catalogam somente material já produzido nas issues
anteriores; não contêm tokens, credenciais reais ou dados pessoais.

## Roteiro navegável dos três momentos

| Momento | Estado demonstrado | Evidência principal | Commit | Execução e data |
| --- | --- | --- | --- | --- |
| 1 — Aprovação | Pipeline-base aprovado | [EVID-01](EVID-01.md) | `78bfade` | [run 31809146741](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31809146741), 14/08/2026 |
| 2A — Violação | Segredo exclusivamente sintético bloqueado pelo Gitleaks | [EVID-03](EVID-03.md) | `c50e11520b66d3bd3ba5ae1ca7f014c3cff62145` | [run 31955024357](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31955024357), 16/08/2026 |
| 2B — Violação | Arquivo `.env` vazio bloqueado pelo controle interno de `POL-02` | [EVID-05](EVID-05.md) | `24b6903dc67d4896d048dc3f0b8862680df4539f` | [run 32040521363](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32040521363), 17/08/2026 |
| 3 — Correção | Todas as correções da PR #20 integradas na `main` e os seis jobs aprovados | [EVID-05](EVID-05.md) e [contingência](contingency/README.md) | `b70e38f7b93822fb96c27a410d9d93c733744c8c` | [run 32062843662](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32062843662), 17/08/2026 |

## Catálogo por controle

| ID | Controle demonstrado | Relatórios ou registros | Origem |
| --- | --- | --- | --- |
| `EVID-01` | Fundação e pipeline-base | Log do CI | [PR #13](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/13) e [run 31809146741](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31809146741) |
| `EVID-02` | Testes automatizados | JUnit e logs do CI | [registro](EVID-02.md), [PR #15](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/15) e [PR #16](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/16) |
| `EVID-03` | Detecção de segredos | SARIF redigido e logs do Gitleaks | [registro](EVID-03.md) e [PR #17](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/17) |
| `EVID-04` | Qualidade e dependências | JSON do Ruff, pip-audit e JUnit | [registro](EVID-04.md), [PR #18](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/18) e [PR #19](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/19) |
| `EVID-05` | Arquivo proibido (`POL-02`) e governança obrigatória (`POL-05`) | Logs do `check_policies.py` | [registro](EVID-05.md) e [PR #20](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/20) |
| `EVID-06` | Release, versão e rastreabilidade (`POL-06` e `POL-07`) | Tag anotada, run da tag, changelog e GitHub Release | [registro](EVID-06.md) e [ISSUE #10](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/10) |

O [mapeamento entre políticas e evidências](POLICY-MAP.md) explicita qual
controle cada registro comprova. O [material de contingência](contingency/README.md)
preserva um roteiro autocontido caso os logs ou artefatos temporários do GitHub
Actions estejam indisponíveis durante a apresentação.

## Estado integrado e artefatos finais

O [run 32062843662](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32062843662)
foi executado na `main` para o commit de merge `b70e38f` e aprovou os seis jobs.
Os relatórios produzidos podem ser acessados diretamente enquanto estiverem no
período de retenção:

- [JUnit `relatorio-junit-32062843662`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32062843662/artifacts/9298786673);
- [pip-audit `relatorio-pip-audit-32062843662`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32062843662/artifacts/9298776654);
- [Ruff `relatorio-ruff-32062843662`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32062843662/artifacts/9298774255);
- [SARIF `gitleaks-results.sarif`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32062843662/artifacts/9298764435).

## Convenção de nomes

- Registro Markdown: `EVID-NN.md`.
- Relatório preservado: `EVID-NN_<controle>_<run-id>.<ext>`.
- Captura: `EVID-NN_<momento>_<run-id>_NN.<ext>`.
- Vídeo: `DEMO_YYYY-MM-DD_<versao>.mp4`.
- Artefato do workflow: `<tipo>-<run-id>`, mantendo os nomes já publicados,
  como `relatorio-junit-31911702227` e `gitleaks-results.sarif`.

Use identificadores em maiúsculas apenas para `EVID` e `DEMO`, termos em
minúsculas ASCII separados por hífen ou sublinhado conforme os modelos acima,
e nunca inclua nome de pessoa, e-mail, token ou outro dado sensível no arquivo.

## Integridade, retenção e revisão

- Os artefatos do Actions têm retenção limitada; os registros Markdown guardam
  commit, run, data, controle e resultado necessários para a apresentação.
- Antes de publicar uma nova cópia, o responsável técnico deve revisar o
  conteúdo, redigir valores e registrar a aprovação no PR correspondente.
- A revisão técnica do Gitleaks, Ruff e pip-audit está vinculada aos PRs #17,
  #18 e #19, sob responsabilidade de Manoel. A correspondência das políticas
  está vinculada ao PR #20, sob responsabilidade de Sabrina.
- Links externos requerem acesso ao GitHub. Os documentos relativos e o roteiro
  de contingência permanecem navegáveis diretamente no repositório.

## Limite da ISSUE-08

Esta catalogação não altera workflow, gerador de evidências, controles de
segurança ou políticas. A publicação e a validação de ausência dos artefatos já
estão implementadas no workflow herdado: Ruff e pip-audit usam
`if-no-files-found: error`; o JUnit usa `warn`, decisão anterior a esta issue.
Qualquer mudança funcional deve ser feita pelo responsável técnico em outra
issue e novamente aprovada antes de ser catalogada aqui.

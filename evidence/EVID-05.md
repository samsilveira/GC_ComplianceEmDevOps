# EVID-05 — Bloqueio por arquivo proibido e validação de governança

## Controles demonstrados

- **`POL-02`:** proibição de arquivos `.env`, verificada por
  `check_policies.py` em complemento ao Gitleaks.
- **`POL-05`:** presença da documentação e da governança obrigatórias,
  verificada pelo mesmo script e pelo `foundation-check`.
- **Issue:** [ISSUE-07](https://github.com/samsilveira/GC_ComplianceEmDevOps/issues/7).
- **Pull request:** [PR #20](https://github.com/samsilveira/GC_ComplianceEmDevOps/pull/20).
- **Responsável:** Sabrina (P4) — `@sabrinaalencaar`.

## Falha controlada

- **Commit da violação:** `24b6903dc67d4896d048dc3f0b8862680df4539f`.
- **Violação segura:** inclusão de um arquivo `.env` vazio, sem segredo real.
- **Execução vermelha:** [run 32040521363](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32040521363).
- **Data da execução:** 17/08/2026.
- **Job:** [Verificação de Políticas do Repositório](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32040521363/job/95418906439).
- **Resultado observado:** o script identificou `./.env` e encerrou com código `1`.

Essa falha demonstra especificamente `POL-02`. Os arquivos obrigatórios
continuaram presentes, portanto o run não demonstra uma violação controlada de
`POL-05`.

O run de falha não publicou artefatos. A evidência remota disponível é o log do job vinculado acima, associado ao commit da violação.

## Restauração da conformidade

- **Commit de restauração:** `fd7f8997824ce32fe050757fcbc0392445d487ba`.
- **Execução verde:** [run 32041545903](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32041545903).
- **Data da execução:** 17/08/2026.
- **Job:** [Verificação de Políticas do Repositório](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32041545903/job/95421668954).
- **Resultado observado:** o script não encontrou arquivo proibido e o job foi concluído com sucesso.

## Estado integrado na `main`

- **Commit de merge da PR #20:**
  [`b70e38f7b93822fb96c27a410d9d93c733744c8c`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/b70e38f7b93822fb96c27a410d9d93c733744c8c).
- **Execução verde pós-merge:**
  [run 32062843662](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32062843662),
  em 17/08/2026.
- **Resultado:** os seis jobs foram aprovados; o `policy-check` confirmou tanto
  a ausência de arquivos proibidos (`POL-02`) quanto a presença dos documentos
  obrigatórios (`POL-05`).

## Limites da evidência

O `check_policies.py` valida nomes de arquivos e a presença de documentos
obrigatórios. A análise de conteúdo para detectar segredos pertence ao Gitleaks
e não deve ser inferida desta evidência.

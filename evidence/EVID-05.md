# EVID-05 — Bloqueio por política interna

## Controle demonstrado

- **Política:** `POL-05` — presença de documentação obrigatória e ausência de arquivos proibidos.
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

O run de falha não publicou artefatos. A evidência remota disponível é o log do job vinculado acima, associado ao commit da violação.

## Restauração da conformidade

- **Commit de restauração:** `fd7f8997824ce32fe050757fcbc0392445d487ba`.
- **Execução verde:** [run 32041545903](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32041545903).
- **Data da execução:** 17/08/2026.
- **Job:** [Verificação de Políticas do Repositório](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32041545903/job/95421668954).
- **Resultado observado:** o script não encontrou arquivo proibido e o job foi concluído com sucesso.

## Limites da evidência

O `check_policies.py` valida nomes de arquivos e a presença de documentos obrigatórios. A análise de conteúdo para detectar segredos pertence ao Gitleaks (`POL-02`) e não deve ser inferida desta evidência.

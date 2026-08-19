# Roteiro documental de contingência

Estes cartões preservam os dados que devem aparecer na demonstração. Eles
substituem a navegação ao vivo quando o GitHub Actions ou seus artefatos
temporários não estiverem disponíveis. Não substituem os runs como fonte
primária; cada cartão aponta para a origem auditável.

## Momento 1 — aprovação inicial

> **APROVADO** · run `31809146741` · commit `78bfade` · 14/08/2026<br>
> Controle: fundação e pipeline-base em estado verde.<br>
> Origem: [EVID-01](../EVID-01.md) · [GitHub Actions](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31809146741)

## Momento 2A — bloqueio de segredo sintético

> **BLOQUEADO** · run `31955024357` · commit `c50e11520b66d3bd3ba5ae1ca7f014c3cff62145` · 16/08/2026<br>
> Controle: Gitleaks, regra `gc-demo-secret`; valores redigidos e nenhuma credencial real.<br>
> Resultado: job de segredos falhou com saída não zero.<br>
> Origem: [EVID-03](../EVID-03.md) · [GitHub Actions](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31955024357)

## Momento 2B — bloqueio por política

> **BLOQUEADO** · run `32040521363` · commit `24b6903dc67d4896d048dc3f0b8862680df4539f` · 17/08/2026<br>
> Controle: `POL-02`; um arquivo `.env` vazio foi usado, sem segredo.<br>
> Resultado: `check_policies.py` detectou o nome proibido e encerrou com código 1.<br>
> Origem: [EVID-05](../EVID-05.md) · [GitHub Actions](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32040521363)

## Momento 3 — aprovação após correção

> **APROVADO** · run `32062843662` · commit `b70e38f7b93822fb96c27a410d9d93c733744c8c` · 17/08/2026<br>
> Controles: `POL-01` a `POL-05` no estado integrado da `main`.<br>
> Resultado: os seis jobs foram concluídos com sucesso e quatro artefatos foram publicados.<br>
> Origem: [EVID-05](../EVID-05.md) · [GitHub Actions](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/32062843662)

## Roteiro curto

1. Mostre o Momento 1 como baseline aprovado.
2. Compare com os Momentos 2A e 2B e destaque o controle que bloqueou cada run.
3. Termine no Momento 3, relacionando remoção, novo commit e novo run verde.
4. Retorne ao [índice](../README.md) para mostrar a navegação por controle.

Os cartões não reproduzem logs nem valores detectados, evitando a exposição de
conteúdo sensível. Antes da apresentação, confirme os links; se o acesso remoto
falhar, todo o roteiro continua disponível por links relativos.

O procedimento principal, os comandos automatizados e a transição para este
modo de contingência estão descritos em
[`docs/10-demonstracao-ao-vivo.md`](../../docs/10-demonstracao-ao-vivo.md).

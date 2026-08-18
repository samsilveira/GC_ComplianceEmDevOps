# 06 — Catálogo de evidências e demonstração

A trilha auditável está centralizada no
[`evidence/README.md`](../evidence/README.md). O índice oferece três caminhos:

- roteiro cronológico de aprovação, violação e correção;
- catálogo por controle e tipo de relatório;
- material autocontido para apresentação em contingência.

O vínculo explícito entre as políticas, seus bloqueios e as respectivas
execuções está no
[`evidence/POLICY-MAP.md`](../evidence/POLICY-MAP.md). O roteiro documental
para substituir uma demonstração ao vivo está em
[`evidence/contingency/README.md`](../evidence/contingency/README.md).

Os artefatos binários e relatórios gerados pelo pipeline permanecem associados
aos runs do GitHub Actions e têm retenção limitada. Por isso, cada registro local
preserva origem, data, commit, run, controle e resultado, sem copiar segredos ou
dados pessoais para o repositório.

## Como interpretar

Os arquivos `EVID-01` a `EVID-05` são índices permanentes, não cópias dos artefatos temporários. Cada um informa controle, commit, execução, data e resultado. `POLICY-MAP.md` permite partir de uma política e chegar às execuções.

Resultados documentados são aqueles associados a runs existentes. Lacunas são identificadas explicitamente como “não produzidas”. A evidência de release (`EVID-06`) permanece planejada para a ISSUE-10.

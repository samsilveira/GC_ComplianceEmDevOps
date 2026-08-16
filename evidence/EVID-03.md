# EVID-03 — Bloqueio por Deteccao de Segredos com Gitleaks

Este registro amarra a violacao controlada da ISSUE-05 ao workflow que a bloqueou e ao commit que restaurou o pipeline para estado verde.

## 1. Identificacao

- **Issue:** #5
- **Responsavel principal:** Manoel (P3) — `@Junio404`
- **Revisores:** Samuel (P1) e Elder (P2)
- **Branch de implementacao:** `feat/scan-segredos`

## 2. Violacao Controlada

- **Branch ou commit da violacao:** `PREENCHER`
- **Arquivo temporario usado na demonstracao:** `controlled-violation-demo.txt`
- **Conteudo permitido para a demonstracao:** `GC_DEMO_SECRET="<valor-falso-controlado>"`
- **Formato aceito para o valor falso temporario:** `gc-demo-secret-XXXXXXXXXXXX` com 12 caracteres maiusculos e/ou digitos
- **Execucao vermelha do GitHub Actions:** `PREENCHER`
- **Artefato/log capturado:** `PREENCHER`

## 3. Correcao

- **Commit que remove a violacao:** `PREENCHER`
- **Execucao verde apos a correcao:** `PREENCHER`

## 4. Observacoes de Auditoria

- Nenhuma credencial real deve ser usada nesta evidencia.
- O arquivo de demonstracao nao deve permanecer no estado final do branch.
- Este registro deve permitir relacionar branch ou commit, execucao com falha e execucao corrigida.

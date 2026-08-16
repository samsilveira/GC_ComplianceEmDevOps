# EVID-03 — Bloqueio por Detecção de Segredos com Gitleaks

Este registro relaciona a violação controlada da ISSUE-05 ao workflow que a bloqueou e ao commit que restaurou o pipeline para o estado verde.

## 1. Identificação

- **Issue:** #5
- **Responsavel principal:** Manoel (P3) — `@Junio404`
- **Revisores:** Samuel (P1) e Elder (P2)
- **Branch de implementação:** `issue5`

## 2. Violação Controlada

- **Commit da violação:** [`c50e11520b66d3bd3ba5ae1ca7f014c3cff62145`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/c50e11520b66d3bd3ba5ae1ca7f014c3cff62145)
- **Ocorrências controladas:** exemplos sintéticos em `docs/05-como-executar.md` e `evidence/EVID-03.md`; nenhuma credencial real foi utilizada.
- **Regra acionada:** `gc-demo-secret`, duas ocorrências, ambas redigidas (`REDACTED`) no log.
- **Formato do valor falso usado:** `gc-demo-secret-XXXXXXXXXXXX`, com 12 caracteres maiúsculos e/ou dígitos.
- **Execução vermelha do GitHub Actions:** [`31955024357`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31955024357)
- **Job bloqueado:** [`Varredura de Segredos`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31955024357/job/95184253271), com código de saída não zero e os testes da API ignorados por dependência.
- **Artefato capturado:** [`gitleaks-results.sarif`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31955024357/artifacts/9265705235), ID `9265705235`, SHA-256 `9fce3ff8df64be7fc140b077fd35205a0f5fd2a0619a87c241931dd84bf1c7e8` e expiração informada pelo GitHub em 14/11/2026.

## 3. Correção

- **Commit que remove a violação:** [`b1ff7add3dec876fc554caab2b3f3b9db23fa4aa`](https://github.com/samsilveira/GC_ComplianceEmDevOps/commit/b1ff7add3dec876fc554caab2b3f3b9db23fa4aa)
- **Execução verde do push:** [`31955499109`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31955499109)
- **Execução verde da pull request:** [`31956280775`](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions/runs/31956280775)
- **Resultado:** o Gitleaks examinou o commit corrigido, informou `no leaks found` e liberou a execução dos testes automatizados da API.

## 4. Observações de Auditoria

- O commit da violação e o commit corrigido têm o mesmo pai (`632e9e3c71397487738e30cd70682d9947f7442a`): a correção foi publicada reescrevendo o commit original, e não como um commit descendente.
- Por causa dessa reescrita, `c50e115` não integra o histórico atual de `issue5`, mas permanece verificável pela execução vermelha, pelo log e pelo artefato do GitHub Actions.
- A demonstração efetivamente realizada usou exemplos sintéticos na documentação; não foi criado o arquivo `controlled-violation-demo.txt` descrito como procedimento recomendado.
- Em demonstrações futuras, devem ser preservados commits separados para introdução e remoção da violação, sem force push, garantindo uma cadeia de auditoria linear.
- O resumo acima preserva os dados essenciais mesmo após a expiração do artefato temporário do GitHub Actions.

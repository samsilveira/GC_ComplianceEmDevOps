# 06 — Catálogo de Evidências e Demonstração

Este documento reúne os links, capturas e descrições das evidências geradas durante as execuções de conformidade.

---

## 1. Estrutura dos Momentos Demonstrados

1. **Momento 1:** Pipeline Conforme (Aprovação Inicial)
2. **Momento 2:** Pipeline Não Conforme (Bloqueio Controlado por Violação)
3. **Momento 3:** Pipeline Corrigido (Aprovação e Restauração)

---

## 2. Relação de Evidências Catalogadas

Durante a ISSUE-05, a evidencia minima a ser preservada para o controle de segredos e:

- branch de implementacao com o workflow atualizado;
- commit da violacao controlada com apenas o segredo falso da demonstracao;
- URL da execucao vermelha em que o job `Varredura de Segredos` falhou;
- log do step `Executar Gitleaks`;
- artefato de relatorio do Gitleaks publicado pela execucao com falha;
- commit que remove a violacao;
- URL da execucao verde apos a correcao.

O registro estruturado desses itens deve ser mantido em [`evidence/EVID-03.md`](../evidence/EVID-03.md) e posteriormente catalogado por Pedro Yan (P6) na ISSUE-08.

Para a ISSUE-06, cada execução não cancelada preserva:

- `reports/ruff.json` no artefato `relatorio-ruff-<run-id>`;
- `reports/pip-audit.json` no artefato `relatorio-pip-audit-<run-id>`;
- logs e códigos de saída dos jobs bloqueantes no GitHub Actions;
- versões, decisões, limitações e vínculos da execução em [`evidence/EVID-04.md`](../evidence/EVID-04.md).

O registro da ISSUE-06 deve vincular o commit avaliado e a URL da execução verde. Caso seja feita uma demonstração controlada de bloqueio, o commit temporário, a execução vermelha e o commit de correção também devem ser registrados sem manter a violação no estado final da branch.

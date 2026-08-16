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

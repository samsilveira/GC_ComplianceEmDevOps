# Mapeamento entre políticas e evidências

| Política/controle | Implementação observada | Evidência de aprovação | Evidência de bloqueio | Evidência após correção |
| --- | --- | --- | --- | --- |
| Documentação mínima (`POL-01`) | Fundação e `check_policies.py` | [EVID-01](EVID-01.md) | Não foi produzida violação específica aprovada | [EVID-05](EVID-05.md) |
| Segurança de credenciais (`POL-02`) | Gitleaks e regra `gc-demo-secret` | [EVID-03](EVID-03.md), run verde 31955499109 | [EVID-03](EVID-03.md), run vermelho 31955024357 | [EVID-03](EVID-03.md), run verde 31955499109 |
| Testes automatizados (`POL-03`) | pytest com relatório JUnit | [EVID-02](EVID-02.md), run verde 31911634784 | [EVID-02](EVID-02.md), run vermelho 31911672486 | [EVID-02](EVID-02.md), run verde 31911702227 |
| Qualidade estática (`POL-04`) | Ruff bloqueante | [EVID-04](EVID-04.md), run verde 31968978387 | Não foi produzida violação específica aprovada | [EVID-04](EVID-04.md), run verde 31970378390 |
| Arquivos obrigatórios/proibidos (`POL-05`) | `check_policies.py` | [EVID-05](EVID-05.md), run verde 32041545903 | [EVID-05](EVID-05.md), run vermelho 32040521363 | [EVID-05](EVID-05.md), run verde 32041545903 |
| Dependências vulneráveis | pip-audit bloqueante em modo `--strict` | [EVID-04](EVID-04.md), run verde 31968978387 | Não foi produzida violação específica aprovada | [EVID-04](EVID-04.md), run verde 31970378390 |

“Não foi produzida” é uma delimitação deliberada: a ISSUE-08 cataloga apenas
execuções entregues e aprovadas pelos responsáveis, sem criar novas violações
para preencher lacunas.

# Mapeamento entre políticas e evidências

| Política/controle | Implementação observada | Evidência de aprovação | Evidência de bloqueio | Evidência após correção |
| --- | --- | --- | --- | --- |
| Testes automatizados (`POL-01`) | pytest com relatório JUnit | [EVID-02](EVID-02.md), run verde 31911634784 | [EVID-02](EVID-02.md), run vermelho 31911672486 | [EVID-02](EVID-02.md), run verde 31911702227 |
| Segurança de credenciais e arquivos `.env` (`POL-02`) | Gitleaks, regra `gc-demo-secret` e `check_policies.py` | [EVID-03](EVID-03.md), run verde 31955499109 | [EVID-03](EVID-03.md), run vermelho 31955024357; [EVID-05](EVID-05.md), run vermelho 32040521363 | [EVID-05](EVID-05.md), run integrado 32062843662 |
| Qualidade estática (`POL-03`) | Ruff bloqueante | [EVID-04](EVID-04.md), run verde 31968978387 | Não foi produzida violação específica aprovada | [EVID-04](EVID-04.md), run final 31970482482 |
| Dependências vulneráveis (`POL-04`) | pip-audit bloqueante em modo `--strict` | [EVID-04](EVID-04.md), run verde 31968978387 | Não foi produzida violação específica aprovada | [EVID-04](EVID-04.md), run final 31970482482 |
| Documentação e governança obrigatórias (`POL-05`) | `foundation-check` e `check_policies.py` | [EVID-01](EVID-01.md) | Não foi produzida violação específica aprovada | [EVID-05](EVID-05.md), run integrado 32062843662 |

“Não foi produzida” é uma delimitação deliberada: a ISSUE-08 cataloga apenas
execuções entregues e aprovadas pelos responsáveis, sem criar novas violações
para preencher lacunas.

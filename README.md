# Compliance em DevOps: Pipeline de Conformidade Automatizada

## Descrição

Este projeto consiste em um experimento prático de **Compliance as Code**, desenvolvido para a disciplina de Gerência de Configuração. O objetivo é demonstrar como requisitos organizacionais de qualidade, segurança, rastreabilidade e auditoria podem ser incorporados a um pipeline de integração contínua.

O experimento utiliza uma API Python mínima como objeto de avaliação. A cada alteração, o GitHub Actions executa controles automáticos, gera evidências auditáveis e impede que uma versão fora das políticas definidas avance no fluxo de desenvolvimento.

## Integrantes

| Papel | Integrante | GitHub | Frente principal |
| :--- | :--- | :--- | :--- |
| **P1** | Samuel Wagner Tiburi Silveira | [@samsilveira](https://github.com/samsilveira) | Repositório, CI, integração e entrega final |
| **P2** | Elder Rayan Oliveira Silva | [@eldrayan](https://github.com/eldrayan) | Aplicação e testes |
| **P3** | Manoel Junio Duarte da Silva | [@Junio404](https://github.com/Junio404) | Segurança e dependências |
| **P4** | Sabrina Alencar Soares | [@sabrinaalencaar](https://github.com/sabrinaalencaar) | Políticas e auditoria |
| **P5** | Espedito Ramom Mascena Ricarto | [@RamomRicarto](https://github.com/RamomRicarto) | Documentação e reprodutibilidade |
| **P6** | Pedro Yan Alcantara Palácio | [@pedropalacioo](https://github.com/pedropalacioo) | Coleta e organização de evidências de baixo risco |
| **P7** | Sebastião Sousa Soares | [@SebastiaoSoares](https://github.com/SebastiaoSoares) | Auditoria, release e apresentação |

Consulte o [Guia de Contribuição (CONTRIBUTING.md)](CONTRIBUTING.md) para detalhes sobre a governança, convenções de branches, commits e fluxo de pull requests.

## Objetivos do experimento

- Demonstrar a aplicação prática de políticas de conformidade em um fluxo DevOps.
- Automatizar verificações de testes, qualidade, segredos, dependências e políticas internas.
- Bloquear alterações que não atendam aos critérios de conformidade estabelecidos.
- Produzir uma trilha de auditoria composta por commits, execuções do pipeline, relatórios e artefatos.
- Permitir que qualquer pessoa reproduza o experimento a partir da documentação do repositório.
- Comparar uma execução aprovada, uma violação intencional e a respectiva correção.

## Tecnologias e mecanismos

- **Linguagem:** Python
- **Aplicação mínima:** Flask
- **Testes automatizados:** pytest
- **Lint e análise de código:** Ruff
- **Detecção de segredos:** Gitleaks
- **Auditoria de dependências:** pip-audit
- **Validação de políticas:** script Python próprio
- **Integração contínua:** GitHub Actions
- **Rastreabilidade:** Git, pull requests, tags, changelog e GitHub Releases
- **Documentação:** Markdown

As versões adotadas estão fixadas nos arquivos de dependências e registradas na documentação técnica para tornar o experimento reproduzível.

## Políticas de conformidade

O MVP validará as seguintes políticas organizacionais:

1. Toda alteração deve passar por testes automatizados.
2. Segredos, credenciais e arquivos `.env` não podem ser versionados.
3. Dependências com vulnerabilidades conhecidas devem bloquear o pipeline.
4. O código deve passar pelas verificações de lint e análise definidas pelo projeto.
5. O repositório deve conter a documentação mínima obrigatória.
6. Toda release deve possuir versão, changelog e vínculo com um commit.
7. Cada execução do pipeline deve produzir evidências consultáveis para auditoria.

## Arquitetura e fluxo de conformidade

```text
Desenvolvedor faz commit ou abre um pull request
                         │
                         v
                  GitHub Actions
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       v                 v                 v
 Testes e lint    Segurança e         Validação das
                  dependências        políticas internas
       │                 │                 │
       └─────────────────┼─────────────────┘
                         v
              Geração de evidências
                         │
             ┌───────────┴───────────┐
             │                       │
             v                       v
      Conforme: aprovado     Não conforme: bloqueado
```

O experimento deverá apresentar três momentos: pipeline aprovado, pipeline bloqueado por uma violação controlada e nova aprovação após a correção.

## Evidências e auditoria

As evidências serão organizadas em `evidence/` e também publicadas como artefatos das execuções do GitHub Actions. O conjunto mínimo inclui:

- pipeline executado com sucesso;
- pipeline bloqueado por violação;
- relatório dos testes;
- resultados do lint e das verificações de segurança;
- resultado da auditoria de dependências;
- log da validação de políticas;
- commit que introduz a violação e commit que a corrige;
- tag, changelog e release final;
- capturas de tela ou vídeo de contingência para a apresentação.

## Pré-requisitos e dependências

- Git
- Python 3.10 ou superior e `pip` (o pipeline usa Python 3.12 como versão de referência)
- Acesso a um terminal
- Conta no GitHub para consultar workflows, artefatos e releases

As dependências necessárias para executar a API são instaladas a partir de `requirements.txt`. As ferramentas de desenvolvimento, qualidade e auditoria estão fixadas em `requirements-dev.txt`.

## Estrutura do repositório

```text
.
├── .github/
│   └── workflows/
│       └── compliance.yml
├── app/
│   ├── __init__.py
│   └── main.py
├── docs/
│   ├── 01-visao-geral.md
│   ├── 02-arquitetura.md
│   ├── 03-ferramentas.md
│   ├── 04-politicas.md
│   ├── 05-como-executar.md
│   ├── 06-evidencias.md
│   ├── 07-auditoria.md
│   ├── 08-referencias.md
│   └── 09-reproducao-independente.md
├── evidence/
│   └── README.md
├── policies/
│   └── policy.md
├── scripts/
│   └── check_policies.py
├── tests/
│   ├── test_api.py
│   └── test_check_policies.py
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## Navegação na documentação

A pasta `docs/` é o ponto de entrada para a documentação aprofundada:

| Documento | Conteúdo |
| --- | --- |
| `docs/01-visao-geral.md` | Contexto, problema, objetivos e escopo |
| `docs/02-arquitetura.md` | Componentes e fluxo do experimento |
| `docs/03-ferramentas.md` | Escolhas técnicas, vantagens e limitações |
| `docs/04-politicas.md` | Políticas e matriz de controles de conformidade |
| `docs/05-como-executar.md` | Instalação, configuração e reprodução completa |
| `docs/06-evidencias.md` | Resultados, imagens, vídeos e artefatos |
| `docs/07-auditoria.md` | Rastreabilidade de alterações, decisões e releases |
| `docs/08-referencias.md` | Referências técnicas e bibliográficas |
| `docs/09-reproducao-independente.md` | Registro do teste de reprodução independente |

## Instalação e execução

> **Estado atual:** a API, os testes e todos os controles automatizados do MVP estão implementados. A governança de release (POL-06) permanece manual até a ISSUE-10.

```sh
git clone https://github.com/samsilveira/GC_ComplianceEmDevOps.git
cd GC_ComplianceEmDevOps

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

No Windows PowerShell, ative o ambiente virtual com:

```powershell
.venv\Scripts\Activate.ps1
```

Para executar a aplicação:

```sh
flask --app app.main run
```

Para executar os testes automatizados (o relatório JUnit será salvo em `reports/junit.xml`):

```sh
pytest
```

Para executar os controles da ISSUE-06 localmente:

```sh
ruff check .
pip-audit --requirement requirements.txt --strict
```

O scan de segredos roda automaticamente no GitHub Actions. A política de estrutura e arquivos proibidos pode ser verificada localmente com:

```sh
python scripts/check_policies.py
```

## Como verificar o pipeline

1. Acesse a aba [Actions](https://github.com/samsilveira/GC_ComplianceEmDevOps/actions) do repositório.
2. Abra uma execução do workflow **Compliance Pipeline**.
3. Verifique os jobs **Verificação da Fundação do Repositório**, **Varredura de Segredos**, **Qualidade de Código com Ruff**, **Auditoria de Dependências com pip-audit** e **Testes Automatizados da API**.
4. No job **Varredura de Segredos**, consulte o step **Executar Gitleaks** para confirmar que o scan rodou automaticamente.
5. Em uma demonstração de falha controlada, baixe o artefato publicado pelo Gitleaks e vincule a execução em `evidence/EVID-03.md`.
6. No job de testes, consulte o step **Executar testes e gerar relatório JUnit** e baixe o artefato `relatorio-junit-<run-id>` ao final da execução.
7. Baixe os artefatos `relatorio-ruff-<run-id>` e `relatorio-pip-audit-<run-id>` e confirme que os relatórios JSON correspondem ao mesmo identificador da execução.
8. Consulte o job **Verificação de Políticas do Repositório** para validar os controles de estrutura e arquivos proibidos.

## Organização do trabalho

As sete frentes propostas para o desenvolvimento são:

| Frente | Responsabilidade principal | Entregas |
| --- | --- | --- |
| P1 | Repositório, CI, integração e entrega final | Fundação, workflow principal, integração de PRs e entrega final |
| P2 | Aplicação e testes | API mínima, rotas `/` e `/health` e testes |
| P3 | Segurança e dependências | Gitleaks, pip-audit, Ruff e relatório de segurança |
| P4 | Políticas e auditoria | Políticas, script de validação, matriz e changelog |
| P5 | Documentação e reprodução | Guias, referências e revisão da reprodutibilidade |
| P6 | Evidências e demonstração | Registros das execuções, artefatos e roteiro prático |
| P7 | Auditoria, release e apresentação | Auditoria final, apoio à release, slides e ensaio |

## Plano de execução

| Dia | Entrega principal |
| --- | --- |
| 1 | Repositório, issues, estrutura e políticas iniciais |
| 2 | API mínima, testes e pipeline-base |
| 3 | Verificações de segurança e dependências |
| 4 | Validação automática de políticas |
| 5 | Evidências de aprovação, violação e correção; release candidata |
| 6 | Reprodução integral por outro integrante e documentação completa |
| 7 | Revisão, ensaio e congelamento do escopo |
| 8 | Entrega e apresentação |

## Escopo do MVP

O projeto prioriza um experimento pequeno, funcional e demonstrável em 12 a 15 minutos. Não fazem parte do escopo obrigatório:

- implementação integral de normas como ISO/IEC, LGPD ou SOC 2;
- Kubernetes ou múltiplos serviços;
- dashboards complexos;
- infraestrutura em nuvem ou ferramentas pagas;
- Docker como requisito de execução.

## Status do projeto

- [x] Repositório e `.gitignore` iniciais
- [x] README inicial e Guia de Contribuição (`CONTRIBUTING.md`)
- [x] Estrutura de diretórios inicial e licença (`LICENSE`)
- [x] Workflow-base no GitHub Actions (`.github/workflows/compliance.yml`)
- [x] Estrutura de aplicação e testes
- [ ] Pipeline completo de conformidade
- [ ] Controles de segurança e dependências
- [ ] Políticas como código
- [ ] Documentação técnica completa
- [ ] Evidências de sucesso, falha e correção
- [ ] Release `v1.0.0`
- [ ] Apresentação e demonstração final

## Referências iniciais

- [GitHub Actions — documentação oficial](https://docs.github.com/actions)
- [Flask — documentação oficial](https://flask.palletsprojects.com/)
- [pytest — documentação oficial](https://docs.pytest.org/)
- [Ruff — documentação oficial](https://docs.astral.sh/ruff/)
- [Gitleaks — repositório oficial](https://github.com/gitleaks/gitleaks)
- [pip-audit — repositório oficial](https://github.com/pypa/pip-audit)
- [Semantic Versioning](https://semver.org/)

As referências utilizadas na fundamentação e na análise dos resultados serão consolidadas em `docs/08-referencias.md`.

# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato baseia-se em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased] (Não Lançado)

Nenhuma alteração registrada.

## [1.0.0] - 2026-08-19

### Adicionado

- Estrutura inicial do projeto e da aplicação base.
- API Flask mínima com as rotas `/` e `/health`.
- Testes automatizados com pytest e relatório JUnit.
- Pipeline de conformidade com verificações de fundação, políticas, segredos,
  qualidade, dependências e testes.
- Artefatos de auditoria do JUnit, Ruff, pip-audit e Gitleaks.
- Script e testes da verificação interna de políticas.
- Catálogo de evidências de aprovação, bloqueio e correção.
- Documentação técnica e registro da reprodução independente da ISSUE-09.

### Alterado

- README, arquitetura, políticas, evidências, auditoria e referências foram
  alinhados ao comportamento entregue.
- O workflow passou a declarar explicitamente a execução em tags semânticas.

### Segurança

- Gitleaks configurado para bloquear segredos e publicar resultado auditável.
- Ruff e pip-audit configurados como controles bloqueantes.
- Arquivos `.env` e `credentials.json` bloqueados pela política interna.

### Limitações conhecidas

- A aplicação é deliberadamente mínima e não inclui autenticação, banco de
  dados, implantação em produção ou observabilidade.
- O pip-audit depende das vulnerabilidades publicadas e da conectividade no
  instante da execução.
- Os artefatos do GitHub Actions têm retenção de 14 dias; os registros Markdown
  preservam os identificadores e resultados essenciais.
- A criação da tag e da GitHub Release é um controle humano, validado pela
  trilha descrita em `docs/07-auditoria.md`.

[Unreleased]: https://github.com/samsilveira/GC_ComplianceEmDevOps/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/samsilveira/GC_ComplianceEmDevOps/releases/tag/v1.0.0

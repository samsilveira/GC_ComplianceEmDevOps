# 01 — Visão Geral do Experimento

Este documento detalha o contexto, problema, objetivos e o recorte prático do experimento **Compliance as Code em Pipelines CI/CD**.

---

## 1. Contexto e Problema

No contexto de DevOps e integração contínua (CI/CD), a velocidade de entrega não deve comprometer a conformidade, a segurança e os requisitos organizacionais. A abordagem tradicional de auditorias manuais e aprovações lentas gera gargalos de entrega e riscos de inconsistência.

A abordagem **Compliance as Code** propõe transformar políticas, regras de governança e controles de segurança em código versionável e verificações automatizadas em tempo de build/pipeline.

---

## 2. Objetivos do Experimento

- Demonstrar a integração prática de ferramentas de qualidade, segurança e governança no GitHub Actions.
- Validar o bloqueio automático de violações controladas (segredos, falhas de políticas, dependências vulneráveis).
- Construir uma trilha de auditoria completa e rastreável.
- Garantir a reprodutibilidade integral por terceiros em ambientes limpos.

---

## 3. Escopo e Limitações do MVP

O experimento é focado em uma aplicação Flask de escopo reduzido para evidenciar o funcionamento do pipeline de conformidade. Não constitui certificação legal ou adesão formal integral a normas externas (ex: ISO 27001, LGPD).

### Incluído

- API Flask determinística com as rotas `/` e `/health`;
- testes funcionais e relatório JUnit;
- lint, detecção de segredos, auditoria de dependências e políticas internas;
- execução em `push` e `pull_request`, com relatórios e histórico de runs;
- evidências dos estados aprovado, bloqueado e corrigido.

### Fora do escopo

- deploy, infraestrutura em nuvem, banco de dados e autenticação;
- certificação ou avaliação jurídica de normas externas;
- monitoramento de produção e resposta a incidentes;
- automação da release, prevista para a ISSUE-10.

## 4. Resultado obtido

Os controles POL-01 a POL-05 estão implementados e bloqueiam o workflow quando falham. A trilha em [`evidence/`](../evidence/README.md) registra execuções reais para aprovação, violações controladas e restauração. A POL-06 está definida, mas ainda depende de revisão humana.

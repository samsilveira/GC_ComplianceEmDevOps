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

# Estrutura — STARTER v5.1 Enterprise + QA Gate

> **AI-Native Runtime Operating System** · 2026-05-20
> **Capability:** ver `governance/skills-governance.md`

```
STARTER/
├── AGENTS.md
├── CONTEXT.md              [humano ≤50L]
├── PRD.md                  [humano]
└── skills/
    ├── runtime/            ★ RUNTIME OS
    │   ├── index.yaml      ★ ordem hot/warm/cold
    │   ├── qa.yaml / handoff.yaml  ★ QA Gate
    │   ├── *.yaml          ★ arquivos operacionais
    │   ├── validate.py
    │   ├── requirements-runtime.txt
    │   └── schema/         ★ JSON Schema (anti-drift)
    │       └── *.schema.json
    ├── governance/
    │   ├── Start-ops.md    ★ orchestrator
    │   └── runtime-protocol.md
    ├── structure/
    ├── local-skills/
    ├── linked-skills/      [reservado · capability futura]
    ├── templates/runtime/  (+ schema/)
    ├── outputs/
    └── cache/              [reservado · sem uso operacional atual]
```

## Classificação de capability

- **Ativa:** `structure/` e `local-skills/`
- **Adiada:** `_deferred/`
- **Futura:** `linked-skills/` e `cache/`

`STRUCTURE.md` descreve a arquitetura esperada do diretório, mas não substitui a governança de capability.

## Fluxo v5

```
index.yaml → validate.py → hot → warm? → cold? → Start-ops → skill → validate → persist
```

## Checklist sessão

- [ ] `index.yaml` lido
- [ ] Hot carregado (3 arquivos)
- [ ] Cold só se trigger
- [ ] `validate.py` OK após edições
- [ ] `state.yaml` atualizado

**Status:** v5.1 enterprise + capability saneada

---

> **Autoria & Rastro de Segurança**
>
> Este documento faz parte do framework **STARTER**, criado e mantido por **Wesley Alves**.
>
> 🔗 [Portfolio](https://wesscrow.github.io/meu-portfolio/) · [LinkedIn](https://www.linkedin.com/in/wessalves/) · [Behance](https://www.behance.net/wesleyalves)
>
> Qualquer reprodução, distribuição ou uso derivado deve manter esta atribuição.
> Última atualização: 2026-06-07

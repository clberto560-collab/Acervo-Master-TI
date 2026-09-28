# Acervo Master TI

> O sistema de conhecimento de um pro-híbrido: Redes + Seguranca + Automacao.

Este nao e um deposito de cursos ou links. E o seu **mecanismo de aprendizado ativo**: tudo aqui nasce de producao propria (notas, labs, scripts, projetos) e alimenta um roadmap de 6 meses ate a empregabilidade.

---

## As 3 Regras de Ouro

1. **Produzir, nao colecionar.** Baixar curso nao e progresso. Progresso = artefato seu. Cada modulo estudado termina EM um arquivo deste acervo. Se voce nao criou nada, nao aprendeu nada.
2. **Nada passa de mes sem projeto.** Cada mes do roadmap entrega um projeto publicavel no GitHub. Teoria sem artefato vira conteudo esquecido em 30 dias.
3. **Revisao espaçada e obrigatoria.** Voce perde ~70% do que estuda em 1 semana sem revisao. O sistema `06-REVISAO` existe para voce reativar conhecimento no ciclo 1d -> 3d -> 7d -> 15d -> 30d (metodo Leitner).

---

## Como usar este acervo (ciclo semanal)

| Dia | Foco | O que produzir |
|-----|------|----------------|
| Dia 1 | **Teoria** (modulo do roadmap) | 1 nota em `01-NOTAS` (explica com suas palavras) |
| Dia 2 | **Pratica guiada** (lab do modulo) | 1 lab documentado em `02-LABS` |
| Dia 3 | **Pratica livre** (variacoes, quebrar e consertar) | Melhorar o lab / novo script em `03-SCRIPTS` |
| Dia 4 | **Revisao** da semana anterior | Flashcards + checklist em `06-REVISAO` |
| Dia 5 | **Revisao** da semana anterior | Flashcards + checklist em `06-REVISAO` |
| (Fim do mes) | **Projeto do mes** | `04-PROJETOS` + publicacao no GitHub |

Carga horaria realista: **1h a 1h30/dia, 5 dias/semana** (5 a 7h semanais). Qualidade do ritual > quantidade de horas.

---

## Estrutura

```
Acervo-Master-TI/
├── 00-ROADMAP/          TRILHA PRINCIPAL: mapa de conhecimento + cronograma 6 meses
│   ├── mapa-do-conhecimento.md      quais areas, ordem e dependencias
│   └── roadmap-6-meses.md           cronograma semana a semana
├── 01-NOTAS/            suas notas de estudo (templates prontos)
├── 02-LABS/             labs praticos documentados (objetivo, topologia, passos, verificacao)
├── 03-SCRIPTS/          scripts Python/Bash comentados e versionados
├── 04-PROJETOS/         os 6 projetos de portfolio + templates
├── 05-CERTIFICACOES/    trilhas de certificacao (CCNA, Security+, ...)
└── 06-REVISAO/          flashcards e checklists de revisao espaçada
```

---

## Como começar

1. Leia `00-ROADMAP/mapa-do-conhecimento.md` (entenda a ordem e por que ela existe).
2. Leia `00-ROADMAP/roadmap-6-meses.md` (seu plano completo).
3. Comece o Mes 1: teoria + lab + nota. Crie o primeiro arquivo na sua pasta `01-NOTAS`.
4. Nunca pule o Dia de Revisao — e o que salva seu progresso.

---

## Regras de higiene do repositorio

- Um conceito/lab/projeto por arquivo. Nada de monolitos.
- Nomes descritivos: `nota-001-subnetting.md`, `lab-003-vlan-por-ssh.md`.
- Imagens (prints de lab, topologia) vao em `assets/` ao lado do arquivo que as usa.
- Projeto so e "concluido" quando o README do projeto responde: o que faz, como roda, e o que voce aprendeu.
- Nada sensivel no git: sem senhas, sem chaves, sem configs de producao (ver `.gitignore`).

---

## Destino final

No Mes 6, este acervo e seu **portfolio vivo**: vira GitHub publico organizado por trilha e por projeto, alimenta LinkedIn, e prova que voce nao so sabe — voce **construiu**.
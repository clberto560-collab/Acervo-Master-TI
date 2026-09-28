# Trilha: Python (aplicado a redes)

**Objetivo:** automatizar configuracao, inspecao e backup de equipamentos de rede.
**Pre-requisito:** Redes basico (IP, SSH, CLI de equipamento).
**Artefato de saida:** scripts reutilizaveis comentados em `03-SCRIPTS`.

---

## Modulos (aulas)

| # | Modulo | Foco | Mes do roadmap |
|---|--------|------|----------------|
| 1 | [Sintaxe basica](modulo-01-sintaxe-basica.md) | variaveis, listas, dicts, funcoes | M2-1 |
| 2 | [Arquivos e dados](modulo-02-arquivos-dados.md) | txt, csv, json | M2-1 |
| 3 | [Erros e logging](modulo-03-erros-logging.md) | try/except, logging | M2-2 |
| 4 | [SSH com Netmiko](modulo-04-ssh-netmiko.md) | conectar e ler `show` | M2-2 |
| 5 | [Dispositivos em lote](modulo-05-dispositivos-em-lote.md) | arquivo + loop + try | M2-3 |
| 6 | [Parse e regex/TextFSM](modulo-06-parse-regex-textfsm.md) | extrair dados de saida | M2-3 |
| 7 | [Backup automatizado (Projeto 2)](modulo-07-backup-automatizado.md) | codigo final de backup | M2-4 |
| 8 | [Push de configs + validacao](modulo-08-push-configs-validacao.md) | VLAN/ACL em lote | M2-4 |

## Regras de codigo para o acervo

- Todo script tem docstring no topo explicando o que faz e como roda.
- Nada de senha hardcoded — variaveis de ambiente ou arquivo `.env` (e nunca no git).
- Rodar sempre em dry-run/ambiente de teste antes de aplicar em dispositivo real.
- Padrao das acoes: **ACAO -> VERIFICACAO -> RELATO** (rode + confirme + log).

## Recursos

- Curso em Video (Python, Mundo 1-3) — base em pt-BR
- FreeCodeCamp / automate the boring stuff — reforco
- Documentacao oficial do Netmiko — o companheiro diario
- Labs do Mes 2 no roadmap para cada modulo

## Checklist de confirmacao

- [ ] Conecta via SSH em um equipamento e le o hostname
- [ ] Executa um `show` e salva a saida em arquivo
- [ ] Aplica configuracao (ex.: VLAN) em 3+ dispositivos com validacao
- [ ] Trata erro de conexao (timeout) sem abortar o lote
- [ ] Tem 3+ scripts prontos, comentados e sem dados sensiveis
- [ ] Projeto 2 (backup) e Projeto 2b (push VLAN/ACL) publicados no GitHub
# Trilha: Python (aplicado a redes)

**Objetivo:** automatizar configuracao, inspecao e backup de equipamentos de rede.
**Pre-requisito:** Redes basico (IP, SSH, CLI de equipamento).
**Artefato de saida:** scripts reutilizaveis comentados em `03-SCRIPTS`.

---

## Topicos na ordem

1. Sintaxe base: variaveis, tipos, condicionais, loops, funcoes
2. Trabalhar com arquivos: ler/escrever .txt, .csv, .json
3. Erros e tratamento: try/except, logging
4. Conexao SSH: `netmiko` e `paramiko` (diferenca e quando usar cada um)
5. Dispositivos em lote: loops sobre lista de IPs lida de arquivo
6. Execucao de comandos remotos e parse de saida (regex basica)
7. Backup automatizado de configuracoes
8. Push de configuracoes (VLAN, ACL, senha) validado com retorno

## Regras de codigo para o acervo

- Todo script tem docstring no topo explicando o que faz e como roda.
- Nada de senha hardcoded — usar variaveis de ambiente ou prompt (`getpass`).
- Rodar sempre em dry-run antes de aplicar em ambiente real.

## Recursos

- Curso em Video (Python, Mundo 1-3) — base em pt-BR
- FreeCodeCamp / automate the boring stuff — reforco
- Documentacao oficial do Netmiko — o companheiro diario
- Pratica guiada: labs do Mes 2 do roadmap

## Checklist de confirmacao

- [ ] Conecta via SSH em um equipamento e lê o hostname
- [ ] Executa um comando `show` e salva a saida em arquivo
- [ ] Aplica uma configuracao (ex.: criar VLAN) em 3+ dispositivos com um script
- [ ] Trata erro de conexao (timeout) de um dispositivo sem abortar o script
- [ ] Tem 3+ scripts prontos, comentados e sem dados sensiveis
# Trilha: Linux

**Objetivo:** operar o sistema onde roda servico, log, firewall e seguranca. Fluencia de terminal, nao de interface grafica.
**Pre-requisito:** Redes basico (IP, SSH, servicos de rede) — Mes 1 concluido.

---

## Modulos (planejados — Mes 3)

| # | Modulo (aula) | Foco | Status |
|---|---------------|------|--------|
| 1 | Terminal, navegacao e arquivos | grep, find, pipes, editor | aguardando (M3-1) |
| 2 | Usuarios, grupos e permissoes | rwx, chmod, chown | aguardando (M3-1) |
| 3 | Processos, servicos e logs | systemctl, ps, journalctl | aguardando (M3-2) |
| 4 | Rede no Linux | ip, ss, DNS, servicos de rede | aguardando (M3-2) |
| 5 | Pacotes e bash script | apt, cron, variaveis | aguardando (M3-3) |
| 6 | SSH server e seguranca | chaves, config, hardening | aguardando (M3-4) |
| 7 | Firewall (ufw/iptables) | regras por porta/origem | aguardando (M3-4) |
| 8 | Hardening essencial (Projeto 3) | servidor seguro do zero + pfSense | aguardando (M3-4) |

> Preenchimento previsto durante o **Mes 3** do roadmap. Esqueleto criado agora para dar o mapa completo da trilha.

## Recursos (planejados)

- Linux Journey — trilha interativa gratuita em ordem
- DIO / cursos de Linux Essentials (orientacao para certificacao)
- Manual `man` de cada comando usado

## Checklist (a validar ao final da trilha)

- [ ] Cria usuario, grupo e ajusta permissoes sem `sudo -i`
- [ ] Instala e configura um servico (SSH ou web) iniciando no boot
- [ ] Agenda tarefa com `cron` e confirma nos logs
- [ ] Cria regra de firewall bloqueando uma porta por IP de origem
- [ ] Encontra evento suspeito em `auth.log` (ex.: tentativa de login falha)
- [ ] Projeto 3 (servidor seguro + pfSense) publicado
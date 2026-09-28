# Trilha: Linux

**Objetivo:** operar o sistema onde roda servico, log, firewall e seguranca. Fluencia de terminal, nao de interface grafica.
**Pre-requisito:** Redes basico (IP, SSH, servicos de rede).
**Artefato de saida:** servidor Linux configurado do zero, do terminal, com firewall e logs.

---

## Topicos na ordem

1. Terminal: navegacao, criacao/edicao de arquivos, `grep`, `find`, pipes
2. Usuarios, grupos e permissoes (rwx, `chmod`, `chown`)
3. Processos e servicos: `systemctl`, `ps`, `top`, logs em `journalctl`
4. Rede no Linux: `ip`, `ss`, `ping`, DNS (`/etc/resolv.conf`)
5. Pacotes: `apt`, atualizacao, repositorios
6. Shell script: variaveis, loops, `cron` para agendamentos
7. SSH server: configuracao, chaves, seguranca basica
8. Firewall: `ufw`/`iptables`, regras por porta e origem
9. Leitura e analise de logs (`/var/log`, `auth.log`, `syslog`)
10. Hardening essencial: atualizacoes, desabilitar servicos, limite de acesso

## Fluxo de estudo

- Instale Debian ou Ubuntu em VM e **use apenas terminal** nessas semanas (sem interface grafica).
- Cada topico gera nota + comando real executado.
- Shell scripts vao para `03-SCRIPTS` versionados.

## Recursos

- Linux Journey — trilha interativa gratuita em ordem
- DIO / cursos gratuitos de Linux Essentials (orientacao para a certificacao)
- Manual `man` de cada comando que voce usar — leia o essencial

## Checklist de confirmacao

- [ ] Cria usuario, grupo e ajusta permissoes sem `sudo -i` o tempo todo
- [ ] Instala e configura um servico (SSH ou web) e o deixa iniciando no boot
- [ ] Agenda tarefa com `cron` e confirma nos logs
- [ ] Cria regra de firewall bloqueando uma porta por IP de origem
- [ ] Encontra um evento suspeito em `auth.log` (ex.: tentativa de login falha)
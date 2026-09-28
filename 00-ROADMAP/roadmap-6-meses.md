# Roadmap de 6 Meses

> Plano ajustado para a pilha correta de aprendizado. Cada mes tem 1 tema central, 1 lab principal e 1 projeto de portfolio.
> Metodo por semana, ver `../README.md`. Foco em producao, nao em volume.

**Carga recomendada:** 1h - 1h30/dia, 5 dias/semana (ritual > quantidade).

---

## MES 1 — Redes de verdade (fundacao)
Tema central: entenda a rede como quem vai operar e atacar depois.

| Semana | Foco | Producao obrigatoria |
|--------|------|----------------------|
| 1 | Modelo OSI, TCP/IP, enderecamento IP, subnetting | nota em `01-NOTAS` (explique CIDR/mascara com suas palavras) |
| 2 | VLAN, switches, acesso, camada 2 | lab: criar e isolar VLANs |
| 3 | Roteamento estatico, tabela de rotas, NAT | lab: 2 roteadores + rotas + NAT |
| 4 | Revisao + fechamento | **PROJETO 1**: topologia 2 switches + 2 roteadores + 4 hosts + documentacao |

**Lab principal:** topologia no GNS3 (ou Packet Tracer) que funcione e voce saiba explicar.
**Ferramentas:** GNS3, Packet Tracer. Recursos: Cisco NetAcad (CCNA1), canal Curso em Video (Redes).
**Criterio de saida:** voce desenha a topologia num papel e explica pacote a pacote o caminho de A ate B.

---

## MES 2 — Python para redes
Tema central: automatizar o que voce aprendeu no Mes 1.

| Semana | Foco | Producao obrigatoria |
|--------|------|----------------------|
| 1 | Python basico: variaveis, listas, funcoes, if/for | nota + 3 scripts simples |
| 2 | SSH em equipamento: netmiko/paramiko | lab: conectar no switch e ler hostname |
| 3 | Loop por varios dispositivos + arquivos | lab: aplicar config em lista de IPs lida de .txt |
| 4 | Revisao + fechamento | **PROJETO 2**: script que conecta em 3+ switches e faz backup das configs |

**Lab principal:** backup automatizado de configuracoes Cisco.
**Cuidado critico:** enfoque em entender *o que* o comando faz na rede (ligue com Mes 1) — senão vira copia de tutorial.

---

## MES 3 — Linux (o ambiente do profissional)
Tema central: operar o SO onde rodam servicos, logs e seguranca.

| Semana | Foco | Producao obrigatoria |
|--------|------|----------------------|
| 1 | Terminal, navegacao, edicao, usuarios e permissoes | nota + script bash basico |
| 2 | Servicos (SSH, servidor web), systemd, agendamento cron | lab: servidor com servicos + tarefa agendada |
| 3 | Rede no Linux, firewall (ufw/iptables), logs | lab: firewall + analise de logs |
| 4 | Revisao + fechamento | **PROJETO 3**: servidor Linux seguro do zero + pfSense virtualizado entre VLANs |

**Lab principal:** pfSense virtualizado com firewall entre redes.
**Dica:** instale Debian/Ubuntu numa VM e use so terminal no dia a dia dessas 4 semanas.

---

## MES 4 — Seguranca de rede na pratica
Tema central: defender e inspecionar o que foi construido.

| Semana | Foco | Producao obrigatoria |
|--------|------|----------------------|
| 1 | Firewall conceitos, ACLs (Cisco) e regras pfSense | lab: bloquear uma VLAN inteira |
| 2 | Seguranca camada 2: port security, DHCP snooping | lab: proteger switch contra acesso indevido |
| 3 | Wireshark + nmap: analise de trafego e descoberta | lab: capturar e identificar protocolos suspeitos |
| 4 | Revisao + fechamento | **PROJETO 4**: lab 3 VLANs + pfSense + monitoramento Wireshark documentado |

**Ferramentas:** pfSense, Wireshark, nmap. **Regra de conduta:** so atacar/buscar vulnerabilidades em ambiente proprio/labs.

---

## MES 5 — Ataque e defesa (Red Team + Blue Team)
Tema central: enxergar como invasor, responder como defensor.

| Semana | Foco | Producao obrigatoria |
|--------|------|----------------------|
| 1 | TryHackMe: Beginner Path — reconhecimento (nmap, gobuster) | notas do que encontrou nas maquinas |
| 2 | TryHackMe: web basico, Burp Suite, metodos de invasao comuns | lab: documentar 1 ataque em VM controlada |
| 3 | Blue Team: Wazuh instalado e coletando logs | lab: Wazuh monitorando Linux/Windows |
| 4 | Dassecao: como detectar os ataques da Semana 1 | **PROJETO 5**: ataque documentado + resposta defensiva com Wazuh |

**Lab principal:** Wazuh coletando logs e alertando.
**Criterio de saida:** voce sabe explicar a fase do ataque (recon -> exploracao -> persistencia) e onde o defender enxerga isso.

---

## MES 6 — Automacao + Portfolio + Empregabilidade
Tema central: transformar tudo em portfólio publicavel e posicionamento de mercado.

| Semana | Foco | Producao obrigatoria |
|--------|------|----------------------|
| 1 | Docker: imagem, container, volume, Dockerfile | lab: colocar Zabbix ou Snort em container |
| 2 | Ansible: playbook criando usuarios, firewall, pacotes | lab: playbook de hardening de servidor |
| 3 | GitHub: organizar os 6 projetos, READMEs, prints, documentacao | repos curados + docs |
| 4 | Curriculo + LinkedIn + definicao de certificacao | **PROJETO 6**: curriculo tecnico + GitHub + LinkedIn prontos |

**Atividade paralela de todo o mes:** iniciar trilha da certificacao escolhida (CCNA ou Security+) — ver `05-CERTIFICACOES`.

---

## Projetos de portfolio (o que sera publicado no GitHub)

| # | Projeto | Demo clara |
|---|---------|-----------|
| 1 | Topologia de rede: 2 switches + 2 roteadores + 4 hosts | topologia + explicacao do caminho do pacote |
| 2 | Automacao de backup/config Cisco com Python (netmiko) | script + prints do resultado |
| 3 | Infra segura: pfSense + VLANs + servidor Linux | regras + topologia + verificação |
| 4 | Lab de seguranca: 3 VLANs + bloqueio + analise Wireshark | prints de captura + regras comentadas |
| 5 | Ataque documentado + defesa com Wazuh | timeline ataque/defesa + alertas |
| 6 | Portfolio: GitHub + LinkedIn + curriculo tecNico | links publicos |

---

## Regras de progresso

- **Nao pule revisao** do dia 4-5. Se acumular, a revisao da proxima semana vira a aula perdida.
- **Mes incompleto = mes refeito.** Se nao produziu o projeto do mes, repita o mes em vez de avancar.
- **Estude em blocos de 45-50 min** com pausa de 10 (tecnicas de foco aplicadas).
- **Quando travar 30+ min em algo:** note a tentativa, marque como duvida, siga. A duvida volta na revisao.

## Certificacoes (ao final)

- Foco 1: **CCNA** (rede) — se quer analista/engenheiro de redes.
- Foco 2: **Security+** (seguranca) — se quer trilha cyber.
- Base de apoio: Linux Essentials, PCAP (Python). Cloud Practitioner so depois.
# Trilha: Redes

**Objetivo:** falar, operar e explicar redes como quem trabalha com isso todo dia.
**Pre-requisito:** nenhum (e a fundacao de tudo).
**Artefato de saida:** topologia completa documentada + fluencia em subnetting.

---

## Modulos (aulas)

| # | Modulo | Foco | Mes do roadmap |
|---|--------|------|----------------|
| 1 | [Modelo OSI e TCP/IP](modulo-01-modelo-osi-tcpip.md) | camadas, por que existem, Wireshark basico | M1-1 |
| 2 | [IPv4, CIDR e Subnetting](modulo-02-ipv4-subnetting.md) | mascaras, sub-redes, contas | M1-1 |
| 3 | [IPv6 basico](modulo-03-ipv6-basico.md) | formato, tipos, SLAAC, dual-stack | M1-1 |
| 4 | [Ethernet, MAC e Switches](modulo-04-ethernet-switch-mac.md) | frame, tabela MAC, ARP, switch | M1-2 |
| 5 | [VLAN, VTP e STP](modulo-05-vlan-vtp-stp.md) | isolamento, 802.1Q, trunk, loop | M1-2 |
| 6 | [Roteamento estatico e NAT](modulo-06-roteamento-nat.md) | rotas, default route, NAT/PAT | M1-3 |
| 7 | [TCP e UDP](modulo-07-tcp-udp.md) | camada 4, portas, handshake | M1-4 |
| 8 | [DHCP e DNS](modulo-08-dhcp-dns.md) | DORA, resolucao, registros | M1-4 |
| 9 | [CLI Cisco](modulo-09-cli-cisco.md) | modos, config, SSH, backup | M2-1 |
| 10 | [OSPF e BGP (conceitos)](modulo-10-ospf-bgp.md) | dinamico: IGP vs EGP | M1-4 |

## Fluxo de estudo

- Cada modula = 1 nota em `01-NOTAS` + 1 lab em `02-LABS` (nunca so teoria).
- Depois de cada modulo, transfira as duvidas para flashcards (`06-REVISAO`).
- Redes so faz sentido quando voce monta as maos: lab em GNS3/Packet Tracer desde o modulo 2.

## Recursos

- Cisco Networking Academy (CCNA1 e CCNA2) — base oficial e estruturada
- Curso "Redes de Computadores" (Curso em Video) — conceitos em pt-BR
- Livro: "Redes de Computadores" (Tanenbaum) — consulta, nao leitura linear
- Pratica: GNS3 (pro) / Packet Tracer (iniciante)

## Checklists (forno para validar a trilha)

- [ ] Calcula subnetting de cabeca/com folha em < 1 min para /24 e /28
- [ ] Desenha e explica o trajeto de um pacote entre 2 hosts de VLANs diferentes
- [ ] Configura roteador/switches via CLI sem consultar guia
- [ ] Explica por que STP existe e o que ele impede
- [ ] Diferencia TCP vs UDP e sabe qual usar em cada situacao
- [ ] Configura/Sedh opera OSPF e identifica lotes BGP na tabela
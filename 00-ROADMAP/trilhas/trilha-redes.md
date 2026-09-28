# Trilha: Redes

**Objetivo:** falar, operar e explicar redes como quem trabalha com isso todo dia.
**Pre-requisito:** nenhum (e a fundacao de tudo).
**Artefato de saida:** topologia completa documentada + fluencia em subnetting.

---

## Topicos na ordem

1. Modelo OSI vs TCP/IP — o que cada camada faz
2. Enderecamento IPv4: IP, mascara, CIDR, subnetting, classe/utilizacao pratica
3. Enderecamento IPv6: conceitos basicos (enderecamento, prefijo)
4. Camada 2: Ethernet, MAC, switches, VLAN, VTP, STP
5. Camada 3: roteamento estatico, tabela de rotas, gateway, NAT
6. Camada 4: TCP e UDP (portas, handshake, quando usar cada um)
7. DHCP e DNS — como hosts e servicos resolvem e se configuram
8. Acessar e configurar equipamentos via CLI (modos, SSH, senhas)
9. Roteamento dinamico: OSPF e BGP (conceitos, quando usar)
10. Protocolos de aplicacao: HTTP/HTTPS, FTP, SNMP, telnet/SSH

## Fluxo de estudo

- Cada topico = 1 nota + 1 lab curto (nunca so teoria).
- Depois de cada topico, **responda perguntas tipo prova** (o que acontece se...?) no formato flashcard.
- Redes so faz sentido quando voce monta as maos: lab em GNS3/Packet Tracer desde o topico 2.

## Recursos

- Cisco Networking Academy (CCNA1 e CCNA2) — base oficial e estruturada
- Curso "Redes de Computadores" (Curso em Video) — conceitos em pt-BR
- Livro: "Redes de Computadores" (Tanenbaum) — consulta, nao leitura linear
- Pratica: GNS3 (pro) / Packet Tracer (iniciante)
- Cisco Packet Tracer: uso em todas as semanas do Mes 1

## Checklist de confirmacao (voce sabe quando dominou)

- [ ] Calcula subnetting de cabeca/com folha em menos de 1 min para /24 e /28
- [ ] Desenha e explica o trajeto de um pacote entre 2 hosts de VLANs diferentes
- [ ] Configura roteador/switches via CLI sem consultar guia
- [ ] Explica por que STP existe e o que ele impede
- [ ] Diferencia TCP vs UDP e sabe em quais situacoes cada um e usado
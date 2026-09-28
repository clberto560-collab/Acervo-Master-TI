# Modulo 4 — Ethernet, MAC e Switches (Camada 2)

> Trilha: Redes | Mes 1, Semana 2 | Aula 4

## Objetivo

Entender como frames chegam ao destino em uma LAN: endereco MAC, tabela de MACs do switch, e arquitetura Ethernet. E a base para VLANs e seguranca de camada 2.

## Teoria

### MAC (Media Access Control)

- Endereco **fisico** da interface (graneado na placa), com **48 bits** (12 hex).
- Formato: `AA:BB:CC:DD:EE:FF`. Os 3 primeiros grupos identificam **fabricante** (OUI); os 3 ultimos sao unicos do dispositivo.
- Num `ipconfig` no Windows: `Endereco fisico`. No Linux `ip link`: `link/ether`.

### Ethernet e o frame

- Ethernet opera na **camada 2** (enlace).
- Frame Ethernet II: **MAC destino + MAC origem + Tipo (0x0800 = IPv4, 0x86DD = IPv6) + Payload + FCS (checagem)**.
- A camada 2 entrega dentro do **mesmo enlace** (rede local / domínio de broadcast). Para alem dele, quem decide e a camada 3 (roteador) — por isso MACs **mudam a cada salto**, IPs **nao**.

Regra de ouro: **IP nao muda de ponta a ponta; MAC muda a cada enlace.**

### Como o switch decide o que fazer

O switch nao "sabe" roteamento: ele tem uma **tabela MAC** e decide:

1. **Desconhecido (flood):** nao sabe quem tem o MAC destino -> entrega em todas as portas (menos a origem) — "broadcast" da camada 2.
2. **Conhecido (forward):** sabe a porta -> entrega na porta certa.
3. **Destino = broadcast (ffff...)** ou o host ARP: sempre flood.
4. **Origem na tabela numa porta diferente (mudou de lugar):** atualiza a tabela (aprende).

Mecanismo de aprendizado: ao receber um frame, o switch le o **MAC de origem** e grava `<MAC, porta, timestamp>`.

### ARP (ponte camada 3 <-> 2)

Para enviar para um IP do mesmo enlace: `arp -a` mostra o mapeamento IP -> MAC. Protocolo ARP pergunta: "quem tem o IP X?" — o dono responde com seu MAC. Isso sera importante em seguranca (spoofing de ARP).

### Half vs Full duplex

- **Half-duplex:** so fala ou escuta por vez (hub/CSMA/CD, antigo).
- **Full-duplex:** fala e escuta simultaneamente (switch moderno) — comutacao "store-and-forward" com CRC.

### Switch vs Hub vs Roteador (nao confundir)

| Item | Camada | O que decide |
|------|--------|--------------|
| Hub | 1 | pensa: repete bit em todas portas |
| Switch | 2 | tabela MAC (encaminha frames na porta certa) |
| Roteador | 3 | tabela de rotas (encaminha pacote a outro enlace) |

## Exemplo pratico no CMD

```
arp -a            -> veja o gateway: qual MAC corresponde ao IP do roteador
ping 192.168.1.1  -> gera ARP para o gateway; depois "arp -a" mostra o MAC novo
ipconfig /all     -> MAC do seu adaptador
```

No Wireshark, capture um `ping` e observe: dois pares de MAC (origem/destino) no header Ethernet — origem e seu PC, destino e o gateway (se o destino for externo).

## Lab guiado (40 min) — Pacote de montagem para camada 2

1. Topologia no Packet Tracer/GNS3: **1 switch + 2 PCs** (PC-A, PC-B).
2. Configure IPs: PC-A `10.0.0.1/24`, PC-B `10.0.0.2/24` (mesma rede).
3. No switch (CLI):
   ```
   enable
   show mac address-table
   ```
   Tabela vazia (ou quase).
4. Ping de PC-A para PC-B.
5. `show mac address-table` novamente:
   - Veja **2 entradas** (MAC do PC-A e MAC do PC-B) com a porta de cada um.
6. (Se usar Wireshark) filtre `arp` e veja o protocolo ARP realizando a consulta que descrevemos.
7. Adicione 1 PC-C e **mova o cabo** do PC-B para outra porta: o switch deve reeditar a entrada (repeticao do aprendizado no ponto 2).

## Verificacao — "sei que aprendi quando..."

- [ ] Explico a diferenca entre encaminhar por MAC e por IP em 2 frases
- [ ] Sei por que o switch "flood" o frame quando nao conhece o destino
- [ ] Descrevo o frame ethernet e o que ele carrega (MAC origem/destino, tipo, payload)
- [ ] Com `arp -a` entendo o mapa IP<->MAC e explico quando ele e usado
- [ ] Expliquei a tabela MAC do switch por que ela e/ou nao necessaria para o PC saber o MAC do gateway

## Conexao com o roadmap

- Camada 2 e direto para: VLAN (Modulo 5), seguranca de acesso (Port Security, DHCP snooping — Mes 4, trilha seguranca).
- No Mes 4 vai ser util enxergar ataques na camada 2 (ARP spoofing, MAC flood).

## Para ir alem (opcional)

- Ler: "Spanning Tree Protocol" (STP) — modulo seguinte já vai precisar.
- Se tiver lab real: teste com hub forneceria flood constante (simulador nao tem quedas como no mundo real). Se tiver hub/WIRES no laboratorio real, veja a diferenca no numero de colisoes num datagrama via Wireshark.
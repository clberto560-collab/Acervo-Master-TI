# Trilha: Seguranca

**Objetivo:** defender (Blue Team) e entender o ataque (Red Team), sempre em ambiente controlado.
**Pre-requisito:** Redes + Linux (Meses 1-3 do roadmap).

---

## Modulos (planejados — Mes 4 e 5)

| # | Modulo (aula) | Foco | Status |
|---|---------------|------|--------|
| 1 | Postura de seguranca | CIA, superficie de ataque | aguardando (M4-1) |
| 2 | Firewall: ACLs Cisco e pfSense | bloquear rede de rede | aguardando (M4-1) |
| 3 | Seguranca de camada 2 | Port Security, DHCP snooping | aguardando (M4-2) |
| 4 | Wireshark e analise de trafego | filtros, protocolos suspeitos | aguardando (M4-3) |
| 5 | Descoberta com nmap | scan, servicos, OS | aguardando (M4-3) |
| 6 | IDS/IPS: Snort/Suricata | assinaturas e alertas | aguardando (M4-4) |
| 7 | Wazuh: monitoramento e resposta | coleta de logs, alertas | aguardando (M5-3) |
| 8 | VPN e autenticacao | wireguard, RADIUS, 802.1X | aguardando (M5) |
| 9 | Red Team basico (TryHackMe) | recon, Burp Suite, exploits (lab!) | aguardando (M5-1/2) |
| 10 | Defesa contra ataques (Projeto 5) | deteccao com Wazuh | aguardando (M5-4) |

> Preenchimento previsto durante os **Meses 4-5** do roadmap. Esqueleto criado agora para dar o mapa completo.

## Regra de ouro (conduta)

- Ferramentas ofensivas (nmap, hping3, brute-force, exploits) **somente em voce, nos seus labs**.
- Nada contra sistemas de terceiros sem autorizacao por escrito.
- Tudo aqui documenta ambiente proprio e controlado.

## Recursos (planejados)

- TryHackMe (Beginner Path) — Red Team guiado
- PortSwigger Web Security Academy — web security gratuita
- Documentacao Wazuh / pfSense — labs reais

## Checklist (a validar ao final da trilha)

- [ ] Bloqueia uma VLAN/sub-rede inteira com regra de firewall e prova com captura
- [ ] Protege um switch (port security) e demonstra o bloqueio
- [ ] Identifica no Wireshark: scan, conexao suspeita, trafico HTTP fora do esperado
- [ ] Explica as 4 fases de um ataque (recon -> exploracao -> estabelecimento -> persistencia)
- [ ] Wazuh alertando por evento testado por voce
- [ ] Projetos 4 e 5 publicados
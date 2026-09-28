# Trilha: Seguranca

**Objetivo:** defender (Blue Team) e entender o ataque (Red Team), sempre em ambiente controlado.
**Pre-requisito:** Redes + Linux.
**Artefato de saida:** lab de bloqueio/deteccao documentado + base em analise de trafego.

---

## Topicos na ordem

1. Postura de seguranca: CIA (confidencialidade, integridade, disponibilidade), superficie de ataque
2. Firewall: conceitos, ACLs (Cisco) e regras pfSense — bloquear uma rede inteira de outra
3. Seguranca de camada 2: Port Security, DHCP snooping, limitacao de MAC
4. Analise de trafego: Wireshark (filtros, seguindo fluxos TCP), protocolos suspeitos
5. Descoberta de rede: nmap (scan, deteccao de servicos/OS)
6. IDS/IPS: Snort, Suricata, assinaturas e alertas
7. Monitoramento e resposta: Wazuh (coleta de logs, FIM, alertas)
8. VPN e autenticacao: wireguard/OpenVPN, RADIUS/802.1X (conceitos)
9. Postura Red Team (labs so em ambiente proprio): fateamento de servicos, brute-force basico, Burp Suite
10. Defesa contra os ataques estudados: porque o ataque funcionou e como detectar

## Regra de ouro (conduta)

- Ferramentas ofensivas (nmap, hping3, brute-force, exploits) **somente em você, nos seus labs**, nunca contra sistemas de terceiros sem autorização.
- Tudo no acervo documenta ambiente proprio e controlado.

## Recursos

- TryHackMe (Beginner Path) — Red Team com laboratorios guiados
- PortSwigger Web Security Academy — seguranca web pratica e gratuita
- Documentacao Wazuh / pfSense — labs reais
- Cisco (ACLs), pfSense docs (regras)

## Checklist de confirmacao

- [ ] Bloqueia uma VLAN/sub-rede inteira com regra de firewall e prova com captura
- [ ] Protege um switch contra conexao indevida (port security) e demonstra o bloqueio
- [ ] Identifica no Wireshark: scan, conexao suspeita, trafico HTTP fora do esperado
- [ ] Explica as 4 fases de um ataque (recon -> exploracao -> estabelecimento -> persistencia)
- [ ] Tem o Wazuh alertando por evento testado por voce mesmo
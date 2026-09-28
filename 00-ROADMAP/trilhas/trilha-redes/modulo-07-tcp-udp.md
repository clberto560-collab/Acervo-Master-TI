# Modulo 7 — TCP e UDP (Camada 4)

> Trilha: Redes | Mes 1, Semana 4 | Aula 7

## Objetivo

Entender o que a camada de transporte faz e por que a Internet inteira depende de duas filosofias opostas: TCP (seguro e caro) e UDP (rapido e simples). Direto para analise de trafego e seguranca (Wireshark/nmap).

## Teoria

### O papel da camada 4

A camada de transporte cuida da **entrega fim-a-fim** entre aplicacoes. Duas decisoes-chave:

1. **Portas:** identificam a aplicacao dentro de um host (de 0 a 65535).
   - Bem conhecidas (<1024): HTTP 80, HTTPS 443, SSH 22, DNS 53, DHCP 67/68, SMTP 25, NTP 123, SNMP 161.
   - Nao confundir: **porta escolhe o app**, IP escolhe a maquina.
2. **Multiplexacao:** varios apps usando a mesma rede, cada um na sua porta.

### TCP (Transmission Control Protocol)

Filosofia: **entrega garantida, em ordem, sem erros**. Preco: mais bytes e mais latencia.

- **3-way handshake** para abrir conexao:
  ```
  Cliente -> SYN        (sincronizo; proponho numero de sequencia)
  Servidor -> SYN-ACK   (recebido; confirma + propoe o dele)
  Cliente -> ACK        (confirmado; conexao aberta)
  ```
- **Flags:** SYN, ACK, FIN, RST, PSH, URG.
- **Controles:** numero de sequencia (montar em ordem), ACKs de recebimento, janela de recepcao (quanto pode mandar antes de esperar), retransmissao em perda.
- **Fechamento:** FIN/ACK ou RST (abrupto).
- Exemplos: HTTP/S, e-mail, SSH, banco. Quase tudo que precisa de confiabilidade.

### UDP (User Datagram Protocol)

Filosofia: **mando e vejo no que da**. Sem conexao, sem garantia, sem reordenação. Custo: nada — 8 bytes de header.

- Nao faz handshake (fire-and-forget).
- Exemplos: DNS, DHCP, VoIP, video/streaming, jogos, SNMP — tudo que priorizaria velocidade/volume a garantia.

### Vision geral (comparacao)

| | TCP | UDP |
|--|-----|-----|
| Conexao | sim (handshake) | nao |
| Confiabilidade | entrega garantida | melhor esforco |
| Ordem | sim | nao |
| Controle de fluxo/congestionamento | sim | nao |
| Header | 20 bytes+ | 8 bytes |
| Uso | web, email, ssh, banco | dns, dhcp, voip, video |

### TCP e seguranca (importante ja)

- **SYN flood:** invasor enche o servidor de SYN sem completar handshake -> servidor esgota memoria. (Volta no Mes 4/5.)
- **Port scan:** nmap envia SYN e interpreta resposta (SYN/ACK = porta aberta, RST = fechada). Base de reconhecimento.

## Exemplo pratico no CMD

```
netstat -an | findstr :443        -> conexoes estabelecidas na porta 443
netstat -an | findstr :53         -> veja DNS (padrao UDP :53)
```
No Wireshark:
- Abra um site (https), filtre `tcp`.
- Veja o **3-way handshake** no inicio: pacotes com SYN -> SYN/ACK -> ACK.
- Clique num pacote: **Source port / Sequence number / Acknowledgment number**.

## Lab guiado (30 min)

1. Inicie captura no Wireshark.
2. No CMD: `nslookup exemplo.com` (gera trafego UDP/DNS).
3. No navegador: acesse `https://exemplo.com` (gera TCP).
4. Filtre:
   - `udp.port == 53` — veja DNS over UDP (perguntas/respostas)
   - `tcp.flags.syn == 1` — veja os inicios de handshake
5. Escreva 1 paragrafo: "o que o Wireshark me mostrou de TCP e UDP" (isso vira nota em 01-NOTAS).
6. (Intermediario) Filtrando `tcp.analysis.retransmission` — se aparecer, houve perda/retransmissao na sua rede (explicar).

## Verificacao — "sei que aprendi quando..."

- [ ] Descrevo o 3-way handshake e o que cada flag faz
- [ ] Listo 3 portas bem conhecidas e seus protocolos
- [ ] Decido (com justificativa) quando usar TCP vs UDP num cenario dado
- [ ] No Wireshark identifico SYN/SYN-ACK/ACK num fluxo real
- [ ] Explico SYN flood e port scan em < 2 min (preparando Mes 4)

## Conexao com o roadmap

- A camada 4 e onde voce vai enxergar ataques (reconhecimento, floods) — Seguranca (Mes 4/5).
- Netmiko (Python) usa TCP/SSH — entender transporte ajuda a depurar timeout de conexao.

## Para ir alem (opcional)

- Ler "TCP congestion control" (conceito) — porque a rede nao congestiona em uso normal.
- Experimentar: `tcp.port == 443` no Wireshark (flitro de porta, não de protocolo — erro comum de iniciante).
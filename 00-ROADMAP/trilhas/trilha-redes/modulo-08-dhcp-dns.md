# Modulo 8 — DHCP e DNS

> Trilha: Redes | Mes 1, Semana 4 | Aula 8

## Objetivo

Entender como os hosts adquirem IP (DHCP) e como nomes se tornam IPs (DNS) — os dois servicos que voce vai configurar/configurar em qualquer rede e monitorar em sua seguranca.

## Teoria

### DHCP (Dynamic Host Configuration Protocol)

Entrega **configuracao automatica de rede** ao host: IP, mascara, gateway, DNS, e servidor NTP. UDP na porta 67/68 — **funciona por broadcast** (nao vai a outro dominio de broadcast).

**Processo DORA:**

```
D - Discover  (host procura: "existe DHCP al?" -> broadcast)
O - Offer      (servidor oferece um IP + config ao host)
R - Request    (host pede formalmente aquele IP)
A - Ack        (servidor confirma; host usa o IP)
```

- **Lease (arrendamento):** o IP e "emprestado" por um tempo (ex.: 8h, 1 dia). Antes de vencer, o host renova.
- **Pool/Range:** faixa de enderecos que o servidor pode distribuir.
- **DHCP Snooping (seguranca):** valida os "DHCP Offers" em portas confiaveis, evitando DHCP rogue (um switch falso entregando IPs) — teoria da trilha de seguranca.

Comando importante (Cisco router as DHCP server):
```
ip dhcp excluded-address 192.168.1.1        ! reserva o gateway
ip dhcp pool LAN
  network 192.168.1.0 255.255.255.0
  default-router 192.168.1.1
  dns-server 8.8.8.8
```

### DNS (Domain Name System)

Converte **nome** (`exemplo.com`) em **IP** (o "telefone da Internet"). Baseado em UDP/TCP 53, hierarquico e distribuido — ninguem guarda a Internet inteira.

Fluxo de resolucao:

1. Host consulta o resolutor configurado (seu ISP/Router, ex.: 8.8.8.8).
2. **Cache:** primeiro verifica se ja sabe a resposta (memoria local).
3. Vai ao **root** -> TLD (`com`) -> autoritativo (`exemplo.com`) -> IP final.

Cadeia de registros:
- **A:** nome -> IPv4
- **AAAA:** nome -> IPv6
- **CNAME:** alias de nome
- **MX:** servidor de e-mail
- **NS:** autoridade do dominio
- **PTR:** IP -> nome (reverso)

Tipos de ataque relacionados (Mes 4/5): **DNS spoofing/pollution**, **DNS rebinding**, **DNS tunneling** (exfiltracao usando DNS). o monitoramento de DNS e essencial em SOC.

## Exemplo pratico no CMD

```
ipconfig /all         -> veja: DHCP habilitado, Lease obtido, servidor DHCP, DNS
nslookup exemplo.com  -> responde o IP (e com -type=A / AAAA muda o tipo)
nslookup -type=MX gmail.com
```

No Wireshark, filtre `dhcp` e `dns` para ver as mensagens reais.

## Lab guiado (40 min)

1. Topologia: **1 switch + 1 roteador + 3 PCs** (como se fosse rede de casa).
2. No roteador, configure o DHCP (comandos do exemplo acima) no subsistema da LAN.
3. PCs em **DHCP** (nao IP manual). Veja: cada um recebe IP do pool.
4. Verifique lease: `ipconfig /all` -> "Concedido em"/"Expira em".
5. **Perda de renovacao:** desligue o servidor DHCP e force `ipconfig /release` + `ipconfig /renew` -> repare o que acontece (sem resposta = IP APIPA 169.254.x.x no Windows).
6. Configure **DNS**: `nslookup exemplo.com` (deve resolver). Depois aponte o DNS do PC da rede para um inexistente e veja a falha.
7. (Avançado/Opcional) DNS local: crie registro no roteador/servidor para `lab.local` e teste.

## Verificacao — "sei que aprendi quando..."

- [ ] Explico DORA de memória e o que acontece se o DHCP nao responde
- [ ] Configuro um pool DHCP num roteador sem consulta
- [ ] Explico a cadeia de resolucao DNS (resolutor -> root -> TLD -> autoritativo)
- [ ] Com `nslookup` identifico tipo de registro e IP resolvido
- [ ] Sei em que porta o DNS e o DHCP rodam (53, 67/68) e quando usam UDP/TCP

## Conexao com o roadmap

- Servico co-planejado no Projeto 3 (Linux: dnsmasq ou pfSense com DHCP).
- Ataque DNS/DHCP reaparece em Seguranca (Mes 4/5): DHCP rogue, DNS poisoning.

## Para ir alem (opcional)

- Testar com seu provedor: `nslookup -type=NS netflix.com`.
- Ler uso de over HTTPS/DoH (DNS criptografado para privacidade).
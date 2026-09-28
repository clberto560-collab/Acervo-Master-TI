# Modulo 2 — Enderecamento IPv4, CIDR e Subnetting

> Trilha: Redes | Mes 1, Semana 1 | Aula 2

## Objetivo

Calcular subnetting com fluencia (na mao e "de cabeca") e entender por que enderecos sao divididos em rede e host. Sem isso, nao se configura nada de rede nem se entende firewall.

## Teoria

### O que e um IPv4

Um endereco IPv4 tem **32 bits**, escritos em 4 octetos de 8 bits separados por ponto: `192.168.1.10`.

Cada octeto: 00000000 a 11111111 = **0 a 255**. (Nao confunda _o numero_ com _a string_: octeto e binario de 8 casas.)

### Rede + Host

Um IP nao anda sozinho: anda **com uma mascara** (`255.255.255.0` ou `/24`). Ela diz quantos bits sao **rede** e quantos sao **host**.

```
192.168.1.10/24
            ^^^^ mascara em "notacao CIDR" = 24 bits para rede, 8 bits para host
255.255.255.0  = notacao decimal da mesma mascara (24 uns + 8 zeros)
```

- **Rede:** parte fixa que identifica a "rua".
- **Host:** parte variavel que identifica a "casa".

### Regras de ouro (decorar de tanta usar)

- **Endereco de rede:** todos os bits de host = 0 → `192.168.1.0/24`
- **Broadcast:** todos os bits de host = 1 → `192.168.1.255/24`
- **Hosts utilizaveis:** `2^(bits de host) - 2` (tira rede e broadcast)
  - /24 → 2^8 - 2 = **254**
- **Sua mascara mais comum:** /24

### Conta de subnetting (metodo rapido)

Os valores que importam por octeto (do maior ao menor): **128, 64, 32, 16, 8, 4, 2, 1**.

Qualquer mascara decimal = soma dos bits 1.
```
255 = 11111111
240 = 11110000  (128+64+32+16)
252 = 11111100  (adiciona 4)
```

**Passo para subdividir uma rede (subnetting):**

1. Quantos hosts por subrede? Pegue `2^n >= hosts + 2` → numero de bits de host (n).
2. Bits de rede do prefixo restante: `prefixo + (32 - prefixo - n)`... na pratica: **pule o espaco de hosts**.
3. O **bloco** (salto entre sub-redes) no ultimo octeto relevante = **256 - valor da mascara naquele octeto**.

Exemplo clasico: dividir `192.168.1.0/24` em 4 sub-redes.
- 4 sub-redes = 2 bits emprestados → mascara vira `/26` (255.255.255.**192**).
- Salto = 256 - 192 = **64**.
- Sub-redes: `.0/26` (hosts 1-62), `.64/26` (65-126), `.128/26` (129-190), `.192/26` (193-254).
- Cada sub-rede: 2^6 - 2 = **62 hosts utilizaveis**.

### Tabelas que valem ouro

| Mascara | CIDR | Hosts utilizaveis | Total de enderecos |
|---------|------|-------------------|--------------------|
| 255.255.255.0 | /24 | 254 | 256 |
| 255.255.255.128 | /25 | 126 | 128 |
| 255.255.255.192 | /26 | 62 | 64 |
| 255.255.255.224 | /27 | 30 | 32 |
| 255.255.255.240 | /28 | 14 | 16 |
| 255.255.255.248 | /29 | 6 | 8 |
| 255.255.255.252 | /30 | 2 | 4 |

Regra pratica para memorizar: **/24 = 254 hosts; cada +1 na mascara (ou /25, /26) divide o numero de hosts aproximadamente pela metade.**

### Classes (existe, mas hoje e raro na pratica)

- A: 1.0.0.0/8 (10.x privado), B: 128.x/16 (172.16 a 172.31 privado), C: 192.x/24 (192.168.x privado).
- **Privados** (RFC 1918): 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. **Loopback:** 127.0.0.1.

## Exemplo pratico

Empresa com 3 departamentos precisa de 3 redes separadas:

- Financeiro: 40 hosts -> 6 bits de host -> /26 (62 hosts) ok.
- TI: 20 hosts -> 5 bits -> /27 (30 hosts).
- Marketing: 100 hosts -> 7 bits -> /25 (126 hosts).

Distribuicao a partir de `10.0.0.0/24`:
- `10.0.0.0/25` -> marketing (0-127)
- `10.0.0.128/26` -> financeiro (128-191)
- `10.0.0.192/27` -> TI (192-223)

Verificar: blocos nao se sobrepoem e todas as contas batem com o numero de hosts.

## Lab guiado (40 min)

1. Abra o Packet Tracer (ou use papel e calculadora!)
2. Crie 4 sub-redes de `192.168.1.0/24` com mascara /26 (blocos 0, 64, 128, 192).
3. Configure 2 PCs numa mesma sub-rede (ex.: 192.168.1.2 e .3 /26, gateway .1):
   - Gateway = primeiro host utilizavel = 192.168.1.1
4. Configure 1 PC em outra sub-rede (ex.: 192.168.1.66).
5. `ipconfig` em cada PC (veja IP, mascara, gateway).
6. **Teste:** `ping` entre PCs da MESMA rede (deve responder) e entre redes DIFERENTES (não deve, sem roteador — use como motivacao para o Modulo 6).
7. Confira no Wireshark/Packet Tracer o IP de origem/destino do pacote.

## Verificacao — "sei que aprendi quando..."

- [ ] Convierto ipv4 decimal <-> binario octeto a octeto na mao
- [ ] Calculo sub-redes e hosts utilizaveis sem consultar (ex.: dividir /24 em 8 partes = /27 = 30 hosts)
- [ ] Identifico rede e broadcast de qualquer prefixo dado
- [ ] Explico por que se remove 2 enderecos (rede + broadcast)
- [ ] Mascara /30 só tem 2 hosts (pontos-a-ponto entre roteadores)

## Conexao com o roadmap

- Base para: roteamento (Modulo 6), firewall/ACL (Seguranca, Mes 4), DHCP (Modulo 8).
- Em labs futuros, sempre determine o CIDR antes de pensar em regras.

## Para ir alem (opcional)

- Praticar com o gerador de subnetting: "subnettingpractice.com" (faca 10 exercicios ao dia).
- IPv6 reserva um espaço para reconexao automatica (Stateless Address Autoconfiguration) — tema do proximo modulo.
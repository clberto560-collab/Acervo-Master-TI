# Modulo 3 — IPv6 (conceitos basicos)

> Trilha: Redes | Mes 1, Semana 1 | Aula 3

## Objetivo

Conhecer por que o IPv6 existe, como ler um endereco IPv6 e quais tipos sao mais comuns no mercado. Nao precisa dominar tudo — precisa nao se assustar quando ver `fe80::1` num comando.

## Teoria

### Por que IPv6?

- IPv4 tem 2^32 enderecos (~4,3 bilhoes) e a Internet cresceu alem disso.
- IPv6 tem **2^128** enderecos → praticamente inesgotavel. Isso muda a mentalidade: **nao existe NAT "para salvar enderecos"**.
- Entre as consequencias: cada dispositivo pode ter um IP publico real (menos NAT = menos complexidade para seguranca/entrega).

### Formato

- **128 bits**, escritos em **8 grupos de 4 hexadecimais** separados por `:`:
  ```
  2001:0db8:85a3:0000:0000:8a2e:0370:7334
  ```
- **Regra de encurtamento:**
  1. Zeros a esquerda dentro do grupo podem sumir: `0db8` -> `db8`; `085a` -> `85a`.
  2. Uma (e so UMA) sequencia de grupos todos `0000` pode virar `::`:
     ```
     2001:db8:85a3::8a2e:370:7334
     ```
  - `::1` = loopback (equivalente do 127.0.0.1).
  - `fe80::/10` = **link-local** (usado automaticamente em cada interface, não roteado).

### Tipos principais

| Tipo | Prefixo | Para que serve |
|------|---------|----------------|
| Global unicast | 2000::/3 | Endereco publico roteado na Internet |
| Link-local | fe80::/10 | Sempre presente em cada interface; comunica apenas naquele enlace (vizinhas) |
| Unique local | fc00::/7 | Equivalente "privado" de um site (opcional) |
| Multicast | ff00::/8 | Envio grupo a grupo (substitui o broadcast do IPv4) |

**Nao ha broadcast em IPv6:** usa multicast/neighbor communication.

### Como um host se vira sozinho

Dois mecanismos fundamentais:

1. **SLAAC (Stateless Autoconfiguration)**: o roteador anuncia o prefixo (`2001:db8:1::/64`) e o host deriva os 64 bits finais do MAC (sistema EUI-64) ou de forma aleatoria (privacy).
2. **DHCPv6**: quando o administrador precisa de mais controle (menos obrigatorio que DHCPv4).

### Convivendo com IPv4

- **Dual-stack:** rodar IPv4 e IPv6 ao mesmo tempo (padrao hoje).
- **Tunnels (6to4, etc.):** encapsulamento — usado em pontos de transicao.

## Exemplo pratico

No CMD do seu PC:

```
ipconfig
```

Voce vera algo como:
```
Endereco IPv6 . . . . : 2804:14d:5a0c:abcd:2222:1111:aaaa:ffff
Endereco IPv6 link-local : fe80::9c8f:e3a2:12bb:44ff%13
```

- O `%13` indica o "zone index" (qual interface/quais enlaces para alcancar o vizinho) — nao faz parte do endereco.

No Linux:
```
ip -6 addr show
```

## Lab guiado (20 min, sem muita dependencia)

1. No CMD, `ipconfig` e anote o **IPv6 global** e o **link-local** da sua placa.
2. Teste ping para o loopback IPv6: `ping ::1`
3. Ping para o link-local de outra maquina (se tiver): `ping fe80::...%indice` ou simplesmente `ping fe80::1` em casa de router.
4. Ferramenta externa: `ping -6 google.com` (se IPv6 disponivel no seu provedor; se falhar, ok — dual stack nem sempre ativo).
5. No Wireshark, filtre `icmpv6` - as Neighbor Solicitation/Advertisement substituem o ARP do IPv4 (mapeia IPv6 -> MAC).

## Verificacao — "sei que aprendi quando..."

- [ ] Escrevo um IPv6 por extenso e o encurto aplicando as 2 regras (`::` apenas uma vez)
- [ ] Identifico prefixo global vs link-local vs multicast
- [ ] Sei que o IPv6 NAO tem broadcast e o que o substitui
- [ ] Explico dual-stack em 2 frases
- [ ] Reconheço `::1` (loopback) e `fe80::` (link-local) ao ler um comando

## Conexao com o roadmap

- Virtual: toda vez que um lab mostrar `fe80::` voce ja sabe do que se trata.
- Futuro: IPv6 aparece em Seguranca (firewalls com endereco v6), CCNA (dominio IPv6).

## Para ir alem (opcional)

- Leitura: "IPv6 on wiki" (apenas secao conceitos).
- Ferramenta de consulta: `ipv6test.google.com` mostra se seu acesso ja e IPv6.
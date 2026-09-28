# Modulo 6 — Roteamento estatico, gateway e NAT

> Trilha: Redes | Mes 1, Semana 3 | Aula 6

## Objetivo

Ligar redes diferentes: o que e uma rota, como o roteador decide para onde mandar o pacote, e o que o NAT faz na borda.

## Teoria

### Por que roteamento?

Sem roteador, VLAN 10 e VLAN 20 ficam isoladas (Modulo 5). O roteador e quem faz **camada 3**: decide "para qual rede e para qual proximo salto" manda o pacote.

### Tabela de rotas

O roteador decide com base na **tabela de rotas** — pares `<rede/prefixo> -> next-hop` (proximo roteador) ou `interface` (conexao direta).

Tipos de rota:

| Tipo | Origem | Exemplo |
|------|--------|---------|
| **Conexao direta** | interface do roteador com IP | `192.168.1.0/24 via fa0/0` |
| **Estatica** | configurada manualmente | `10.0.20.0/24 via 192.168.1.2` |
| **O SPF/BGP** | protocolos de roteamento dinamico | (Modulo 10) |

### Rota estatica (quando usar)

- Redes pequenas e previsiveis, ponto-a-ponto, para rota "default" de saida.
- **Default route:** `0.0.0.0/0` (tudo que nao tem rota especifica -> sai por aqui, tipicamente para o provedor).

Comando Cisco:
```
ip route 10.0.20.0 255.255.255.0 192.168.1.2
ip route 0.0.0.0 0.0.0.0 203.0.113.1      (default route)
```

### Como o pacote "viaja" (o caminho)

1. O host ve que o destino nao e sua rede -> manda ao **gateway** (seu default route).
2. O roteador consulta a rota. Se nao tem -> **descarta + ICMP unreachable** (ou default route).
3. O roteador troca o frame (novo MAC de destino = do proximo salto) — **MAC muda, IP destino nao** (camada 2 do Modulo 4).
4. Repete ate chegar ao roteador da rede destino (que entrega no host).

### NAT (Network Address Translation) — bordo da rede

- **Para que:** permitir muitos hosts privados (RFC 1918) acessarem a Internet com poucos IPs publicos; e esconder a rede interna.
- **PAT (overload)** — o normal: varios privados saem com **o mesmo IP publico**, diferenciados pela **porta de origem**.
- **Static NAT:** 1 privado <-> 1 publico (para servidores acessiveis de fora).

Exemplo de PAT:
```
PC(192.168.1.10:50000)  -> R [NAT publico 203.0.113.5:1024] -> Internet :443
PC(192.168.1.11:55000)  -> R [NAT publico 203.0.113.5:1025] -> Internet :80
```
Do lado de fora parece tudo vindo do mesmo IP; a **tabela NAT** devolve a resposta para o host certo.

Cisco (roteador borda):
```
ip nat inside source list 1 interface GigabitEthernet0/1 overload
access-list 1 permit 192.168.0.0 0.0.0.255
interface g0/0
  ip nat inside
interface g0/1
  ip nat outside
```

## Exemplo pratico

Topologia do Modulo 5 (router-on-a-stick) + um roteador de borda. Roteador R1: interna (192.168.10.0/24 e .20.0/24) e Internet (203.0.113.0/30).

Rotas:
```
ip route 0.0.0.0 0.0.0.0 203.0.113.2     ! na borda do seu lado
```
Nos switches não há rotas (camada 2). Nos roteadores internos: rotas para redes internas + default route para a borda.

## Lab guiado (60 min)

Topologia: **2 roteadores + 2 switches + 4 hosts (como no modelo CPE/SOHO)**.

1. Monte: R1 <-> SW1 <-> (PC-A, PC-B) em 192.168.1.0/24; R2 <-> SW2 <-> (PC-C, PC-D) em 192.168.2.0/24; R1<->R2 em 10.0.0.0/30.
2. IPs nas interfaces de cada roteador.
3. **Rota estatica:**
   - Em R1: `ip route 192.168.2.0 255.255.255.0 10.0.0.2`
   - Em R2: `ip route 192.168.1.0 255.255.255.0 10.0.0.1`
   - Default route em ambos: hipotese do provedor/para fora.
4. Gateways dos PCs = IP do roteador no seu switch.
5. `show ip route` em cada roteador — veja as rotas: C (connected), S (static).
6. `ping` PC-A -> PC-C: deve passar por 2 roteadores.
7. `tracert` para o destino: veja os saltos (cada roteador = um salto).
8. (Opcional) NAT na borda: adicione um 3o roteador representando a Internet (com NAT) e teste ping externo.

## Verificacao — "sei que aprendi quando..."

- [ ] Configurei rota estatica e default route sem consulta
- [ ] Expliquei porque MAC muda e IP nao muda de ponta a ponta
- [ ] Usando `tracert`/`ping`, interpreto o caminho (saltos) num pacote
- [ ] Explico NAT vs PAT (quando usa cada um)
- [ ] Sei identificar a rota "default" na tabela `show ip route`

## Conexao com o roadmap

- Projeto 1 (topologia 2 roteadores + hosts) usa exatamente este modulo.
- NAT fica intenso na Seguranca (Mes 4): regras de firewall trabalham juntas com NAT (acesso externo a servidores).

## Para ir alem (opcional)

- Testar roteamento com 3 roteadores em anel + ver redistribuicao (nao agora; sera base do Modulo 10 OSPF/BGP).
- Ler sobre "route summarization" (resumo de rotas) — conceito CCNA avançado.
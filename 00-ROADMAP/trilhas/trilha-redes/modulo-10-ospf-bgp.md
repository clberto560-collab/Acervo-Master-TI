# Modulo 10 — Roteamento dinamico: OSPF e BGP (conceitos)

> Trilha: Redes | Mes 1, Semana 4 | Aula 10

## Objetivo

Como redes aprendem rotas sozinhas: OSPF (dentro de uma empresa/ISP) e BGP (entre ISPs — a espinha dorsal da Internet). Foco em conceito, nao em memorizacao de cada paramento.

## Teoria

### Por que dinamico?

- Milhares de redes espalhadas. Configurar rota estatica para todas e impossivel/erro propenso (Modulo 6).
- Protocolos dinamicos detectam mudancas, trocam informacoes e **convergem** para o caminho novo sozinho.

### OSPF (Open Shortest Path First)

- **IGP (Interior Gateway Protocol):** roda DENTRO de uma mesma area/AS (autonomous system).
- Baseado em **link-state**: cada roteador anuncia seus enlaces (LSAs) e todos montam o mesmo "mapa" da rede.
- Calcula o caminho com **SPF (Dijkstra)** — o melhor caminho por custo/banda.
- **Area:** redes OSPF sao divididas em areas (Area 0 = backbone). Reduz mapa e recalculo.
- **Adjacencia:** vizinhos trocam rotas via hello packets. **DR/BDR** eleito para reduzir trocas em redes broadcast.

Comportamento-chave: **converge rapido** (segundos), melhor para redes empresa/DC.

### BGP (Border Gateway Protocol)

- **EGP (Exterior Gateway Protocol):** roda ENTRE ASes (autonomous systems) — conecta ISPs, empresas grandes e a Internet inteira.
- Baseado em **path-vector**: anuncia prefixos junto com o "caminho" (sequencia de ASes).
- **Politica > forma (custo):** os operadores decidem por regras/politica estes (peerings, prepend, preferred path), nao por "custo de link".
- **eBGP:** entre ASes (vizinhança externa); **iBGP:** dentro do mesmo AS.
- Muda o roteamento da Internet com **MED/AS-path/LocalPref** (atributos).

Diferenca na pratica:

| | OSPF | BGP |
|--|------|-----|
| Escopo | dentro do AS | entre ASes |
| Algoritmo | SPF (link-state) | path-vector |
| Criterio | custo/banda | politica/atributos |
| Convergencia | segundos | minutos possivelmente |
| Uso | DC, empresa, ISP interno | Internet, ISP de borda, peering |

### Termos que voce vai ouvir (nao memorizar tudo, reconhecer)

- **AS (Autonomous System):** numero que identifica uma rede na Internet (ex.: AS15169 = Google).
- **Neighbor/Peer:** roteador vizinho configurado para trocar rotas.
- **Default route/static:** BGP distribui a default route para o interior (0.0.0.0/0).

## Exemplo pratico (laboratorio mental com 3 AS)

```
AS-1 (Empresa)          AS-2 (ISP A)          AS-3 (ISP B)
[R3] <----eBGP----> [R2] <-----eBGP-----> [R1]
       192.0.2.0/30                    198.51.100.0/30
```

- R1 <-> R2 = eBGP entre ISPs; R2 <-> R3 = interior (OSPF dentro de AS-1 ou eBGP se outra empresa).
- Se um caminho cair, o BGP/OSPF **converge** para o outro (se configurado).

## Lab guiado (50 min) — sem o roteamento "na mao"

Objetivo: ver OSPF conversando entre roteadores, sem configurar estaticas.

1. Topologia: **3 roteadores em triangulo** + 1 PC por roteador.
   R1--R2, R2--R3, R1--R3 (caminhos redundantes).
2. IPs em cada enlace: use redes /30 em cada leg (10.0.1.0/30, 10.0.2.0/30, 10.0.3.0/30).
3. **OSPF em cada router** (config global + nas interfaces):
   ```
   router ospf 1
     network 10.0.1.0 0.0.0.3 area 0
     network <rede-do-PC> 0.0.0.255 area 0
   ```
4. `show ip ospf neighbor`: veja os vizinhos formados.
5. `show ip route ospf`: veja rotas O (OSPF) aprendidas.
6. **Teste de convergencia (diversao):** desligue uma interface/coloque o cabo R1-R2 em shutdown -> espere ~10s -> o pacote PC1->PC2 deve mudar de caminho sozinho. (`tracert` antes/depois)
7. **BGP (conceito, opcional):** se quiser ver na pratica, monte 2 roteadores com `router bgp <as>` + `neighbor <ip> remote-as <as>` + `network`/`redistribute` — anuncie um prefixo e veja `show ip bgp`.

## Verificacao — "sei que aprendi quando..."

- [ ] Explico por que a rota dinamica e preferida em redes grandes vs estatica
- [ ] Descrevo o que "convergencia" significa e por que importa
- [ ] Digo a diferenca essencial OSPF (interior, custo) vs BGP (exterior, politica)
- [ ] No lab, configurei OSPF e vi vizinhos + rotas aprendidas
- [ ] Explico em 2 frases por que a Internet nao sobreviveria com rotas estáticas

## Conexao com o roadmap

- Não é foco do Projeto 1, mas e diferencial de entrevista (Analista/Eng. Redes).
- CCNA: dominios "IP connectivity" (OSPF) e "network fundamentals".
- Vai reaparecer em Redes reais e ate em seguranca (BGP hijacking — tema de cyber).

## Para ir alem (opcional)

- Around the "OSPF states" (Down, Init, Two-Way, ExStart, Exchange, Loading, Full) — reconhecer o `show ip ospf neighbor`.
- Ler um caso real de "BGP hijacking" (2018, Google) para entender o impacto — exemplo de tema premium para posts de LinkedIn.
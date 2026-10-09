# DC CORP — RPG Tecnológico

> Jogo educativo em terminal: voce e o estagiario mais novo da DC Corp e evolui de cargo fazendo missoes de TI reais em terminais simulados. Aprende o oficio **brincando** — cada capitulo ensina um pilar: VLAN, trunk, roteamento, firewall, DHCP, analise de trafego, defesa cibernetica.

## Como rodar

Modo terminal (o classico):

```
python dc_corp_jogo.py
```

Modo historia (prototipo visual com cenas e baloes de conversa + terminal com Detonado do lado):

```
python dc_corp_gui.py
```

Requer apenas **Python 3** (sem dependencias externas; o modo visual usa o tkinter que ja vem no Windows). O jogo roda 100% offline no terminal do PC (proximo passo: versao Android).

## Modo Historia (o visual)

Uma passada visual por cima do mesmo jogo:

- **Narrativa:** cada missao abre com uma cena desenhada (predios, silhuetas dos personagens) e os baloes de conversa digitando, como quadrinho. Avanca com o botao.
- **Missao:** o TERMINAL abre de um lado e o DETONADO (guia passo a passo) fica do outro, o tempo todo. Alem do guia, botões de MISSAO (objetivo), PROGRESSO (requisitos em tempo real) e DICA.
- A engine de terminal (`dc_corp_jogo.py`) e reaproveitada 100% - os comandos sao os mesmos.
- Salve o progresso normalmente: o modo visual usa o mesmo `save_dc_corp.json`.
- O clima da cena muda com o capitulo (cap.4 ganha o muro do firewall no desenho).

## O loop do jogo (RPG)

- Voce tem **cargo, XP e nivel** (de Estagiario Recem-Admitido ate O Profissional Hibrido = lenda urbana).
- A **Central de Operacoes** e o hub: iniciar capitulo, ver mapa, consultar o **DETONADO** (guia), ver perfil.
- Cada missao concluida da XP + nova missao desbloqueada; comandos corretos no terminal somam XP extra.
- **LEVEL UP** acontece no meio da missao, se voce for bem.

## Enredo

- **Supervisora Janaina Lopes** — sua mentora de infra. Manda a demanda, poe medo, da dica.
- **Sr. Valente** — CEO velho de guerra. Grosso, mas respeita quem resolve.
- **Dra. Santos** — chefe de seguranca (aparece a partir do Cap. 6).
- **Cenario:** DC Corp, empresa ficticia de 3 andares com rede antiga e instavel. O andar 15 sempre cai.

## Mapa de missoes (basico -> avancado)

| Cap | Missao | Nivel | Aprende |
|-----|--------|-------|---------|
| 1 | O Primeiro Dia (JOGAVEL) | 1 | VLAN, modos do IOS, salvar config |
| 2 | Unindo os Andares (JOGAVEL) | 2 | Trunk 802.1Q, VLANs multiplas |
| 3 | Estradas da DC Corp (JOGAVEL) | 3 | Roteamento estatico, NAT/PAT |
| 4 | O Muro da Empresa (JOGAVEL) | 4 | Firewall/ACL, contadores |
| 5 | Trunk ou Access Trocado (JOGAVEL) | 5 | Porta access vs trunk, diagnosticar layer 2 |
| 6 | A VLAN Fantasma (JOGAVEL) | 6 | Allowed vlan, VLAN nativa, remover VLAN fantasma |
| 7 | Primeiro Script (Python) (JOGAVEL) | 5 | Python do zero: print, variaveis, texto e numero |
| 8 | A Infra que se Configura Sozinha | 8 | Python+Netmiko, Ansible |
| 9 | O Defensor Final | 9 | Defesa completa (red team simulado) |

> A **progressao do jogo espelha o roadmap de estudo do acervo** — cada missao jogavel e um modulo concluido no mundo real e uma gameplay nova no jogo.

## Trilha de Aprendizado (o Acervo no jogo)

No menu da Central, opcao **5** (ou o comando `trilha` dentro do terminal, e o botao **TRILHA** no Modo Historia) mostra a **JORNADA**: todo o mapa de estudo do Acervo Master TI virou trilha de missoes, organizada por tema.

- **Tema** = um mundo, com uma **fase da empresa por tras** (o enredo explica por que se aprende aquilo ali).
- **Topico** = uma trilha de missoes. Cada topico tem **varias missoes/situacoes** (nao so uma): cada uma e um problema que acontece na DC Corp.
- **Pre-requisito = destravar**: `(primeiro: <topico>)` aparece em todo topico que exige base. A ideia e exatamente que **cada trilha puxa a outra no conhecimento**.
- Badges: **JOGAVEL** (tem terminal funcionando), **CONCLUIDA** (voce venceu), **EM BREVE** (ja esta no roadmap).
- Horas de curso viram **XP de meta** (1h = 100 XP), pra "estudei no mundo real" bater com "subi no jogo".

As fases (ordem da empresa, tal qual a Jornada):

1. **Redes** - o estagiario ressuscita a rede velha dos andares (o que ja jogamos).
2. **Cabeamento** - crescer exige casa arrumada: par metalico certificado, depois fibra. Ninguem monta Mikrotik em cabo solto.
3. **Mikrotik** - com a infra pronta, chega o roteador de borda que o Valente comprou.
4. **Ubiquiti** - Wi-Fi pra firma inteira, em cima da fibra ja certificada.
5. **Huawei** - o contrato grande exige padrao enterprise: a DC Corp vira provedora.
6. **Zabbix** - tudo no ar, agora ninguem dorme: monitoramento 24h.
7. **DataCenter** - o desfecho: consolidar a DC Corp num data center de verdade.
8. **Programacao** - transversal: Python ensina a infra a se configurar sozinha.

> Ex.: o topico *Switches Ethernet - Parte I* ja e jogavel (missoes 1-2: VLAN + trunk; missoes 5-6: access/trunk trocado e VLAN fantasma) e *Python do Zero* acaba de ganhar a primeira situacao jogavel (cap. 7).

## O Detonado

Dentro do jogo, opcao **3** mostra o guia passo a passo de cada missao (quem passa, cenario, objetivo, o que aprende, recompensa e os passos exatos). Tambem da pra acessar por capitulo: `detonado 2`.

## Gameplay atual (Capitulos 1 ao 7)

Terminal Cisco simulado com comandos reais (engine generica, reutilizavel nas proximas missoes):

- `enable` (modo privilegiado)
- `configure terminal` (modo config)
- `vlan <n>` / `name <nome>` / `no vlan <n>` (remove uma VLAN - caça a fantasma)
- `interface fa0/24` (modo interface, switch) e `interface fa0/0`/`fa0/1` (roteador)
- `switchport mode trunk` / `switchport mode access` / `switchport access vlan <n>`
- `switchport trunk allowed vlan 10,20` / `switchport trunk native vlan <n>`
- `ip address <ip> <mascara>` / `no shutdown`
- `ip route <rede> <mascara> <next-hop>` (rota estatica / default route)
- `access-list <n> permit <rede> <wildcard>` + `ip nat inside source list <n> interface <if> overload`
- `access-list <n> deny|permit ip <src> <wildcard> <dst> <wildcard>` (ACL extended)
- `ip access-group <n> in|out` (aplicar ACL na interface)
- `show vlan brief` / `show running-config` / `show interfaces trunk` / `show ip route` / `show ip nat translations` / `show access-lists`
- `write memory` (salvar)
- `conectar <host>` (trocar equipamento) — `show switches` lista os hosts
- `help` / `dica` / `missao` / `progresso` / `detonado`
- `ping 8.8.8.8` (prova da missao 3: diagnostica LAN -> rota -> NAT)

**Capitulo 7 abre o terminal Python (>>>)** — o estagiario comeca a automatizar. Interpretador didatico (seguro, sem exec de codigo arbitrario) que por enquanto ensina a base:

- `print("texto")` — mostra algo na tela (texto entre aspas)
- `variavel = valor` — guarda um valor: `empresa = "DC Corp"` (texto) ou `andar = 15` (numero)
- `print(empresa)` — imprime o valor guardado
- `# comentario` — nao faz nada
- `progresso` mostra as metas da aula (print de boas-vindas, variavel empresa, imprimir a empresa, andar 15)
- `simular trafego` (prova das missoes 4, 5 e 6: testa ACL / access x trunk / trunk e fantasma)

**Capitulo 1** (O Primeiro Dia): recriar a VLAN 10 (TI) nos dois switches e salvar.
**Capitulo 2** (Unindo os Andares): criar a VLAN 20 (RH) nos dois switches, configurar a
porta `fa0/24` como trunk 802.1Q e liberar **apenas** as VLANs 10 e 20 no trunk.
**Capitulo 3** (Estradas da DC Corp): configurar o roteador RT-01 — LAN (`fa0/0`,
192.168.10.1/24), WAN (`fa0/1`, 200.100.50.2/30), rota padrao para o provedor, NAT
overload (ACL 1 + inside/outside) — e provar com `ping 8.8.8.8` (4/4).
**Capitulo 4** (O Muro da Empresa): trancar o RH na Diretoria. No RT-01, criar a ACL 100
negando `192.168.20.0 -> 192.168.10.0` **antes** do `permit ip any any` generico, aplicar
`ip access-group 100 in` na `fa0/1` (lado do RH), salvar e provar com `simular trafego`
(RH bloqueado + TI livre) — a ordem das regras manda: a primeira que bate vale.

> Regra de ouro logo no comeco: trunk aberto (`vlan any any`) vai escoar todas as
> VLANs pelo cabo — porta aberta pra ladrao. Sempre limitar com
> `switchport trunk allowed vlan`.
>
> E no roteador: IP privado chegando na borda sem NAT morre ali. Nenhum IP interno
> ultrapassa o `inside` sem virar o IP publico no `outside`.
>
> E no firewall: ACL e avaliada de cima pra baixo — regra especifica que nega vem
> ANTES da regra generica que permite. O contador do `show access-lists` prova
> (ou flagra) quem bateu em qual regra.

## Save automatico

Seu progresso (XP, cargo, missoes concluidas) fica salvo em `save_dc_corp.json`
(ignorado pelo git). Feche o jogo e volte depois: o jogo continua de onde parou.

## Proximos passos (curto prazo)

1. **Missao 5 jogavel** (DHCP/DNS como servidor)
2. **Evolucao do Modo Historia** (artes finais dos personagens, animacoes de transicao, som)
3. **Salto para Godot** (versao Android offline com o mesmo conteudo)

## Teste automatizado

```
python -m py_compile dc_corp_jogo.py
```
Fluxo de teste completo via arquivo de entrada redirecionado (ver CI do projeto).
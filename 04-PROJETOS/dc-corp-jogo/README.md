# DC CORP — RPG Tecnológico

> Jogo educativo em terminal: voce e o estagiario mais novo da DC Corp e evolui de cargo fazendo missoes de TI reais em terminais simulados. Aprende o oficio **brincando** — cada capitulo ensina um pilar: VLAN, trunk, roteamento, firewall, DHCP, analise de trafego, defesa cibernetica.

## Como rodar

```
python dc_corp_jogo.py
```

Requer apenas **Python 3** (sem dependencias externas). O jogo roda 100% offline no terminal do PC (proximo passo: versao Android).

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
| 4 | O Muro da Empresa | 4 | Firewall/ACL, contadores |
| 5 | O Carteiro Digital | 5 | DHCP, DNS |
| 6 | Espionando o Trafego | 6 | Wireshark, nmap |
| 7 | Visao de Coruja | 7 | Wazuh/SIEM, resposta |
| 8 | A Infra que se Configura Sozinha | 8 | Python+Netmiko, Ansible |
| 9 | O Defensor Final | 9 | Defesa completa (red team simulado) |

> A **progressao do jogo espelha o roadmap de estudo do acervo** — cada missao jogavel e um modulo concluido no mundo real e uma gameplay nova no jogo.

## O Detonado

Dentro do jogo, opcao **3** mostra o guia passo a passo de cada missao (quem passa, cenario, objetivo, o que aprende, recompensa e os passos exatos). Tambem da pra acessar por capitulo: `detonado 2`.

## Gameplay atual (Capitulos 1, 2 e 3)

Terminal Cisco simulado com comandos reais (engine generica, reutilizavel nas proximas missoes):

- `enable` (modo privilegiado)
- `configure terminal` (modo config)
- `vlan <n>` / `name <nome>`
- `interface fa0/24` (modo interface, switch) e `interface fa0/0`/`fa0/1` (roteador)
- `switchport mode trunk` / `switchport trunk allowed vlan 10,20`
- `ip address <ip> <mascara>` / `no shutdown`
- `ip route <rede> <mascara> <next-hop>` (rota estatica / default route)
- `access-list <n> permit <rede> <wildcard>` + `ip nat inside source list <n> interface <if> overload`
- `show vlan brief` / `show running-config` / `show interfaces trunk` / `show ip route` / `show ip nat translations`
- `write memory` (salvar)
- `conectar <host>` (trocar equipamento) — `show switches` lista os hosts
- `help` / `dica` / `missao` / `progresso` / `detonado`
- `ping 8.8.8.8` (prova da missao 3: diagnostica LAN -> rota -> NAT)

**Capitulo 1** (O Primeiro Dia): recriar a VLAN 10 (TI) nos dois switches e salvar.
**Capitulo 2** (Unindo os Andares): criar a VLAN 20 (RH) nos dois switches, configurar a
porta `fa0/24` como trunk 802.1Q e liberar **apenas** as VLANs 10 e 20 no trunk.
**Capitulo 3** (Estradas da DC Corp): configurar o roteador RT-01 — LAN (`fa0/0`,
192.168.10.1/24), WAN (`fa0/1`, 200.100.50.2/30), rota padrao para o provedor, NAT
overload (ACL 1 + inside/outside) — e provar com `ping 8.8.8.8` (4/4).

> Regra de ouro logo no comeco: trunk aberto (`vlan any any`) vai escoar todas as
> VLANs pelo cabo — porta aberta pra ladrao. Sempre limitar com
> `switchport trunk allowed vlan`.
>
> E no roteador: IP privado chegando na borda sem NAT morre ali. Nenhum IP interno
> ultrapassa o `inside` sem virar o IP publico no `outside`.

## Save automatico

Seu progresso (XP, cargo, missoes concluidas) fica salvo em `save_dc_corp.json`
(ignorado pelo git). Feche o jogo e volte depois: o jogo continua de onde parou.

## Proximos passos (curto prazo)

1. **Missao 4 jogavel** (firewall: ordem de regras e contadores)
2. **Missao 5 jogavel** (DHCP/DNS como servidor)
3. **Salto para Godot** (versao Android offline com o mesmo conteudo)

## Teste automatizado

```
python -m py_compile dc_corp_jogo.py
```
Fluxo de teste completo via arquivo de entrada redirecionado (ver CI do projeto).
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
| 2 | Unindo os Andares | 2 | Trunk 802.1Q, VLANs multiplas |
| 3 | Estradas da DC Corp | 3 | Roteamento estatico, NAT |
| 4 | O Muro da Empresa | 4 | Firewall/ACL, contadores |
| 5 | O Carteiro Digital | 5 | DHCP, DNS |
| 6 | Espionando o Trafego | 6 | Wireshark, nmap |
| 7 | Visao de Coruja | 7 | Wazuh/SIEM, resposta |
| 8 | A Infra que se Configura Sozinha | 8 | Python+Netmiko, Ansible |
| 9 | O Defensor Final | 9 | Defesa completa (red team simulado) |

> A **progressao do jogo espelha o roadmap de estudo do acervo** — cada missao jogavel e um modulo concluido no mundo real e uma gameplay nova no jogo.

## O Detonado

Dentro do jogo, opcao **3** mostra o guia passo a passo de cada missao (quem passa, cenario, objetivo, o que aprende, recompensa e os passos exatos). Tambem da pra acessar por capitulo: `detonado 2`.

## Gameplay atual (Capitulo 1)

Terminal Cisco simulado com comandos reais:

- `enable` (modo privilegiado)
- `configure terminal` (modo config)
- `vlan 10` / `name TI`
- `show vlan brief` / `show running-config`
- `write memory` (salvar)
- `conectar SW-01` / `SW-02` (trocar equipamento)
- `help` / `dica` / `detonado`

## Proximos passos (curto prazo)

1. **Missao 2 jogavel** (trunk 802.1Q entre SW-01/SW-02 com teste de comunicacao)
2. **Persistencia de save** (seu cargo/XP ficam salvos entre sessoes)
3. **Salto para Godot** (versao Android offline com o mesmo conteudo)

## Teste automatizado

```
python -m py_compile dc_corp_jogo.py
```
Fluxo de teste completo via arquivo de entrada redirecionado (ver CI do projeto).
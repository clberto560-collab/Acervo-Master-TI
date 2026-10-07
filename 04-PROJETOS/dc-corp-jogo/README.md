# DC Corp — Dia 1: Restaure a Rede do Andar 15

> Prototipo jogavel (MVP) do jogo educativo de TI. Voce e o novo tecnico e aprende **CLI Cisco real** praticando numa missao, em vez de assistir teoria.

## O jogo em 30 segundos

A rede do andar 15 caiu: as VLANs sumiram das configs dos switches. Voce conecta no terminal de cada switch (**SW-01** e **SW-02**) e usa comandos reais de Cisco IOS para restaurar a VLAN 10 (TI) e salvar a configuracao. O jogo valida cada comando, da XP, e o Sr. Valente (seu gerente) avalia sua atuacao.

## Como rodar

```
pip (nada alem do Python 3 nativo)
python dc_corp_jogo.py
```

Requer apenas Python 3 (sem dependencias externas).

## Comandos suportados (ate agora)

| Comando | Modo | Faz |
|---------|------|-----|
| `help` | todos | lista os comandos do contexto |
| `enable` | user (`>`) | entra no modo privilegiado (`#`) |
| `configure terminal` | priv (`#`) | entra em configuracao (`(config)#`) |
| `vlan 10` | config | cria e entrara a VLAN |
| `name TI` | dentro da vlan | nomeia a VLAN |
| `show vlan brief` | qualquer | tabela de VLANs |
| `show running-config` | qualquer | configuracao atual |
| `write memory` | privilegiado/config | salva a configuracao |
| `conectar SW-01` / `SW-02` | qualquer | troca de equipamento |
| `end` / `exit` | config/vlan | volta de nivel |
| `missao` / `dica` | todos | objetivo e pista |

## Objetivo da missao

Em **cada** switch:
1. `vlan 10` (criar a VLAN)
2. `name TI` (nomear)
3. `write memory` (salvar)

## Design (visao de futuro)

Cada missao seguinte = um modulo do roadmap de estudo:

- **Missao 2:** VLAN entre 2 switches com trunk (802.1Q)
- **Missao 3:** Roteamento estatico + NAT
- **Missao 4:** ACL bloqueando a VLAN do RH
- **Missao 5:** DHCP na rede da DC Corp
- **Depois:** pfSense, Zabbix, Wireshark/nmap, defesa cibernetica

Tecnologia alvo: Godot (Python-like) para **Android offline**. Este prototipo em terminal Python serve para validar a **pegada** (jogador digita comando real -> game valida -> XP) antes de investir no jogo completo.

## Liocoes de construcao (aprendi fazendo)

- A logica de ensino esta em **proibir o atalho**: o jogador precisa aprender a navegar os modos do IOS.
- Mensagens de erro estilo Cisco ensinam mais que "Comando invalido".
- Requisitar `write memory` treina o habito profissional (config nao salva = mistake classico).

## Rodando o teste automatizado

```
python -m py_compile dc_corp_jogo.py
```
(ou fazer jogada completa com arquivo de entrada redirecionado)
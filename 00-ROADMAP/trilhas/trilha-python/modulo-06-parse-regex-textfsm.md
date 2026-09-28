# Modulo 6 — Parse de saida: regex e texto estruturado (TextFSM)

> Trilha: Python | Mes 2, Semana 3 | Aula 6

## Objetivo

Transformar saidas de `show` (texto) em **dados utilizaveis** (dicts/listas). Sem isso, voce fica colando texto; com isso, voce gera relatorios e logs automaticos.

## Teoria

### O problema

`show ip interface brief` retorna texto:
```
Interface              IP-Address      OK? Method Status    Protocol
GigabitEthernet0/0     192.168.1.1     YES manual up        up
GigabitEthernet0/1     unassigned      YES manual administratively down down
Vlan1                  10.0.0.254      YES manual up        up
```
Precisamos extrair: quais interfaces tem IP e qual o status — como dados (ex.: dict), nao como texto.

### Regex basica (o que precisamos)

```python
import re

texto = "GigabitEthernet0/0     192.168.1.1     YES manual up        up"
# procurar um IP v4
ip = re.search(r"\d+\.\d+\.\d+\.\d+", texto)
print(ip.group())   # 192.168.1.1
```

A regex mais usada em redes: `(\d{1,3}\.){3}\d{1,3}` (IPv4). (Existe o padrao completo batante mais longo, mas esse é o suficiente em 90% dos casos.)

### TextFSM + netmiko (`use_textfsm`)

A melhor pratica: deixar a biblioteca parsear a tabela. O Netmiko tem **templates TextFSM** prontos para os comandos mais comuns. Quando ativo, retorna uma lista de dicts.

```python
from netmiko import ConnectHandler

c = ConnectHandler(device_type="cisco_ios", host="192.168.1.1", username="admin", password="sua_senha")
dados = c.send_command("show ip interface brief", use_textfsm=True)
print(dados)
# [{'interface': 'GigabitEthernet0/0', 'ip_address': '192.168.1.1', 'status': 'up', 'protocol': 'up'}, ...]

# Filtrar
up = [d for d in dados if d["status"] == "up" and d["protocol"] == "up"]
print(f"Interfaces up: {len(up)}")

# IPs configurados
ips = [d["ip_address"] for d in dados if d["ip_address"] != "unassigned"]
```

### Pra que isso serve na pratica

- **Relatorio diario:** rodar `show ip interface brief` em 10 roteadores e gerar lista de quem tem interface down.
- **Inventario automatizado:** extrair hostname/OS/IP e gravar num CSV/JSON (Aula 2).
- **Verificacao de config:** checar se a VLAN X existe na config antes/pos aplicacao.

## Exemplo pratico (relatorio de interfaces down)

```python
from netmiko import ConnectHandler

dispositivos = ["192.168.1.1", "192.168.1.2"]

def interfaces_down(ip):
    c = ConnectHandler(device_type="cisco_ios", host=ip, username="admin", password="sua_senha")
    dados = c.send_command("show ip interface brief", use_textfsm=True)
    down = [d["interface"] for d in dados if d["protocol"].lower() != "up"]
    c.disconnect()
    return ip, down

for ip in dispositivos:
    ip, down = interfaces_down(ip)
    print(f"{ip}: interfaces fora do ar -> {down if down else 'nenhuma'}")
```

## Lab guiado (40 min)

1. Conecte no roteador do lab e rode `show ip interface brief` com `use_textfsm=True`.
2. Imprima o resultado estruturado (lista de dicts) — veja que agora as colunas sao chaves.
3. Escreva o codigo do "exemplo pratico" (lista de interfaces down) para 2 roteadores.
4. (Regex) extraia o IP de uma saida aleatoria com `re.search` e confira.
5. (Avançado) rode `show version | include uptime` e depois `use_textfsm=True`; compare DENTRO vs FORA.

## Verificacao — "sei que aprendi quando..."

- [ ] Uso `use_textfsm=True` e recebo dicts (nao texto) de um `show`
- [ ] Escrevo uma regex basica para extrair IPv4 com `re.search`
- [ ] Gero um relatorio (ex.: interfaces down) a partir de dados estruturados
- [ ] Differencio dado estruturado vs texto e por que isso importa no operacional

## Conexao com o roadmap

- Vocẽ vai precisar disso para: verificar resultados de config aplicada (Projeto 2) e inventario (Mes 5/6).
- No Projeto de seguranca (Mes 4), parsear `show access-lists` ou contadores com TextFSM e poderoso.

## Para ir alem (opcional)

- Ver os templates padroes do NAPALM/pyATS (cisco) — FAQ em rodagem automatica de conformidade.
- Testar `send_command(..., command_string="show version", use_genie=True)` (Genie, se disponivel no device).
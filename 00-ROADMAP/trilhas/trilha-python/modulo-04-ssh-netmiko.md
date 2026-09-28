# Modulo 4 — Conexao SSH com Netmiko e Paramiko

> Trilha: Python | Mes 2, Semana 2 | Aula 4

## Objetivo

Conectar de verdade num equipamento via SSH e executar comandos `show` a partir do Python. E o momento em que o Mes 1 (CLI Cisco) encontra o Mes 2 (automacao).

## Teoria

### O que voce vai usar

- **Paramiko:** biblioteca SSH de baixo nivel (nao conhece rede; so SSH).
- **Netmiko:** construida em cima do Paramiko, **especializada em equipamentos de rede** — conhece modos do IOS, espera prompts, executa `enable`, `config t`, etc.

Simples: **use Netmiko**. Paramiko voce conhece (e util quando precisar de baixo nivel/fora da rede), mas o dia a dia de automacao de rede e Netmiko.

### Instalacao

```
pip install netmiko
```

(Paramiko vem junto como dependencia. Se precisar isolado: `pip install paramiko`.)

### Conceitos do Netmiko

- **ConnectHandler** cria a conexao. Preciso de um dict com credenciais + `device_type`.
- **`device_type`:** `cisco_ios` (roteador/switch IOS), `cisco_xe`, `cisco_nxos`, `mikrotik_routeros`, `juniper_junos`, etc.
- **Metodos que voce vai usar:**
  - `send_command("show ...")` — executa comando de EXEC/`show`
  - `send_config_set([...])` — envia lista de comandos em modo configuracao
  - `enable()` — entra no modo privilegiado (se lo necesasario)
  - `disconnect()` — fecha conexao (sempre!)

### Exemplo minimo (que executa)

```python
from netmiko import ConnectHandler

dispositivo = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "sua_senha_forte",   # NAO deixe hardcoded em producao (Modulo 5)
}

conexao = ConnectHandler(**dispositivo)
saida = conexao.send_command("show ip interface brief")
print(saida)
conexao.disconnect()
```

> Obs.: em muitos labs voce vai usar um roteador ethanulado no GNS3/EVE-NG com SSH habilitado. Sem isso o lab nao funciona — config veja Modulo 9 da trilha Redes.

## Exemplo pratico (mostrar o prompt)

```python
from netmiko import ConnectHandler

r1 = ConnectHandler(
    device_type="cisco_ios",
    host="192.168.1.1",
    username="admin",
    password="sua_senha",
)

print(r1.find_prompt())          # ex.: "R1#"
print(r1.send_command("show running-config | include hostname"))
r1.disconnect()
```

Saida esperada:
```
R1#
hostname R1
```

## Lab guiado (60 min) — primeira automacao de verdade

Requisito: ter um roteador/switch no GNS3/Packet Tracer com **SSH habilitado** (Modulo 9 da trilha Redes).

1. Instale: `pip install netmiko`
2. Num roteador do lab, confirme SSH: `show ip ssh`, `line vty 0 4 transport input ssh`.
3. Teste o exemplo "minimo" acima com o IP/credenciais do lab.
   - Se der `Authentication failed`: revise usuario/senha (e que o device_type confere com o OS do equipamento).
   - Se der `Timeout`: confirme ping do PC -> IP do equipamento e porta 22 aberta.
4. Rode `send_command` para: `show ip interface brief`, `show version | include IOS`.
5. Faça `enable()` (se o equipamento exigir) e rode `show running-config | include vlan`.
6. (Validação de retorno) imprima um `show` e cole a saida num arquivo `.txt` em `03-SCRIPTS/python` (primeiro backup manual automatizado!).

## Verificacao — "sei que aprendi quando..."

- [ ] Instalei e importei netmiko sem erro
- [ ] Conectei num equipamento real/emulado via SSH e li o prompt
- [ ] Executei um `show` e capturei o retorno numa variavel
- [ ] Chamei `disconnect()` no final e sei por que eh importante
- [ ] Diagnostico os 3 erros classicos: auth fail, timeout, device_type errado

## Conexao com o roadmap

- Este é o "click" que abre Mes 2: loop de dispositivos (Aula 5), backup com arquivos (Aula 6/7).
- Projeto 2 = voce conecta em 3+ dispositivos (ou inventario) e salva config — tudo desta aula.

## Para ir alem (opcional)

- Ver na doc oficial do Netmiko os `device_type` suportados (`show` em `netmiko.ssh_dispatcher`).
- Dica de seguranca: nunca coloque senha em texto puro — no proximo modulo tratamos isso como padrao.
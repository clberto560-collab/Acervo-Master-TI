# Modulo 8 — Python para Redes: Push de configuracoes (VLAN, ACL) com validacao

> Trilha: Python | Mes 2, Semana 4 | Aula 8

## Objetivo

Nao so baixar config (Aula 7) mas **aplicar configuracao** em lote — criar VLANs, aplicar ACL, configurar porta — com validacao de que "pegou".

## Teoria

### Diferença: send_command vs send_config_set

- `send_command("show ...")`: modo EXEC (somente leitura).
- `send_config_set([...])`: entra em modo configuracao, envia comandos, sai. **E a forma de aplicar config.**

### Aplicando config (com template)

```python
from netmiko import ConnectHandler

conexao = ConnectHandler(device_type="cisco_ios", host="192.168.1.1", username="admin", password="sua_senha")

comandos = [
    "vlan 40",
    "name DEP_Legal",
]
saida = conexao.send_config_set(comandos)
print(saida)

# Alternativa: passar como string multilinha
comandos_txt = """
vlan 50
 name DEP_Fiscal
"""
conexao.send_config_set(comandos_txt.splitlines())
conexao.disconnect()
```

### Validacao (o que a automacao decente faz)

Nao basta "rodou sem erro" — é preciso **provar** que a mudanca aplicou:

```python
# depois de criar a vlan 40
verif = conexao.send_command("show vlan brief")
if "40" in verif:
    print("VLAN 40 presente na tabela")
else:
    print("FALHA: vlan 40 nao apareceu")
```

Padrao recomendado: **ACAO -> VERIFICACAO -> RELATO**. (Em Ansible, Mes 6, isso vira `changed_when`/`assert` — mesma ideia.)

### Aplicar ACL (regra) via config

```python
regras = [
    "ip access-list extended BLOQUEAR_RH",
    "deny ip 10.0.20.0 0.0.0.255 10.0.10.0 0.0.0.255",
    "permit ip any any",
]
conexao.send_config_set(regras)
# validar
acl = conexao.send_command("show access-lists BLOQUEAR_RH")
print(acl)
```

(Detalhe de ACL cisco: mascara "wildcard" = inverso da mascara normal. 255.255.255.0 -> 0.0.0.255.)

## Exemplo pratico (push VLAN em 3 switches, com validacao)

```python
import logging
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

VLAN = ["vlan 60", "name AUTOMACAO"]
IPs = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

for ip in IPs:
    try:
        c = ConnectHandler(device_type="cisco_ios", host=ip, username="admin", password="sua_senha")
        c.send_config_set(VLAN)
        tabela = c.send_command("show vlan brief")
        c.disconnect()
        if "60" in tabela:
            logging.info(f"{ip}: VLAN 60 criada e confirmada")
        else:
            logging.warning(f"{ip}: VLAN 60 NAO confirmada (revisar)")
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as erro:
        logging.error(f"{ip}: {erro}")
```

## Lab guiado (50 min)

1. Rode o exemplo acima num lab com 3 switches (ou 3 roteadores com `vlan` se suportado).
2. De ao menos 1 IP do lote um switch FISICAMENTE desligado (para voltar a falha).
3. Valide o resultado: `show vlan brief` em cada equipamento confirma `AUTOMACAO`?
4. Adicione ACL: bloqueie o trafego `10.0.20.0/24 -> 10.0.10.0/24`, aplique em interface de entrada e VALIDE com `show access-lists` + um `show interface | include packets denied` (contadores!).
5. (Desafio) transforme em playbook final classificado como projeto/experimenta no repo `04-PROJETOS/projeto-02b-push-configs/`.

## Verificacao — "sei que aprendi quando..."

- [ ] Uso send_config_set para aplicar config (nao mais `send_command` copiando comando)
- [ ] Apos aplicar, rodo comando de verificacao e confirmo no log
- [ ] Reconheço a mascara wildcard (`0.0.0.255`) e sei quando usar ACL
- [ ] Sei que "rodou sem erro" != "aplicou" (diferenca que empresas exigem)
- [ ] Tenho 1 push de config (ex.: VLAN ou ACL) funcionando com validacao

## Conexao com o roadmap

- Push de config e exigido no Projeto 2/4 (criar VLANs em N switches, aplicar firewall/ACL).
- Prepara o terreno para Ansible (Mes 6), que faz o mesmo conceito para servidores.

## Para ir alem (opcional)

- Aplicar via NAPALM (API mais alto nivel) para comparar abordagens (network driver padronizado).
- Experimentar `fast_cli=True` para equipamentos modernos (velocidade) e `read_timeout` em configs grandes.
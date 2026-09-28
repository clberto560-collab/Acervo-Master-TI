# Modulo 5 — Python para Redes: Dispositivos em lote (arquivo + loop)

> Trilha: Python | Mes 2, Semana 3 | Aula 5

## Objetivo

Passar de "1 dispositivo" para "N dispositivos": ler IPs de um arquivo, conectar em cada um, tratar falhas e obter um relatório. Essa é a diferença entre script de laboratório e automacao util.

## Teoria

### O padrao: arquivo + loop + try/except

Juntando Aula 2 (arquivos), Aula 3 (erros/logging) e Aula 4 (netmiko):

```python
import logging
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

CREDENCIAIS = {"username": "admin", "password": "sua_senha"}

def ler_ips(caminho):
    with open(caminho) as f:
        return [linha.strip() for linha in f if linha.strip()]

def backup_config(ip):
    conexao = ConnectHandler(device_type="cisco_ios", host=ip, **CREDENCIAIS)
    config = conexao.send_command("show running-config")
    with open(f"backup_{ip}.txt", "w") as f:
        f.write(config)
    conexao.disconnect()
    logging.info(f"Backup de {ip} salvo")

ips = ler_ips("dispositivos.txt")
for ip in ips:
    try:
        backup_config(ip)
    except NetmikoTimeoutException:
        logging.error(f"{ip} - timeout (host/porta SSH fechada)")
    except NetmikoAuthenticationException:
        logging.error(f"{ip} - autenticacao falhou")
```

### Boas praticas ja desde agora

- **Credenciais fora do codigo:** env var (`os.environ`) ou arquivo `.env` (nunca no script). Ex.:
  ```python
  import os
  CREDENCIAIS = {"username": os.environ["NET_USER"], "password": os.environ["NET_PASS"]}
  ```
- **Mensagens claras de erro:** nada de `except Exception: pass` silencioso.
- **Saida deterministica:** se gravar arquivos, nomeie com IP/date.
- **`send_command` com `use_textfsm`** (Aula 6): para extrair dados estruturados em vez de texto solto.

## Exemplo pratico (conte a historia no log)

Adapte o codigo acima: use `logging.INFO` por dispositivo OK e `logging.ERROR` quando falhar. Rode contra 3 roteadores no GNS3, um deles com IP inexistente. Saida parecida:

```
INFO - Backup de 192.168.1.1 salvo
INFO - Backup de 192.168.1.2 salvo
ERROR - 192.168.1.99 - timeout (host/porta SSH fechada)
```

O script termina normal (exit 0) mesmo com falhas — e o relatorio fica no log.

## Lab guiado (50 min)

1. Crie `dispositivos.txt` com os IPs de 3 roteadores do lab (deixe um deles errado para provocar erro).
2. Escreva o script do padrao acima (adaptando credenciais para o seu lab).
3. Rode: todos os backup_IP.txt criados? Log com INFO/ERROR correto?
4. Confira que os arquivos `.txt` contem a config completa do equipamento.
5. Adicione `finally` que aguarde 1s entre dispositivos (`import time; time.sleep(1)`) — evita sobrecarregar o equipamento.
6. (Desafio) suporte a dispositivos com `device_type` diferente por IP: leia o tipo de um CSV em vez de fixar `cisco_ios`.

## Verificacao — "sei que aprendi quando..."

- [ ] Meu script processa N dispositivos e NAO morre no primeiro erro
- [ ] Leio IPs de um arquivo, sem hardcode
- [ ] Registro no log o destino de cada acao (OK / erro especifico)
- [ ] Sei quando usar Timeout vs Auth exception vs catch generico
- [ ] Credenciais nao aparecem no codigo nem no git (env / sem commit)

## Conexao com o roadmap

- **Fim do Mes 2 -> Projeto 2:** "Script Python conecta em 3 roteadores e salva config de cada um".
- Esse e exatamente o codigo do exemplo — adaptar contexto real e publicar no GitHub.

## Para ir alem (opcional)

- Ler sobre `dotenv` (`pip install python-dotenv`) para carregar `.env` com credenciais.
- Pensar: como faria o script rodar "periodicamente" (agendando com cron, tema Mes 3/Linux).
# Modulo 3 — Python para Redes: Erros, try/except e logging

> Trilha: Python | Mes 2, Semana 2 | Aula 3

## Objetivo

Escrever scripts que nao "quebram" silenciosamente quando um dispositivo falha: capturar erros com try/except e registrar o que aconteceu com logging.

## Teoria

### Por que erros acontecem em script de rede

- Host desligado (timeout), porta fechada, senha errada, equipamento sem SSH habilitado, rede bloqueando porta 22.
- Um script que **para no primeiro erro** e inutil em producao. Tratar erro e obrigatorio.

### try / except (o "se der errado")

```python
try:
    conexao = ssh_conectar("192.168.1.99")     # dispositivo inexistente
    print("Conectado")
except Exception as erro:
    print(f"Nao foi possivel conectar: {erro}")
```

- `try`: tenta o codigo.
- `except Exception as erro`: captura qualquer erro, nomeia e continua.
- Excecoes especificas são melhores que pegar tudo (`except` generico esconde bugs). Para redes, ex.: `socket.timeout`, `netmiko.NetmikoTimeoutException`.

### finally e else

```python
try:
    conexao = ssh(x)
except TimeoutError:
    registrar("timeout")
else:
    salvar_backup(conexao)      # rodou sem erro
finally:
    fechar_arquivo()             # SEMPRE roda
```

### Logging (o diario do script)

Melhor que `print` para scripts serios: com timestamps, niveis e saida configurável.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename="automacao.log",          # grava em arquivo (opcional)
)
logging.info("Iniciando backup de 3 dispositivos")
logging.warning("SW2 nao respondeu em 30s")
logging.error("Falha irreversivel na conexao")
```

Niveis: DEBUG < INFO < WARNING < ERROR < CRITICAL. Configure `level=` para o que voce quer ver (INFO = geral, DEBUG = detalhes de conexao).

## Exemplo pratico (o padrao que voce vai repetir)

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

dispositivos = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

def conectar(ip):
    # simulacao: o ".2" "cai"
    if ip.endswith(".2"):
        raise TimeoutError(f"{ip} sem resposta")
    return f"conexao-{ip}"

for ip in dispositivos:
    try:
        conexao = conectar(ip)
        logging.info(f"OK: {ip} conectado")
    except TimeoutError as erro:
        logging.warning(str(erro))
```

Saida:
```
INFO - OK: 192.168.1.1 conectado
WARNING - 192.168.1.2 sem resposta
INFO - OK: 192.168.1.3 conectado
```
O script nao parou no erro — a logica de negocio (backup) continua para os demais.

## Lab guiado (30 min)

1. Escreva a funcao `conectar(ip)` que "falha" quando o ultimo octeto for par (simule timeout).
2. Num loop de 4 IPs, use try/except: registre WARNING nos que falham e INFO nos que passam.
3. Grave o log num arquivo `automacao.log` e abra para conferir timestamps.
4. Adicione `finally` que imprime `"--- fim da tentativa para <ip> ---"` (roda para todos).
5. (Desafio) use `except` especifico duas vezes (TimeoutError e outra) e imprima mensagens diferentes.

## Verificacao — "sei que aprendi quando..."

- [ ] Expliquei por que `except Exception` generico pode mascarar erros de codigo
- [ ] Uso try/except + finally para garantir execucao e registro
- [ ] Config loglevel, melhorei e escrevi mensagens em arquivo
- [ ] Sei a diferenca entre print e logging para scripts de producao
- [ ] Tratei timeout de 1 dispositivo num lote sem derrubar o script

## Conexao com o roadmap

- O padrao try/except + logging e usado em **Todos os scripts** do Mes 2 (backup, push de config).
- Na automacao real (Ansible), a mesma filosofia vira "retries" e relatorios.

## Para ir alem (opcional)

- Ler sobre "exception hierarchy" do Python (a familia de erros: IOError, ValueError, TimeoutError).
- Avançar: criar Exceptions proprias (`class FalhaDeRede(Exception)`) para erros de dominio.
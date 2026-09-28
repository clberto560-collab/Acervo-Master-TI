# Modulo 1 — Python para Redes: Sintaxe base

> Trilha: Python | Mes 2, Semana 1 | Aula 1

## Objetivo

Ter a base de Python suficiente para o caminho de redes: variaveis, tipos, condicionais, loops e funcoes. Nao é um curso de "todas as features" — e o minimo indispensavel para usar Netmiko nos proximos modulos.

## Teoria

### Variaveis e tipos (o essencial)

```python
nome = "ER-01"          # string  (texto)
porta = 22               # int     (numero inteiro)
latencia = 0.5           # float   (fracao)
ativo = True             # bool    (True/False)
```

- Python define o tipo automaticamente. `type(variavel)` mostra o tipo.
- Nomes: `snake_case` (`ip_do_gateway`), sem espacos, sem caracter especial.

### Condicional

```python
if resposta == "reachable":
    print("O host respondeu")
elif resposta == "timeout":
    print("Sem resposta")
else:
    print("Resultado desconhecido")
```

### Loops

```python
# for: iterar sobre uma lista
dispositivos = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
for ip in dispositivos:
    print("Conectando em", ip)

# range
for i in range(1, 4):
    print("Execucao numero", i)

# while: repete enquanto a condicao for verdadeira
tentativas = 0
while tentativas < 3:
    print("Tentando...")
    tentativas += 1
```

### Listas e dicionarios (os dois que voce vai usar MUITO)

```python
# Lista: ordem de itens
switches = ["SW1", "SW2", "SW3"]
switches.append("SW4")     # adiciona

# Dicionario: chave -> valor
dispositivo = {
    "host": "192.168.1.1",
    "username": "admin",
    "device_type": "cisco_ios",
}
print(dispositivo["host"])
```

### Funcoes (organizar e reusar)

```python
def verificar_host(ip):
    """Retorna True se o host responde."""
    # (no proximo modulo isso virara um ping/ssh real)
    return ip.startswith("192.168.")

print(verificar_host("192.168.1.1"))   # True
print(verificar_host("10.0.0.5"))      # False
```

### Erros (o que voce vai ver quando funcionar errado)

- `NameError: name 'x' is not defined` -> variavel nao existe (erro de escrita).
- `TypeError: ...` -> tipos incompatíveis (ex.: int + string).
- `IndentationError` -> indentacao errada (o famoso espaco).
- A leitura de erros e HABILIDADE: leia a ultima linha primeiro.

## Exemplo pratico

Crie `ola_redes.py`:

```python
redes = ["192.168.1.0/24", "192.168.2.0/24", "10.0.0.0/8"]

for rede in redes:
    prefixo = rede.split("/")[0]
    print(f"A rede {rede} tem o prefixo {prefixo}")
```

Rode: `python ola_redes.py`. Saida:
```
A rede 192.168.1.0/24 tem o prefixo 192.168.1.0
...
```

## Lab guiado (30 min)

1. Crie a pasta `03-SCRIPTS/python` (se nao existir) e um arquivo `sintaxe_base.py`.
2. Escreva um script que:
   - tem uma lista de 3 IPs de roteadores (`192.168.1.1`, `.2`, `.3`)
   - itera nessa lista
   - para cada IP, imprime `"SSH -> " + ip` só se o IP terminar em `.1` ou `.3`
3. Transforme isso numa funcao `conectar(ip)` e chame-a para cada item.
4. Adicione um dicionario de credenciais (`usuario`, `senha`) e imprima o usuario.
5. Provocou um erro propositalmente (ex.: lista[3] numa lista de 3) e leia a mensagem.

## Verificacao — "sei que aprendi quando..."

- [ ] Explico a diferenca entre lista e dicionario e quando usar cada
- [ ] Escrevo for/if/funcao sem olhar a teoria
- [ ] Leio um traceback e identifico a linha/erro em < 20s
- [ ] Sei que arquivo .py roda com `python nome.py` no terminal

## Conexao com o roadmap

- A base deste modulo alimenta tudo de Python a redes (Meses 2, 5, 6).
- Em especial: listas = lista de dispositivos; dict = credenciais/config; funcoes = organizacao do script de automacao.

## Para ir alem (opcional)

- Curso em Video (Python, Mundo 1) para reforco de comandos base.
- Praticar: escrever por extenso "minha primeira automacao" (pseudo codigo) antes de abrir o editor — pensa a logica primeiro.
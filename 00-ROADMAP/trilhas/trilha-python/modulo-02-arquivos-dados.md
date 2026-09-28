# Modulo 2 — Python para Redes: Arquivos e dados (txt, csv, json)

> Trilha: Python | Mes 2, Semana 1 | Aula 2

## Objetivo

Ler e escrever os formatos de dados que voce vai manipular em redes: listas de dispositivos em .txt, conectividade no CSV, configs e saidas em .json.

## Teoria

### Arquivos de texto (.txt)

```python
# Ler o arquivo inteiro
with open("dispositivos.txt", "r") as f:     # "r" = read
    conteudo = f.read()
print(conteudo)

# Ler linha por linha -> lista
with open("dispositivos.txt") as f:
    linhas = f.readlines()          # ["192.168.1.1\n", "192.168.1.2\n"]

# Limpar o \n
ips = [linha.strip() for linha in linhas]
```

### Escrever

```python
hosts = ["SW1", "SW2", "SW3"]

with open("configs/backup.txt", "w") as f:   # "w" = write (sobrescreve!)
    for h in hosts:
        f.write(h + "\n")
```

Cuidado com modos: `"r"` leitura, `"w"` sobrescreve, `"a"` adiciona ao final.

### CSV (planilha) — arquivo de inventario

```python
import csv

# Ler
with open("inventario.csv") as f:
    leitor = csv.DictReader(f)      # cada linha vira dict (usa o header como chave)
    for linha in leitor:
        print(linha["ip"], linha["site"])

# Escrever
with open("saida.csv", "w", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerow(["dispositivo", "ip", "status"])   # header
    escritor.writerow(["SW1", "192.168.1.1", "ok"])
```

### JSON — o formato das APIs/equipamentos

```python
import json

dados = {
    "hostname": "SW1",
    "vlans": [10, 20, 30],
    "ativo": True,
}

# Python -> texto JSON
texto = json.dumps(dados, indent=2)
print(texto)

# texto JSON -> Python
de_volta = json.loads(texto)
print(de_volta["hostname"])
```

Em redes, JSON e onipresente (saidas do IOS via RESTCONF/NETCONF, Google/API de cloud, `show` parseado). Dominar dict/json é dominar a "linguagem" dos dados.

### Caminhos relativos vs absolutos

- Relativo: `"dispositivos.txt"` (relativo a pasta onde o script roda).
- Absoluto: `"C:/Users/.../dispositivos.txt"`.
- Use `os.path.join` para montar caminhos seguros entre SOs:
  ```python
  import os
  caminho = os.path.join("03-SCRIPTS", "python", "dispositivos.txt")
  ```

## Exemplo pratico

Criar um mini inventário e criar um "estado" dele:

```python
import csv, json

# dados
inventario = [
    {"host": "SW1", "ip": "192.168.1.1", "vlan": 10},
    {"host": "SW2", "ip": "192.168.1.2", "vlan": 20},
]

# grava CSV
with open("inventario.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["host", "ip", "vlan"])
    w.writeheader()
    w.writerows(inventario)

# le e salva como JSON
with open("inventario.csv") as f:
    linhas = list(csv.DictReader(f))
with open("inventario.json", "w") as f:
    json.dump(linhas, f, indent=2)
```

## Lab guiado (30 min)

1. Crie `dispositivos.txt` com 5 IPs ficticios (um por linha).
2. Script: leia o arquivo, remova quebras de linha, imprima quantos dispositivos ha.
3. Adicione um novo IP e grave o arquivo de volta (`artesenho manual do inventario`).
4. Crie um `.json` com 3 dispositivos e leia de volta, imprimindo as chaves.
5. (Desafio) monte um CSV com `ip,host,role` e escreva um script que conta quantos integram o papel "roteador".

## Verificacao — "sei que aprendi quando..."

- [ ] Uso `with open` para ler e escrever arquivos (e o `with` fecha sozinho)
- [ ] Sei a diferenca de "r", "w", "a" e os possiveis erros ao abrir arquivo
- [ ] Leio um CSV e um JSON com `csv` e `json`
- [ ] Vejo um JSON e digo se e valido e que estruturas tem (dict/list/str/int/bool)
- [ ] Troco dados de csv -> dict -> json naturalmente

## Conexao com o roadmap

- Base para: lista de dispositivos lida de arquivo (Projeto 2) e inventario Ansible (Mes 6).
- A partir daqui, todo script do acervo vem de arquivo (nada de IP "na mao" dentro do codigo).

## Para ir alem (opcional)

- Mais tarde: curto sobre "formatos de dados de inventario de redes" e exemplos na documentacao NAPALM.
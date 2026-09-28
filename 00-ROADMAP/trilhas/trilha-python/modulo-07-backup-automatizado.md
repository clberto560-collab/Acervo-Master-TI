# Modulo 7 — Python para Redes: Backup automatizado de configuracoes (Projeto 2)

> Trilha: Python | Mes 2, Semana 4 | Aula 7

## Objetivo

**Projeto 2 completo**: conectar em 3+ dispositivos, ler a config, salvar com nome padronizado e gerar relatorio. O resultado publica como portfolium no GitHub.

## Teoria

### O que o projeto deve entregar

1. Ler lista de dispositivos de um arquivo (txt).
2. Para cada um: conectar (netmiko), executar `show running-config`.
3. Salvar a config com nome padrao: `backup_{hostname}_{data}.cfg`.
4. Tratar falha individual (timeout/auth) SEM abortar o lote.
5. Log com resumo: quantos OK, quantos falharam.

### Decisao de design (por que assim)

- **Arquivo de entrada**: você nao edita o script para mudar equipamento — muda o txt. (Separa dados do codigo.)
- **Funcoes pequenas**: `ler_dispositivos()`, `backup_um(ip)`, `main()`. Facil testar e ler.
- **Estrutura de pasta**: `dados/dispositivos.txt`, `backups/` para output.
- **Relatorio**: log simples + gravar `relatorio.json` (resumo) para consumo futuro (Aula 2/6).

### Estrutura final (para publicar)

```
02-automacao-backup/
├── README.md               (instrucoes + como rodar)
├── dados/
│   └── dispositivos.txt
├── backups/                (saidas geradas)
└── backup_configs.py
```

## Codigo (versao final do projeto)

```python
#!/usr/bin/env python3
"""Backup de configuracoes de dispositivos Cisco via SSH (netmiko)."""

import json
import logging
from datetime import datetime
from pathlib import Path

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

DADOS = Path("dados/dispositivos.txt")
SAIDA = Path("backups")
CREDS = {"username": "admin", "password": "senha-do-lab"}   # em producao: env vars!


def ler_dispositivos(caminho: Path) -> list[str]:
    """Le IPs/visoes uma por linha, ignorando vazias/comentarios."""
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")
    return [linha.strip() for linha in caminho.read_text().splitlines() if linha.strip() and not linha.startswith("#")]


def backup_um(ip: str) -> tuple[str, str]:
    """Conecta, baixa a config e salva em arquivo. Retorna (ip, hostname)."""
    conexao = ConnectHandler(device_type="cisco_ios", host=ip, **CREDS)
    hostname = conexao.send_command("show running-config | include hostname").split()[-1]
    config = conexao.send_command("show running-config")
    conexao.disconnect()

    SAIDA.mkdir(exist_ok=True)
    nome = f"backup_{hostname}_{datetime.now():%Y%m%d_%H%M}.cfg"
    (SAIDA / nome).write_text(config)
    logging.info(f"{ip} OK -> {nome}")
    return ip, hostname


def main() -> None:
    dispositivos = ler_dispositivos(DADOS)
    ok, falhas = [], []

    for ip in dispositivos:
        try:
            _, hostname = backup_um(ip)
            ok.append(ip)
        except NetmikoTimeoutException:
            logging.error(f"{ip} timeout (sem SSH/resposta)")
            falhas.append({"ip": ip, "erro": "timeout"})
        except NetmikoAuthenticationException:
            logging.error(f"{ip} autenticacao falhou")
            falhas.append({"ip": ip, "erro": "auth"})

    resumo = {"total": len(dispositivos), "ok": ok, "falhas": falhas}
    (SAIDA / "relatorio.json").write_text(json.dumps(resumo, indent=2))

    logging.info(f"Fim: {len(ok)}/{len(dispositivos)} OK, {len(falhas)} falhas")


if __name__ == "__main__":
    main()
```

Rodar: `python backup_configs.py`.

## Lab guiado (finalizacao do projeto — 60 min)

1. Monte a estrutura de pastas acima.
2. `dados/dispositivos.txt` com os IPs do seu lab (3 equipamentos cisco_ios com SSH).
3. Rode o script. Confira: `backups/` com `.cfg` por equipamento (veja o nome com hostname+data) e `relatorio.json`.
4. Quebre um outro dispositivo (desligue) e rode de novo: **o lote sofre e termina** (falha registrada no JSON).
5. Escreva o `README.md` do projeto respondendo: o que faz, prerequisitos, como rodar, exemplo de saida, lições aprendidas. (Vira modelo do template de projeto em `04-PROJETOS`.)
6. Publique no GitHub (repositorio proprio ou dentro do Acervo em `04-PROJETOS/projeto-02-backup-configs/`).

## Verificacao — "sei que aprendi quando..."

- [ ] Progresso: 3+ dispositivos em lote, sem hardcode de IP no codigo
- [ ] Saidas com nome padronizado (hostname + data)
- [ ] Falha de 1 dispositivo nao derruba o lote
- [ ] Credenciais fora do codigo (ou de forma segura) e nada de sensivel no git
- [ ] Passei do "exemplo" para "projeto publicavel" (README + pasta organizada)

## Conexao com o roadmap

- Este e o **Projeto 2** oficial (Mes 2). Reaproveita Aulas 1-6.
- Serve de base para o Mes 6 (GitHub organizado + portfolio) e para automatizacao avancada (Ansible, Mes 6).

## Para ir alem (opcional)

- Evolucao: receber progresso por `send_command(..., read_timeout=...)` e `delay_factor` para configs longas.
- Adicionar "diff" entre o backup de hoje e o de ontem (novo campo no relatorio).
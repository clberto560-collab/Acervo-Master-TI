# SCRIPTS

Biblioteca de scripts proprios (Python/Bash) versionados e comentados.

## Regras de higiene

- Todo script tem **docstring** no topo: o que faz, como rodar, prerequisitos.
- **Nada de senha/chave hardcoded** — use variaveis de ambiente ou `getpass`.
- Rode em **dry-run/ambiente de teste** antes de qualquer dispositivo real.
- Nome descritivo: `backup_configs_netmiko.py`, `cria_vlans_lista.py`.

## Estrutura sugerida

```
03-SCRIPTS/
├── python/
│   ├── backup_configs_netmiko.py
│   ├── aplica_vlans.py
│   └── le_lista_dispositivos.py
├── bash/
│   ├── backup_diario.sh
│   └── harden_user_fw.sh
└── README.md   (este arquivo — listar scripts novos aqui)
```

## Indice de scripts

| Data | Script | O que faz | Trilha atraves |
|------|--------|-----------|----------------|
| (preencher) | | | |

## Changelog (mente do "produzir, nao colecionar")

- [ ] primeiro script criado
- [ ] ... (acompanha seu progresso aqui)
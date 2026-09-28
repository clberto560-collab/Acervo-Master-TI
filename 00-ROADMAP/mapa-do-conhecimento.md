# Mapa do Conhecimento

Objetivo final: **pro-híbrido Redes + Programação + Segurança** (Analista de Redes Sênior, Especialista em Infraestrutura Segura, DevSecOps, Engenheiro de Redes com automação, Cybersecurity Analyst).

Este mapa explica a *ordem de aprendizado* e as *dependencias* — por que voce estuda cada area naquele momento.

---

## As 6 areas e os "porques"

```
        ┌──────────────────────────────────────────────────────────┐
        │                      1. REDES                            │
        │   (fundacao de tudo — voce aplica 100% do resto nelas)   │
        └───────────────────────────┬──────────────────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │  2. PYTHON APLICADO │   │   3. LINUX        │   │   6. AUTOMACAO   │
   │  a redes          │   │   (shell, perl-   │   │  (Ansible,        │
   │  (netmiko,        │   │   missoes,         │   │   Docker)         │
   │   paramiko)       │   │   servicos)        │   │                   │
   └─────────┬────────┘   └─────────┬────────┘   └─────────┬────────┘
             │                      │                      │
             └──────────┬───────────┴───────────┬──────────┘
                        ▼                       ▼
              ┌──────────────────────────────────────────────┐
              │               5. SEGURANCA                   │
              │   firewall, IDS, Wireshark, TryHackMe,       │
              │   Blue/Red Team — consome Redes + Linux      │
              └──────────────────────────────────────────────┘
                        │
                        ▼
              ┌──────────────────────────────────────────────┐
              │             4. DEVOPS / CLOUD                │
              │   CI/CD, IaC, Docker/K8s, AWS/Azure          │
              │   (a vitrine de empregabilidade final)       │
              └──────────────────────────────────────────────┘
```

(Numeracao = ordem de aprendizado, com 4 dependente de 5 e 6 juntos no fim.)

---

## Ordem pedagogica e por que ela existe

| # | Area | Pre-requisitos | Motivo da posicao na fila |
|---|------|----------------|---------------------------|
| 1 | **Redes** | nenhum | Tudo o resto depende de IP, roteamento, switch, topologia |
| 2 | **Python para redes** | Redes (min: IP, SSH, config router) | Automacao so faz sentido quando voce sabe o que esta automatizando |
| 3 | **Linux** | Redes | Ambiente real de trabalho e a base da seguranca (logs, servicos, firewall) |
| 4 | **Seguranca** | Redes + Linux | Ataque/defesa exige entender camadas e sistemas |
| 5 | **Automacao/DevOps** | Python + Linux | Docker/Ansible assumem que voce ja programa e opera o SO |
| 6 | **Cloud / IaC** | DevOps basico | Apos entender infra local, voce replica em nuvem |

Erro classico que este mapa evita: fazer pentest/DevOps sem Redes ou Linux solidos. Vira "imitador de tutorial" e trava na entrevista tecnica.

---

## Dependencias criticas (nao pule)

- `Redes (subnetting + roteamento)` -> tudo
- `SSH/configuracao de equipamento` -> automacao com Python
- `Linux terminal + permissoes + logs` -> seguranca e DevSecOps
- `Python logica + funcoes` -> scripts, automacao, seguranca

---

## Criterio de "dominado" por area

Voce so avança de area quando produzir o artefato de saida:

| Area | Artefato que prova dominio |
|------|----------------------------|
| Redes | Topologia completa no GNS3/Packet Tracer funcionando e documentada (lab) |
| Python p/ redes | Script conectando em 3+ dispositivos e aplicando/baixando config |
| Linux | Servidor configurado do zero via terminal (users, permissões, cron, firewall) |
| Seguranca | Lab de bloqueio/deteccao documentado com Wireshark + logs |
| Automacao | Playbook Ansible + container Docker operacionais |
| Cloud/IaC | Infra provisionada com Terraform documentada |

---

## Areas de apoio (nao bloqueiam, mas somam)

- **Git/GitHub** — use desde o dia 1 (todo artefato aqui e versionado)
- **Wireshark** — companheiro diario de quem mexe em rede
- **Documentacao/Markdown** — o acervo inteiro depende disso

---

## O perfil final (o que voce sera)

```
TI Hibrido
├── Redes: subnetting fluente, VLAN/VTP/STP, roteamento estatico/dinamico (OSPF/BGP)
├── Python: scripts de automacao de config e backup
├── Linux: operacao fluida, servicos, firewall, logs
├── Seguranca: firewall/ACL, IDS/IPS, analise de trafego, deteccao de ataques
├── Automacao: Ansible, Docker, CI/CD basico, IaC
└── Emprego: portfolio Git + LinkedIn + 1 certificacao (CCNA ou Security+)
```
# Modulo 9 — acesso e configuracao de roteadores/switches via CLI (Cisco)

> Trilha: Redes | Mes 2, Semana 1 | Aula 9

## Objetivo

Operar equipamento Cisco no terminal com autonomia: acessar, entrar no modo certo, configurar e **salvar**. E a porta de entrada para a automacao com Python (Mes 2).

## Teoria

### Modos do IOS (navegacao)

| Modo | Prompt | O que faz |
|------|--------|-----------|
| User EXEC | `Router>` | visao basica, comandos show limitados |
| Privileged EXEC | `Router#` | `enable` — acesso as configs e comandos show completos |
| Global Configuration | `Router(config)#` | `configure terminal` — config global |
| Interface/Sub | `Router(config-if)#` | dentro de uma interface |
| Line/VTY | `Router(config-line)#` | linhas de console/SSH/aux/telnet |

Fluxo: `Router>` -> `enable` -> `Router#` -> `configure terminal` -> `Router(config)#` -> configura interfaces, rotas, etc.

### Comandos essenciais (categoria)

| Categoria | Exemplo |
|-----------|---------|
| Navegar | `enable`, `exit`, `end`, `configure terminal`, `interface g0/0` |
| Ver | `show running-config`, `show ip interface brief`, `show ip route`, `show vlan brief`, `show mac address-table`, `show startup-config` |
| Salvar | `write memory` (= `copy running-config startup-config`) |
| Apagar/recarregar | `erase startup-config`, `reload` |
| Autenticacao | `enable secret`, `username ... secret`, `line vty 0 4 ... password` |
| Seguranca basica | `service password-encryption`, `login local`, `transport input ssh` |

### Configuracao minima de seguranca (sempre)

```
enable secret <senha forte>
line console 0
  password <senha>
  login
line vty 0 4
  transport input ssh
  login local
username admin privilege 15 secret <senha>
service password-encryption
```

**Regra:** nunca deixe telnet ligado, nunca senha fraca de enable, sempre `write memory`.

### SSH vs Telnet

- Telnet: texto puro (capturavel). **Nao usar.**
- SSH: criptografado. Sempre o padrao. **SSH exige par de chaves ou usuario/senha e configuracao (ip domain-name, crypto key generate rsa).**

## Exemplo pratico (config basica de acesso remoto)

```
enable
configure terminal
hostname SW-ACERVO
!
ip domain-name acervo.local
crypto key generate rsa modulus 2048
!
username admin privilege 15 secret MinhaSenhaForte
line vty 0 4
  transport input ssh
  login local
  exit
!
enable secret MinhaSenhaForte
service password-encryption
!
end
write memory
```

## Lab guiado (60 min) — o lab que aprende entre R1 e R2

Objetivo: configurar SSH e ver o `show running-config` pela primeira vez com seguranca.

1. Topologia simples: **1 switch** (ou roteador) no Packet Tracer/GNS3.
2. **Consiga o prompt:** `enable` (sem senha ainda) -> `configure terminal`.
3. **Configuracoes base:** hostname, enable secret, service password-encryption.
4. **SSH:** ip domain-name, crypto key generate rsa, username, line vty, transporte input ssh.
5. **Interface de gerencia** (switch): vlan 1 ou SVI `interface vlan 1` + `ip address 192.168.1.10/24` + `no shutdown`.
6. **Salve:** `write memory`.
7. `show running-config` -> encontre no texto tudo que configuramos. Identifique o que o IOS reescreve (ex.: a senha cifrada em enable).
8. No CMD, acesse de fora do proprio lab para testar SSH: formatos como `ssh -l admin 192.168.1.10` (no lab real). Se o usuario usado, coloque o PC na mesma VLAN.
9. **Backup manual:** `show running-config` -> copie a saida para um arquivo .txt em `03-SCRIPTS` (repetiremos isso automatizado no Mes 2!).

## Verificacao — "sei que aprendi quando..."

- [ ] Navego entre os modos IOS sem consulta (prompt correto)
- [ ] Configuro telnet desabilitado + SSH habilitado num equipamento
- [ ] Salvo config com `write memory` e explico a diferenca running vs startup
- [ ] Leio um `show running-config` e localizo: hostname, enable, vty, interfaces
- [ ] Faco backup da config num arquivo .txt (base do Projeto 2)

## Conexao com o roadmap

- **Projeto 2 (Mes 2)** depende de voce saber CLI Cisco: o script Python vai fazer SSH em 3+ dispositivos e dar comandos — que voce ja conhece daqui.
- Seguranca (Mes 4): ACL e port security usam exatamente o CLI deste modulo.

## Para ir alem (opcional)

- Fazer o "exame" mental: desenhe um roteador com 2 portas e escreva a config minima de IP+SSH de cabo para cabo (treino de entrevista tecnica).
- Instalar e usar o "network simulator GNS3" se ainda nao usa (vamos precisar no Projeto 2).
# -*- coding: utf-8 -*-
"""DC CORP - RPG TECNOLOGICO (prototipo)

Voce entra na DC Corp como estagiario de infra e evolui de cargo realizando
missoes de TI reais em terminais simulados. Cada missao ensina um pilar:
VLAN, switch, trunk, roteamento, firewall, analise de trafego, defesa...

Como jogar: python dc_corp_jogo.py
Na central de operacoes use os numeros das opcoes.
O DETONADO (opcao 3) e o guia passo a passo de cada missao.

Requires: Python 3 (sem dependencias externas).
"""

import os
import sys
import time

if os.name == "nt":
    os.system("")  # habilita cores ANSI no terminal Windows

RESET = "\033[0m"
COR = {
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}

INTERATIVO = sys.stdin.isatty()


def cr(texto, cor):
    return f"{COR[cor]}{texto}{RESET}"


def motd(linhas, delay=0.015):
    for item in linhas:
        if isinstance(item, tuple):
            texto, cor = item
            print(cr(texto, cor))
        else:
            print(item)
        if INTERATIVO:
            time.sleep(delay)


def ler(prompt=""):
    try:
        return input(prompt).strip()
    except EOFError:
        return "eof"


# ---------------------------------------------------------------------------
# PERSONAGEM E PROGRESSAO
# ---------------------------------------------------------------------------

# (xp acumulado minimo, cargo) - a espinha da progressao
CARGOS = [
    (0, "Estagiario Recem-Admitido"),
    (300, "Tecnico que Surpreendeu o Valente"),
    (700, "Operador de Rede em Ascensao"),
    (1300, "Engenheiro de Infra Junior"),
    (2100, "Analista de Redes Pleno"),
    (3000, "Guardiao do Perimetro"),
    (4200, "Especialista em Defesa Cibernetica"),
    (5600, "Arquiteto de Solucoes"),
    (7200, "Braco Direito da DC Corp"),
    (9000, "O Profissional Hibrido (lenda urbana)"),
]


def cargo_atual(xp):
    atual = CARGOS[0][1]
    for limite, nome in CARGOS:
        if xp >= limite:
            atual = nome
        else:
            break
    return atual


def proximo_cargo(xp):
    for limite, nome in CARGOS:
        if xp < limite:
            return nome, limite
    return None, None


class Personagem:
    def __init__(self):
        self.nome = "Cleber"
        self.xp = 0
        self.acertos = 0
        self.erros = 0
        self.missoes = {}  # id -> "concluida"

    def ganha_xp(self, pontos, motivo=None):
        antes = cargo_atual(self.xp)
        self.xp += pontos
        depois = cargo_atual(self.xp)
        marca = f"  [+{pontos} XP]" if not motivo else f"  [+{pontos} XP] {motivo}"
        print(cr(marca, "green"))
        if depois != antes:
            self.level_up(depois)

    def level_up(self, cargo):
        prox, limite = proximo_cargo(self.xp)
        print()
        print(cr("=" * 60, "yellow"))
        print(cr(f"  ** LEVEL UP **  Novo cargo: {cargo}", "yellow"))
        if prox:
            print(cr(f"  Proximo nivel em {prox} (precisa de {limite} XP)", "dim"))
        print(cr("=" * 60, "yellow"))
        print()

    def status_perfil(self):
        prox, limite = proximo_cargo(self.xp)
        linhas = [
            cr("== FICHA DO ESTAGIARIO ==", "bold"),
            f"  Nome          : {self.nome}",
            f"  Cargo         : {cr(cargo_atual(self.xp), 'cyan')}",
            f"  Experiencia   : {self.xp} XP",
        ]
        if prox:
            linhas.append(f"  Proximo nivel : {prox} ({self.xp}/{limite} XP)")
        else:
            linhas.append(cr("  Ranking Maximo alcancado. A lenda e voce.", "yellow"))
        concluidas = [m for m in MISSOES.values() if m["id"] in self.missoes]
        linhas.append(f"  Missoes feitas: {len(concluidas)}/{len(MISSOES)}")
        linhas.append(f"  Bravatas       : {self.acertos} acertos / {self.erros} erros no terminal")
        return "\n".join(linhas)


# ---------------------------------------------------------------------------
# CATALOGO DE MISSOES (cada missao = um pilar do oficio)
# ---------------------------------------------------------------------------

# 1 = JOGAVEL  |  2 = em breve  |  3 = concluida
def status_missao(jogo, mid):
    if mid in jogo.missoes:
        return 3
    return MISSOES[mid]["estado"]

MISSOES = {
    "m1": {
        "id": "m1",
        "capitulo": 1,
        "titulo": "O Primeiro Dia",
        "estado": 1,
        "lv": 1,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "A rede do andar 15 caiu: as VLANs sumiram das configs.",
        "objetivo": "Recriar a VLAN 10 (TI) nos switches SW-01 e SW-02 e salvar a configuracao.",
        "aprender": "Configuracao basica de VLAN e a rotina de salvar config (write memory).",
        "recompensa": 300,
        "guia": [
            "1) No terminal do SW-01, suba de nivel: digite  enable",
            "2) Confira o estado atual:  show vlan brief   (repare: NAO existe VLAN 10)",
            "3) Entre na configuracao global:  configure terminal",
            "4) Crie a VLAN 10:  vlan 10",
            "5) Nomeie a VLAN:  name TI",
            "6) Volte e salve:  end  e depois  write memory",
            "7) Troque de equipamento:  conectar SW-02",
            "8) Repita os passos 1 a 6 no SW-02",
            "9) Confira:  show vlan brief  nos dois deve listar a VLAN 10 como TI",
            "10) (Dica) Travou? digite  dica  dentro do terminal a qualquer momento.",
        ],
    },
    "m2": {
        "id": "m2",
        "capitulo": 2,
        "titulo": "Unindo os Andares",
        "estado": 2,
        "lv": 2,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "O andar 14 precisa falar com o 15. Dois switches, um trunk, VLANs espalhadas.",
        "objetivo": "Criar VLANs nos dois switches, configurar trunk 802.1Q e testar comunicacao entre VLANs.",
        "aprender": "Trunk, tag 802.1Q, VLANs multiplas e o perigo dos loops (STP deixa pra tristeza depois).",
        "recompensa": 450,
        "guia": [
            "1) Criar as VLANs 10 (TI) e 20 (RH) nos dois switches.",
            "2) Configurar a porta que liga SW-01 e SW-02 como trunk.",
            "3) Liberar apenas as VLANs 10 e 20 no trunk.",
            "4) Testar: hosts de VLANs iguais conversam; de VLANs diferentes nao.",
            "5) (Em contrucao no jogo - gameplay chegando).",
        ],
    },
    "m3": {
        "id": "m3",
        "capitulo": 3,
        "titulo": "Estradas da DC Corp",
        "estado": 2,
        "lv": 3,
        "npc": "Sr. Valente (CEO)",
        "ambientacao": "Os andares viraram redes separadas. Agora precisa ligar tudo com roteadores.",
        "objetivo": "Configurar roteamento estatico entre redes e NAT para a Internet.",
        "aprender": "Tabela de rotas, rota estatica, default route e NAT/PAT.",
        "recompensa": 600,
        "guia": [
            "1) Enderecar as interfaces dos roteadores.",
            "2) Criar rotas estaticas para as redes vizinhas.",
            "3) Configurar default route para a borda.",
            "4) Implementar NAT (overload) para os hosts sairem com IP publico.",
            "5) Provar com ping entre redes diferentes.",
        ],
    },
    "m4": {
        "id": "m4",
        "capitulo": 4,
        "titulo": "O Muro da Empresa",
        "estado": 2,
        "lv": 4,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "O financeiro descobriu que o RH acessa os servidores da diretoria. Briga feia.",
        "objetivo": "Criar regras de firewall: bloquear a VLAN do RH de acessar a rede da diretoria.",
        "aprender": "ACL (Cisco) e regras de firewall, ordem das regras e verificacao com contadores.",
        "recompensa": 800,
        "guia": [
            "1) Mapear as redes envolvidas (RH, TI, Diretoria).",
            "2) Escrever ACL que nega RH -> Diretoria.",
            "3) Aplicar a ACL na interface correta (entrada ou saida).",
            "4) Permitir o resto do trafego depois da regra de negacao.",
            "5) Verificar com contadores de pacotes (show access-lists).",
        ],
    },
    "m5": {
        "id": "m5",
        "capitulo": 5,
        "titulo": "O Carteiro Digital",
        "estado": 2,
        "lv": 5,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "120 computadores pra configurar na mao todo dia. A DC Corp precisa de DHCP.",
        "objetivo": "Subir um servidor DHCP e DNS funcional para as redes da DC Corp.",
        "aprender": "DHCP (DORA, lease, pool), DNS (resolucao, registros A/AAAA/MX).",
        "recompensa": 1000,
        "guia": [
            "1) Configurar pool DHCP para cada rede.",
            "2) Apontar gateway e DNS no pool.",
            "3) Configurar registros de DNS para os servidores internos.",
            "4) Provar: host pega IP por DHCP e resolve nomes.",
        ],
    },
    "m6": {
        "id": "m6",
        "capitulo": 6,
        "titulo": "Espionando o Trafego",
        "estado": 2,
        "lv": 6,
        "npc": "Dra. Santos (Seguranca)",
        "ambientacao": "Alguem esta mandando dados pra fora na calada da noite. A DC Corp precisa de olhos.",
        "objetivo": "Capturar e analisar trafego da rede, encontrar o trafego suspeito.",
        "aprender": "Wireshark (filtros), nmap, identificacao de protocolos e anomalias.",
        "recompensa": 1200,
        "guia": [
            "1) Escanear a rede-alvo com nmap (hosts e servicos).",
            "2) Capturar trafego com Wireshark/filtros.",
            "3) Identificar protocolos suspeitos e portas estranhas.",
            "4) Relatar o que encontrou como ticket de seguranca.",
        ],
    },
    "m7": {
        "id": "m7",
        "capitulo": 7,
        "titulo": "Visao de Coruja",
        "estado": 2,
        "lv": 7,
        "npc": "Dra. Santos (Seguranca)",
        "ambientacao": "A infra cresceu e ninguem enxerga mais o que acontece nos servidores.",
        "objetivo": "Implantar monitoramento de logs (Wazuh) e detectar eventos suspeitos.",
        "aprender": "SIEM basico, coleta de logs, alertas, resposta a incidente.",
        "recompensa": 1500,
        "guia": [
            "1) Instalar e configurar o agente de monitoramento.",
            "2) Coletar logs de autenticacao de um servidor.",
            "3) Detectar uma tentativa de acesso suspeita.",
            "4) Documentar o incidente do inicio ao fim.",
        ],
    },
    "m8": {
        "id": "m8",
        "capitulo": 8,
        "titulo": "A Infra que se Configura Sozinha",
        "estado": 2,
        "lv": 8,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "O Valente quer cortar custo manual. Ele descobriu a palavra 'automacao'.",
        "objetivo": "Automatizar configuracao e backup dos equipamentos com Python/Ansible.",
        "aprender": "Python + Netmiko (SSH em lote), Ansible, infra como codigo.",
        "recompensa": 1800,
        "guia": [
            "1) Conectar via SSH em varios dispositivos com script.",
            "2) Automatizar backup de configuracao.",
            "3) Criar playbook que aplica config em N servidores.",
            "4) Deixar a DC Corp a prova de apagao.",
        ],
    },
    "m9": {
        "id": "m9",
        "capitulo": 9,
        "titulo": "O Defensor Final",
        "estado": 2,
        "lv": 9,
        "npc": "Dra. Santos (Seguranca) + Sr. Valente",
        "ambientacao": "Um teste de invasao autorizado (red team) vai tentar entrar na DC Corp. Voce defende.",
        "objetivo": "Detectar, responder e expulsar um invasor simulado antes que ele chegue aos servidores.",
        "aprender": "Ciclo completo de defesa: deteccao, analise, contencao, erradicacao, recuperacao.",
        "recompensa": 2400,
        "guia": [
            "1) Reconhecer os primeiros sinais (scan, brute force, movimentacao lateral).",
            "2) Conter o acesso do invasor em cada fronteira.",
            "3) Erradicar a presenca e restaurar configs.",
            "4) Entregar o relatorio final pro Valente (com XP gordo).",
        ],
    },
}


def mapa_missoes(jogo):
    linhas = [cr("== MAPA DE MISSOES / CAPITULOS ==", "bold")]
    for m in MISSOES.values():
        st = status_missao(jogo, m["id"])
        if st == 3:
            badge = cr(" CONCLUIDA ", "green")
        elif st == 1:
            badge = cr(" JOGAVEL ", "cyan")
        else:
            badge = cr(" EM BREVE ", "dim")
        linhas.append(
            f"  Cap.{m['capitulo']:>2} | Lv.{m['lv']:<2} | {badge} | {m['titulo']}"
        )
    linhas.append("")
    linhas.append(cr("Para ver o DETONADO detalhado de uma missao, digite: detonado <numero-do-capitulo>", "dim"))
    return "\n".join(linhas)


def mostrar_detonado(jogo, capitulo=None):
    linhas = [cr("== DETONADO - GUIA PASSO A PASSO ==", "bold")]
    for m in MISSOES.values():
        if capitulo is not None and m["capitulo"] != capitulo:
            continue
        st = status_missao(jogo, m["id"])
        badge = {3: cr("CONCLUIDA", "green"), 1: cr("JOGAVEL", "cyan"), 2: cr("EM BREVE", "yellow")}[st]
        linhas.append("")
        linhas.append(cr(f"--- Capitulo {m['capitulo']}: {m['titulo']} ---", "bold"))
        linhas.append(f"  Quem passa    : {m['npc']}   {badge}")
        linhas.append(f"  Nivel preciso : {m['lv']}")
        linhas.append(f"  Cenario       : {m['ambientacao']}")
        linhas.append(cr(f"  Objetivo      : {m['objetivo']}", "cyan"))
        linhas.append(f"  Aprende       : {m['aprender']}")
        linhas.append(f"  Recompensa    : {m['recompensa']} XP")
        linhas.append(cr("  Guia passo a passo:", "yellow"))
        for passo in m["guia"]:
            linhas.append(f"     {passo}")
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# GAMEPLAY: MISSÃO 1 (CLI Cisco simulada)
# ---------------------------------------------------------------------------

def novo_switch(codigo):
    return {
        "cod": codigo,
        "hostname": codigo,
        "modo": "user",
        "ctx_vlan": None,
        "vlans": {1: "default"},
        "saved": False,
        "vlan10_ok": False,
    }


class Missao1:
    def __init__(self, jogo):
        self.jogo = jogo
        self.switches = {"SW-01": novo_switch("SW-01"), "SW-02": novo_switch("SW-02")}
        self.atual = None

    @property
    def switch(self):
        return self.atual

    def prompt(self):
        if self.atual is None:
            return cr("DC-CORP/>", "cyan")
        s = self.atual
        modos = {
            "user": f"{s['hostname']}>",
            "priv": f"{s['hostname']}#",
            "conf": f"{s['hostname']}(config)#",
            "conf-vlan": f"{s['hostname']}(config-vlan)#",
        }
        return cr(modos[s["modo"]], "cyan")

    def ver_switches(self):
        out = [cr("Switches do andar 15:", "bold")]
        for cod, s in self.switches.items():
            v10 = "VLAN 10: TI" if s["vlan10_ok"] else "VLAN 10: AUSENTE"
            save = "salvo" if s["saved"] else "nao salvo"
            out.append(f"  {cr(cod, 'green')} | {v10} | config {cr(save, 'yellow')}")
        return "\n".join(out)

    def vitoria(self):
        return all(s["vlan10_ok"] and s["saved"] for s in self.switches.values())

    def comando_desconhecido(self, linha):
        self.jogo.erros += 1
        print(cr("% Invalid input detected at '^' marker.", "red"))
        print("   " + linha)
        if linha.split():
            print("   " + " " * len(linha.split()[0]) + "^")
        print(cr("Digite help para ver os comandos disponiveis.", "dim"))

    def comando_errado(self, msg):
        self.jogo.erros += 1
        print(cr(msg, "red"))

    def help_switch(self):
        s = self.atual
        base = [
            cr("== COMANDOS DO " + s["hostname"] + " ==", "bold"),
            "  enable                          entra no modo privilegiado",
            "  show vlan brief                 mostra as VLANs do switch",
            "  show running-config             mostra a configuracao atual",
            "  conectar SW-01|SW-02            troca de equipamento",
            "  missao / detonado / dica        objetivo, guia e pista",
            "  help / sair                     ajuda / encerra",
        ]
        if s["modo"] == "priv":
            base.insert(2, "  configure terminal (conf t)     entra no modo de configuracao")
            base.append("  write memory / end / exit        salva e navega")
        if s["modo"] == "conf":
            base = [
                cr("== COMANDOS DE CONFIGURACAO ==", "bold"),
                "  vlan <numero>                   cria/entra numa VLAN",
                "  end                            volta ao modo privilegiado",
            ]
        if s["modo"] == "conf-vlan":
            base = [
                cr("== CONFIGURANDO VLAN " + str(s["ctx_vlan"]) + " ==", "bold"),
                "  name <nome>                    da um nome a VLAN",
                "  exit / end                     sai da vlan / volta ao privilegiado",
            ]
        return "\n".join(base)

    def dica(self):
        if self.atual is None:
            return "Conecte em um switch com: conectar SW-01"
        s = self.atual
        if s["modo"] == "user":
            return "Entre no modo privilegiado com: enable"
        if s["modo"] == "priv":
            if not s["vlan10_ok"]:
                return "Use 'configure terminal' e depois 'vlan 10' para criar a VLAN 10."
            if not s["saved"]:
                return "A VLAN ja existe. Salve a configuracao com: write memory"
            return "Este switch esta pronto. Conclua no outro (conectar SW-02)."
        if s["modo"] == "conf":
            return "Crie a VLAN 10 com: vlan 10"
        if s["modo"] == "conf-vlan":
            return "Diga o nome da VLAN: name TI"
        return "Use help para ver os comandos."

    def pedir_guia(self):
        return mostrar_detonado(self.jogo, 1)

    def ac_show_vlan(self):
        s = self.atual
        linhas = ["", "VLAN Name                             Status    Ports",
                  "---- -------------------------------- --------- ---------------"]
        for vid, nome in s["vlans"].items():
            if vid == 1:
                linhas.append(f"{vid:<4} {nome:<32} active    Fa0/1-24")
            else:
                linhas.append(f"{vid:<4} {nome:<32} active")
        linhas.append("")
        return "\n".join(linhas)

    def ac_show_running(self):
        s = self.atual
        partes = ["Building configuration...", "",
                  "Current configuration, " + ("atualizada" if s["saved"] else "NAO salva"), "!"]
        partes.append("hostname " + s["hostname"])
        partes.append("!")
        for vid, nome in s["vlans"].items():
            partes.append("vlan %d" % vid)
            partes.append(" name %s" % nome)
            partes.append("!")
        partes += ["interface FastEthernet 0/1", " switchport mode access",
                   " switchport access vlan " + (str(10) if s["vlan10_ok"] else "1"), "!", "end"]
        return "\n".join(partes)

    def ac_enable(self):
        s = self.atual
        if s["modo"] != "user":
            self.comando_errado("% Command not allowed in this mode.")
            return
        s["modo"] = "priv"
        print(cr("Senha de enable: ************", "dim"))
        print(cr("Enable granted.", "green"))
        self.jogo.ganha_xp(5, "modo privilegiado")

    def ac_conf_t(self):
        s = self.atual
        if s["modo"] != "priv":
            self.comando_errado("% Command not allowed in this mode.")
            return
        s["modo"] = "conf"
        print("Entrando no modo de configuracao global...")

    def ac_vlan(self, arg):
        s = self.atual
        if s["modo"] != "conf":
            self.comando_errado("% vlan is only allowed in configuration mode.")
            return
        if not arg:
            self.comando_errado("% Incomplete command.")
            return
        try:
            vid = int(arg)
        except ValueError:
            self.comando_errado("% Invalid number.")
            return
        if not (1 <= vid <= 4094):
            self.comando_errado("% VLAN id must be between 1 and 4094.")
            return
        s["ctx_vlan"] = vid
        s["modo"] = "conf-vlan"
        s["vlans"].setdefault(vid, "")
        print(cr(f"Configurando a VLAN {vid}...", "bold"))
        if vid == 10 and not s["vlan10_ok"]:
            self.jogo.ganha_xp(20, f"VLAN {vid} criada no {s['hostname']}")
        elif vid != 10:
            self.jogo.ganha_xp(5, f"VLAN {vid} criada")

    def ac_name(self, arg):
        s = self.atual
        if s["modo"] != "conf-vlan":
            self.comando_errado("% Command not allowed in this mode.")
            return
        if not arg or len(arg) > 32:
            self.comando_errado("% Invalid name.")
            return
        vid = s["ctx_vlan"]
        s["vlans"][vid] = arg
        if vid == 10 and arg.upper() == "TI":
            s["vlan10_ok"] = True
            self.jogo.ganha_xp(30, f"VLAN {vid} nomeada TI no {s['hostname']}")
        elif vid == 10:
            print(cr("(hmm, o departamento pediu o nome certo... a Janaina vai reparar)", "dim"))
        else:
            self.jogo.ganha_xp(5, f"VLAN {vid} renomeada")

    def ac_write(self):
        s = self.atual
        if s["modo"] == "user":
            self.comando_errado("% Command not allowed in this mode.")
            return
        s["saved"] = True
        print(cr("Building configuration on " + s["hostname"] + "...", "bold"))
        print(cr("[OK]", "green"))
        self.jogo.ganha_xp(30, f"config salva no {s['hostname']}")

    def ac_end(self):
        s = self.atual
        s["ctx_vlan"] = None
        s["modo"] = "priv"

    def ac_exit(self):
        s = self.atual
        if s["modo"] in ("conf", "config"):
            s["ctx_vlan"] = None
            s["modo"] = "priv"
        elif s["modo"] == "conf-vlan":
            s["ctx_vlan"] = None
            s["modo"] = "conf"
        elif s["modo"] == "priv":
            s["modo"] = "user"
        else:
            print(cr("Connection closed. Volta a celula.", "yellow"))
            self.atual = None

    def processar(self, linha):
        if self.atual is None:
            return self.processar_hub(linha)
        s = self.atual
        partes = linha.split()
        if not partes:
            return True
        cmd = partes[0].lower()
        arg = partes[1] if len(partes) > 1 else ""
        arg_resto = " ".join(partes[1:])

        if cmd in ("sair", "quit"):
            return False
        if cmd == "help":
            print(self.help_switch())
            return True
        if cmd == "missao":
            print(objetivo_da_missao(self.jogo, "m1"))
            return True
        if cmd == "detonado":
            print(self.pedir_guia())
            return True
        if cmd == "dica":
            print(self.dica())
            return True
        if cmd == "show":
            if arg == "vlan":
                print(self.ac_show_vlan())
                return True
            if arg == "running-config":
                print(self.ac_show_running())
                return True
            if arg == "version":
                print(self.ac_show_version())
                return True
            if arg == "switches":
                print(self.ver_switches())
                return True
            self.comando_desconhecido(linha)
            return True
        if cmd == "enable":
            self.ac_enable()
            return True
        if cmd == "configure":
            if arg == "terminal":
                self.ac_conf_t()
                return True
            self.comando_errado("% Incomplete command. (configure terminal)")
            return True
        if cmd in ("conf", "config"):
            if arg in ("t", "terminal"):
                self.ac_conf_t()
                return True
            self.comando_errado("% Use configure terminal.")
            return True
        if cmd == "vlan":
            self.ac_vlan(arg)
            return True
        if cmd == "name":
            self.ac_name(arg_resto)
            return True
        if cmd == "write":
            if arg in ("memory", "mem"):
                self.ac_write()
                return True
            self.comando_errado("% Incomplete command. (write memory)")
            return True
        if cmd in ("wr", "save"):
            self.ac_write()
            return True
        if cmd == "end":
            self.ac_end()
            return True
        if cmd == "exit":
            self.ac_exit()
            return True
        if cmd == "conectar":
            self.ac_exit()
            if arg in self.switches:
                self.atual = self.switches[arg]
                self.atual["modo"] = "user"
                print(cr(f"Conectando a {arg} via SSH...", "bold"))
                print(cr("Autenticacao bem-sucedida.", "green"))
            else:
                self.comando_errado("% Host desconhecido. Use: conectar SW-01 ou SW-02")
            return True
        self.comando_desconhecido(linha)
        return True

    def processar_hub(self, linha):
        partes = linha.split()
        cmd = partes[0]
        arg = partes[1] if len(partes) > 1 else ""
        if cmd in ("sair", "quit"):
            return False
        if cmd == "help":
            print(cr("No terminal do switch: help  |  Para voltar ao jogo: sair", "dim"))
            return True
        if cmd == "conectar":
            if arg in self.switches:
                self.atual = self.switches[arg]
                self.atual["modo"] = "user"
                print(cr(f"Conectando a {arg}...", "bold"))
            else:
                self.comando_errado("% Host desconhecido.")
            return True
        self.comando_desconhecido(linha)
        return True

    def ac_show_version(self):
        return "\n".join([
            "DC-Corp Switch (Simulated)  --  4GB DRAM  --  IOS Educational v1.0",
            "System uptime is 0 days, 0 hours, 12 minutes",
        ])

    def jogar(self):
        motd([
            cr("Supervisora JANAINA LOPES entra na sala de treino:", "yellow"),
            cr('"Estagiario, primeiro dia e a gente ja testa o cabelo de quem quer', "magenta"),
            cr('  virar gente na infra. A rede do andar 15 caiu: as VLANs sumiram', "magenta"),
            cr('  dos switches. O Valente ta nervoso. Conecta no SW-01 e resolve."', "magenta"),
            cr('"Se travar, o DETONADO do jogo tem o passo a passo. Vai, mostra servico."', "magenta"),
        ])
        print()
        self.atual = self.switches["SW-01"]
        print(cr("Voce esta no terminal do SW-01. Digite help para os comandos.", "green"))
        print()
        while True:
            linha = ler(self.prompt() + " ")
            if linha == "eof":
                break
            if not linha:
                continue
            if not self.processar(linha):
                break
            if self.vitoria():
                self.fim_da_missao()
                return

    def fim_da_missao(self):
        m = MISSOES["m1"]
        self.jogo.missoes["m1"] = "concluida"
        self.jogo.ganha_xp(m["recompensa"], "missao concluida")
        print()
        print(cr("=" * 60, "green"))
        print(cr("           MISSAO CUMPRIDA - DC CORP", "green"))
        print(cr("=" * 60, "green"))
        print()
        print(cr('Janaina: "Olha so. Primeiro dia, rede do 15 de volta.', "magenta"))
        print(cr('  True profissional e assim: resolve sem aviaozinho de papel.', "magenta"))
        print(cr('  O Valente ja ficou sabendo. Daqui a pouco voce ouve o berro dele... de felicidade."', "magenta"))
        print()
        print(cr("Capitulo 1 concluido! Clima de fim de expediente.", "cyan"))
        print(cr("(Proximo capitulo: 'Unindo os Andares' - trunk entre switches)", "dim"))


def objetivo_da_missao(jogo, mid):
    m = MISSOES[mid]
    return "\n".join([
        cr(f"== CAPITULO {m['capitulo']}: {m['titulo']} ==", "bold"),
        f"  {m['ambientacao']}",
        cr(f"  OBJETIVO: {m['objetivo']}", "cyan"),
        f"  Recompensa: {m['recompensa']} XP",
        "",
        cr("  (Detalhes passo a passo: digite  detonado)", "dim"),
    ])


# ---------------------------------------------------------------------------
# CENTRAL DE OPERACOES (hub do jogo)
# ---------------------------------------------------------------------------

BANNER = r"""
   __________  ____  ______    ____     _____
  / __/  _/  |/  / / __/ /   / __/    / ___/
 / _// / / /|_/ / / _// /__ / _/     / /__
/___/___/_/  /_/ /___/____/___/      \___/

       SISTEMA DE TREINAMENTO E PROGRESSAO
"""


def central(jogo):
    print(cr(BANNER, "cyan"))
    if INTERATIVO:
        motd([
            "",
            (cr("[ Dia 1, 08h00 - DC Corp, andar 1 ]", "yellow")),
            "Voce e o estagiario mais novo da maior distribuidora de bobagem do ramo.",
            "A Supervisora Janaina Lopes apontou pra tua cadeira e disse:",
            (cr('"Bem-vindo a civilizacao, estagiario. Ta tudo no DETONADO. Nao erre feito besta."', "magenta")),
            "",
        ])
    while True:
        print()
        print(cr("   ============  CENTRAL DE OPERACOES  ============", "bold"))
        print("   1) Iniciar capitulo atual")
        print("   2) Mapa de missoes (todos os capitulos)")
        print("   3) Detonado (guia passo a passo)")
        print("   4) Perfil (nivel, XP, cargo)")
        print("   5) Sair")
        print(cr("   ===============================================", "dim"))
        escolha = ler("  > ").strip()
        if escolha == "eof":
            break
        if escolha == "1":
            if "m1" not in jogo.missoes:
                print()
                Missao1(jogo).jogar()
            else:
                print(cr("Capitulo 1 ja concluido!", "green"))
                print(cr("Cap.2 'Unindo os Andares' esta EM CONSTRUCAO no jogo (veja o detonado).", "yellow"))
        elif escolha == "2":
            print()
            print(mapa_missoes(jogo))
        elif escolha == "3":
            print()
            print(mostrar_detonado(jogo))
        elif escolha == "4":
            print()
            print(jogo.status_perfil())
        elif escolha == "5":
            break
        elif escolha.startswith("detonado"):
            partes = escolha.split()
            cap = None
            if len(partes) > 1:
                try:
                    cap = int(partes[1])
                except ValueError:
                    cap = None
            print()
            print(mostrar_detonado(jogo, cap))
        elif escolha in ("missoes", "mapa"):
            print()
            print(mapa_missoes(jogo))
        elif escolha in ("perfil", "ficha"):
            print()
            print(jogo.status_perfil())
        else:
            print(cr("Comando nao reconhecido. Use os numeros 1 a 5.", "red"))


def main():
    jogo = Personagem()
    try:
        central(jogo)
    except KeyboardInterrupt:
        print()
        print(cr("Conexao encerrada. O Valente ja vai ouvir sobre isso.", "dim"))
    print()
    print(cr("Sessao encerrada. A DC Corp agradece. Volte sempre, estagiario.", "dim"))


if __name__ == "__main__":
    main()
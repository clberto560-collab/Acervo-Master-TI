# -*- coding: utf-8 -*-
"""DC CORP - RPG TECNOLOGICO (prototipo)

Voce entra na DC Corp como estagiario de infra e evolui de cargo realizando
missoes de TI reais em terminais simulados. Cada missao ensina um pilar:
VLAN, trunk, switch, roteamento, firewall, analise de trafego, defesa...

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


def motd(linhas, delay=0.012):
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
# PROGRESSAO DO PERSONAGEM
# ---------------------------------------------------------------------------

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
        self.missoes = {}

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
        linhas.append(f"  Missoes feitas : {len(concluidas)}/{len(MISSOES)}")
        linhas.append(f"  No terminal   : {self.acertos} acertos / {self.erros} erros")
        return "\n".join(linhas)


# ---------------------------------------------------------------------------
# CATALOGO DE MISSOES
# ---------------------------------------------------------------------------

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
        "aprender": "VLAN basica, modos do IOS e a rotina de salvar config (write memory).",
        "recompensa": 300,
        "cena_intro": [
            'Supervisora JANAINA LOPES entra na sala de treino:',
            '"Estagiario, primeiro dia e a gente ja testa o cabelo de quem quer',
            '  virar gente na infra. A rede do andar 15 caiu: as VLANs sumiram',
            '  dos switches. O Valente ta nervoso. Conecta no SW-01 e resolve."',
            '"Se travar, o DETONADO do jogo tem o passo a passo. Vai, mostra servico."',
        ],
        "guia": [
            "1) No terminal, suba de nivel: digite  enable",
            "2) Confira o estado atual:  show vlan brief   (repare: NAO existe VLAN 10)",
            "3) Entre na configuracao global:  configure terminal",
            "4) Crie a VLAN 10:  vlan 10",
            "5) Nomeie a VLAN:  name TI",
            "6) Volte e salve:  end  e depois  write memory",
            "7) Troque de equipamento:  conectar SW-02",
            "8) Repita os passos 1 a 6 no SW-02",
            "9) Confira:  show vlan brief  nos dois deve listar a VLAN 10 como TI",
            "10) Travou? digite  dica  dentro do terminal.",
        ],
    },
    "m2": {
        "id": "m2",
        "capitulo": 2,
        "titulo": "Unindo os Andares",
        "estado": 1,
        "lv": 2,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "Andar 14 e 15 viram ilhas: nenhum trunk liga os switches.",
        "objetivo": "Criar a VLAN 20 (RH) nos dois switches e configurar trunk 802.1Q na porta fa0/24 liberando apenas as VLANs 10 e 20.",
        "aprender": "Trunk 802.1Q, interface de uplink e limitacao de VLANs no trunk.",
        "recompensa": 450,
        "cena_intro": [
            "Supervisora JANAINA bate na mesa:",
            '"Rapaz, o andar 14 e o 15 viraram ilhas. Nenhum trunk ligando',
            '  os switches, e o pessoal do RH anda sem rede. Bora parar de',
            '  girar na maionese."',
            '"Cria a VLAN 20 do RH nos dois switches, configura a porta fa0/24',
            '  como trunk e libera SO as vlans 10 e 20 no cabo. Nem uma a mais."',
            '"E guarda isso: trunk aberto com vlan any any e porta aberta pra',
            '  ladrao. Ta ligado no que eu disse?"',
        ],
        "guia": [
            "1) No SW-01, crie a VLAN 20:  enable, configure terminal, vlan 20",
            "2) De liquente o nome:  name RH",
            "3) Volte ao modo privilegiado:  end",
            "4) Entre na interface de uplink:  configure terminal, interface fa0/24",
            "5) Transforme em trunk:  switchport mode trunk",
            "6) Libere SO as VLANs 10 e 20:  switchport trunk allowed vlan 10,20",
            "7) Salve:  end  e  write memory",
            "8) Faca o mesmo no SW-02:  conectar SW-02  e repita os passos 1-7",
            "9) Confira em cada um:  show interfaces trunk  e  show vlan brief",
            "10) Dica: dentro do terminal, digite  dica  a qualquer momento.",
        ],
    },
    "m3": {
        "id": "m3",
        "capitulo": 3,
        "titulo": "Estradas da DC Corp",
        "estado": 2,
        "lv": 3,
        "npc": "Sr. Valente (CEO)",
        "ambientacao": "Os andares viram redes separadas. Agora precisa ligar tudo com roteadores.",
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
        "aprender": "ACL (Cisco) e regras de firewall, ordem das regras e contadores.",
        "recompensa": 800,
        "guia": [
            "1) Mapear as redes envolvidas (RH, TI, Diretoria).",
            "2) Escrever ACL que nega RH -> Diretoria.",
            "3) Aplicar a ACL na interface correta (entrada ou saida).",
            "4) Permitir o resto do trafego depois da negacao.",
            "5) Verificar contadores com show access-lists.",
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
        "aprender": "DHCP (DORA, lease, pool) e DNS (resolucao, registros).",
        "recompensa": 1000,
        "guia": [
            "1) Configurar pool DHCP para cada rede.",
            "2) Apontar gateway e DNS no pool.",
            "3) Configurar registros de DNS internos.",
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
        "objetivo": "Capturar e analisar trafego da rede e encontrar o trafego suspeito.",
        "aprender": "Wireshark (filtros), nmap e identificacao de anomalias.",
        "recompensa": 1200,
        "guia": [
            "1) Escanear a rede-alvo com nmap (hosts e servicos).",
            "2) Capturar trafego com Wireshark/filtros.",
            "3) Identificar protocolos e portas suspeitas.",
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
        "aprender": "SIEM basico, coleta de logs, alertas e resposta a incidente.",
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
        "aprender": "Python + Netmiko (SSH em lote), Ansible e infra como codigo.",
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
        "npc": "Dra. Santos + Sr. Valente",
        "ambientacao": "Um teste de invasao autorizado (red team) vai tentar entrar na DC Corp. Voce defende.",
        "objetivo": "Detectar, responder e expulsar um invasor simulado antes que ele chegue aos servidores.",
        "aprender": "Ciclo de defesa: deteccao, analise, contencao, erradicacao, recuperacao.",
        "recompensa": 2400,
        "guia": [
            "1) Reconhecer os primeiros sinais (scan, brute force, movimentacao lateral).",
            "2) Conter o acesso do invasor em cada fronteira.",
            "3) Erradicar a presenca e restaurar configs.",
            "4) Entregar o relatorio final pro Valente.",
        ],
    },
}


def status_missao(jogo, mid):
    if mid in jogo.missoes:
        return 3
    return MISSOES[mid]["estado"]


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


def mapa_missoes(jogo):
    linhas = [cr("== MAPA DE MISSOES / CAPITULOS ==", "bold")]
    for m in MISSOES.values():
        st = status_missao(jogo, m["id"])
        badge = {3: cr(" CONCLUIDA ", "green"), 1: cr(" JOGAVEL ", "cyan"), 2: cr(" EM BREVE ", "dim")}[st]
        linhas.append(f"  Cap.{m['capitulo']:>2} | Lv.{m['lv']:<2} | {badge} | {m['titulo']}")
    linhas.append("")
    linhas.append(cr("Para o DETONADO de uma missao:  detonado <numero-do-capitulo>", "dim"))
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
# SIMULADOR DE TERMINAL CISCO (engine generica)
# ---------------------------------------------------------------------------

def norm_if(arg):
    a = arg.lower().replace(" ", "")
    for alias in ("fastethernet0/24", "fa0/24", "g0/24", "gigabitethernet0/24", "gi0/24"):
        if a.startswith(alias) or a == alias:
            return "fa0/24"
    if a.startswith(("fa0/", "fastethernet0/")):
        return "fa0/" + a.split("/")[-1]
    return a


class Device:
    def __init__(self, codigo, vlans_iniciais=None, interfaces=None, saved_inicial=False):
        self.codigo = codigo
        self.hostname = codigo
        self.modo = "user"
        self.ctx_vlan = None
        self.ctx_if = None
        self.vlans = vlans_iniciais if vlans_iniciais is not None else {1: "default"}
        self.interfaces = interfaces or {}
        for nome in list(self.interfaces):
            self.interfaces[norm_if(nome)] = self.interfaces.pop(nome)
        self.saved = saved_inicial

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def ordem_interfaces(self):
        return sorted(self.interfaces, key=lambda n: int(n.split("/")[1]))

    def vlan_ok(self, vid, nome):
        return self.vlans.get(vid) == nome

    def trunk_info(self):
        info = []
        for nome, itf in self.interfaces.items():
            if itf["mode"] == "trunk":
                allowed = itf["trunk_allowed"]
                info.append((nome, allowed))
        return info


def checar_missao(mid, d):
    if mid == "m1":
        return d.vlan_ok(10, "TI") and d.saved
    if mid == "m2":
        t = d.interfaces.get("fa0/24")
        ok_vlan20 = d.vlan_ok(20, "RH")
        ok_trunk = bool(t) and t["mode"] == "trunk" and t["trunk_allowed"] is not None and {10, 20} <= t["trunk_allowed"]
        return ok_vlan20 and ok_trunk and d.saved
    return False


class TerminalGame:
    def __init__(self, jogo, mid):
        m = MISSOES[mid]
        self.jogo = jogo
        self.mid = mid
        self.missao = m

        def base_interface():
            return {"mode": "access", "access_vlan": 1, "trunk_allowed": None}

        def device_vazio(cod):
            return Device(
                cod,
                vlans_iniciais={1: "default"},
                interfaces={
                    "fa0/1": base_interface(),
                    "fa0/24": base_interface(),
                },
            )

        self.devices = {"SW-01": device_vazio("SW-01"), "SW-02": device_vazio("SW-02")}
        if mid == "m2":
            for cod, d in self.devices.items():
                d.vlans = {1: "default", 10: "TI"}
                d.saved = False
        self.atual = self.devices["SW-01"]
        self.atual["modo"] = "user"

    # ---- infos de apresentacao ----

    def prompt(self):
        d = self.atual
        modos = {
            "user": f"{d.hostname}>",
            "priv": f"{d.hostname}#",
            "conf": f"{d.hostname}(config)#",
            "conf-vlan": f"{d.hostname}(config-vlan)#",
            "conf-if": f"{d.hostname}(config-if)#",
        }
        return cr(modos[d["modo"]], "cyan")

    def ver_progresso(self):
        linhas = [cr(f"== PROGRESSO DA MISSAO (capitulo {self.missao['capitulo']}) ==", "bold")]
        for cod, d in self.devices.items():
            requisitos = []
            if self.mid == "m1":
                requisitos.append("VLAN 10 = TI" if d.vlan_ok(10, "TI") else "VLAN 10: pendente")
            if self.mid == "m2":
                requisitos.append("VLAN 20 = RH" if d.vlan_ok(20, "RH") else "VLAN 20: pendente")
                t = d.interfaces.get("fa0/24")
                if t and t["mode"] == "trunk" and t["trunk_allowed"] is not None and {10, 20} <= t["trunk_allowed"]:
                    requisitos.append("trunk ok")
                else:
                    requisitos.append("trunk: pendente")
            requisitos.append("salvo" if d.saved else "NAO salvo")
            ok_tudo = checar_missao(self.mid, d)
            marca = cr("OK", "green") if ok_tudo else cr("FALTA", "yellow")
            linhas.append(f"  {d.hostname}: {marca}  (" + ", ".join(requisitos) + ")")
        concluidos = sum(1 for d in self.devices.values() if checar_missao(self.mid, d))
        linhas.append(f"  -> {concluidos}/{len(self.devices)} equipamentos prontos")
        return "\n".join(linhas)

    def dica(self):
        d = self.atual
        if d["modo"] == "user":
            return "Entre no modo privilegiado: enable"
        if self.mid == "m1":
            if not d.vlan_ok(10, "TI"):
                return "configure terminal, depois: vlan 10 e name TI"
            if not d.saved:
                return "Falta salvar este switch: write memory"
            return "Este switch esta pronto. Vai pro outro: conectar SW-02"
        if self.mid == "m2":
            if not d.vlan_ok(20, "RH"):
                return "Crie a VLAN 20 do RH: configure terminal -> vlan 20 -> name RH -> end"
            t = d.interfaces.get("fa0/24")
            if not (t and t["mode"] == "trunk"):
                return "Configure a interface de uplink: configure terminal -> interface fa0/24 -> switchport mode trunk"
            if not (t and t["trunk_allowed"] is not None and {10, 20} <= t["trunk_allowed"]):
                return "Libere so as VLANs 10 e 20 no trunk: switchport trunk allowed vlan 10,20"
            if not d.saved:
                return "Falta salvar: write memory"
            return "Este switch esta pronto. Vai pro outro: conectar SW-02"
        return "Digite help para ver comandos."

    def help_tela(self):
        d = self.atual
        if d["modo"] == "user":
            linhas = [
                cr(f"== COMANDOS DO {d.hostname} ==", "bold"),
                "  enable                          modo privilegiado",
                "  show vlan brief / running-config",
                "  show interfaces trunk / show switches",
                "  conectar SW-01|SW-02            troca de equipamento",
                "  missao / progresso / detonado / dica",
                "  help / sair",
            ]
        elif d["modo"] == "priv":
            linhas = [
                cr("== MODO PRIVILEGIADO ==", "bold"),
                "  configure terminal              modo de configuracao",
                "  show vlan brief / running-config / interfaces trunk",
                "  write memory                    salva a config",
                "  exit / end                      navegacao",
            ]
        elif d["modo"] == "conf":
            linhas = [
                cr("== CONFIGURACAO GLOBAL ==", "bold"),
                "  vlan <numero>                   cria/entra na VLAN",
                "  interface fa0/24                entra na interface",
                "  end / exit",
            ]
        elif d["modo"] == "conf-vlan":
            linhas = [
                cr(f"== VLAN {d.ctx_vlan} ==", "bold"),
                "  name <nome>                     nomeia a VLAN",
                "  exit / end                      sai",
            ]
        else:
            linhas = [
                cr(f"== INTERFACE {d.ctx_if} ==", "bold"),
                "  switchport mode trunk           vira trunk",
                "  switchport mode access          vira porta comum",
                "  switchport access vlan <n>      poe a porta na VLAN",
                "  switchport trunk allowed vlan <a>,<b>   limita VLANs",
                "  exit / end",
            ]
        return "\n".join(linhas)

    def comando_desconhecido(self, linha):
        self.jogo.erros += 1
        print(cr("% Invalid input detected at '^' marker.", "red"))
        print("   " + linha)
        if linha.split():
            print("   " + " " * len(linha.split()[0]) + "^")
        print(cr("Digite help para ver os comandos.", "dim"))

    def comando_errado(self, msg):
        self.jogo.erros += 1
        print(cr(msg, "red"))

    # ---- acoes ----

    def show_vlan_brief(self):
        d = self.atual
        linhas = ["", "VLAN Name                             Status    Ports",
                  "---- -------------------------------- --------- --------------"]
        for vid, nome in d["vlans"].items():
            portas = []
            for nome_if, itf in d["interfaces"].items():
                if itf["mode"] == "access" and itf["access_vlan"] == vid:
                    portas.append(nome_if.replace("fa", "Fa"))
            if vid == 1 and not portas:
                portas = ["Fa0/1-23"]
            linhas.append(f"{vid:<4} {nome:<32} active    " + ", ".join(portas))
        linhas.append("")
        return "\n".join(linhas)

    def show_running(self):
        d = self.atual
        partes = ["Building configuration...", "",
                  "Current configuration, " + ("[SALVA]" if d.saved else "[NAO SALVA]"), "!",
                  "hostname " + d["hostname"], "!"]
        for vid, nome in d["vlans"].items():
            partes += [f"vlan {vid}", f" name {nome}", "!"]
        for nome_if in d.ordem_interfaces():
            itf = d["interfaces"][nome_if]
            partes.append("interface " + nome_if)
            if itf["mode"] == "trunk":
                partes.append(" switchport mode trunk")
                if itf["trunk_allowed"] is not None:
                    partes.append(" switchport trunk allowed vlan " +
                                  ",".join(str(v) for v in sorted(itf["trunk_allowed"])))
            else:
                partes.append(" switchport mode access")
                partes.append(f" switchport access vlan {itf['access_vlan']}")
            partes.append("!")
        partes.append("end")
        return "\n".join(partes)

    def show_trunk(self):
        d = self.atual
        if not d.trunk_info():
            return cr("Nenhuma porta em modo trunk.", "yellow")
        linhas = ["", "Port        Mode         Encapsulation  Status        Native vlan",
                  "------      ------------ -------------  ------------- -------------"]
        for nome_if, allowed in d.trunk_info():
            linhas.append(f"{nome_if:<12} on          802.1q         trunking      1")
        linhas.append("")
        linhas.append("Port        Vlans allowed on trunk")
        linhas.append("------      -----------------------")
        for nome_if, allowed in d.trunk_info():
            if allowed is None:
                linhas.append(f"{nome_if:<12} todas (perigoso!)")
            else:
                linhas.append(f"{nome_if:<12} " + ",".join(str(v) for v in sorted(allowed)))
        linhas.append("")
        return "\n".join(linhas)

    def ac_enable(self):
        d = self.atual
        if d["modo"] != "user":
            self.comando_errado("% Command not allowed in this mode.")
            return
        d["modo"] = "priv"
        print(cr("Senha de enable: ************", "dim"))
        print(cr("Enable granted.", "green"))
        self.jogo.ganha_xp(5, "modo privilegiado")

    def ac_conf_t(self):
        d = self.atual
        if d["modo"] != "priv":
            self.comando_errado("% Command not allowed in this mode.")
            return
        d["modo"] = "conf"
        print("Entrando no modo de configuracao global...")

    def ac_vlan(self, arg):
        d = self.atual
        if d["modo"] != "conf":
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
        d["ctx_vlan"] = vid
        d["modo"] = "conf-vlan"
        d["vlans"].setdefault(vid, "")
        print(cr(f"Configurando a VLAN {vid}...", "bold"))
        self.jogo.ganha_xp(15, f"vlan {vid} criada em {d.hostname}")

    def ac_name(self, arg):
        d = self.atual
        if d["modo"] != "conf-vlan":
            self.comando_errado("% Command not allowed in this mode.")
            return
        if not arg or len(arg) > 32:
            self.comando_errado("% Invalid name.")
            return
        vid = d["ctx_vlan"]
        d["vlans"][vid] = arg
        alvo = (10, "TI") if self.mid == "m1" else (20, "RH") if self.mid == "m2" else (vid, arg.upper())
        self.jogo.ganha_xp(30 if alvo[1] == arg.upper() else 5, f"vlan {vid} nomeada {arg}")
        if self.mid == "m1" and vid == 10 and arg.upper() != "TI":
            print(cr("(hmm, o departamento pediu o nome certo... a Janaina vai reparar)", "dim"))

    def ac_interface(self, arg):
        d = self.atual
        if d["modo"] != "conf":
            self.comando_errado("% interface is only allowed in configuration mode.")
            return
        nome = norm_if(arg)
        if nome not in d["interfaces"]:
            d["interfaces"][nome] = {"mode": "access", "access_vlan": 1, "trunk_allowed": None}
            print(cr(f"(criando interface {nome} no simulador)", "dim"))
        d["ctx_if"] = nome
        d["modo"] = "conf-if"
        print(f"Entrando na interface {nome}...")

    def ac_switchport(self, arg_resto):
        d = self.atual
        if d["modo"] != "conf-if":
            self.comando_errado("% switchport is only allowed inside an interface.")
            return
        nome = d["ctx_if"]
        itf = d["interfaces"][nome]
        partes = arg_resto.lower().split()
        if not partes:
            self.comando_errado("% Incomplete command.")
            return
        if partes[0] == "mode":
            if len(partes) < 2:
                self.comando_errado("% Incomplete command.")
                return
            modo = partes[1]
            if modo == "trunk":
                itf["mode"] = "trunk"
                if itf.get("trunk_allowed") is None:
                    itf["trunk_allowed"] = set()
                self.jogo.ganha_xp(20, f"{nome} virou trunk")
                print(cr("Porta agora e trunk. (cuidado: trunk liberado vaza VLANs!)", "yellow"))
            elif modo == "access":
                itf["mode"] = "access"
                itf["access_vlan"] = 1
                self.jogo.ganha_xp(5, f"{nome} virou access")
            else:
                self.comando_errado("% Invalid mode. Use: trunk ou access")
            return
        if partes[0] == "access":
            if len(partes) == 3 and partes[1] == "vlan":
                try:
                    itf["access_vlan"] = int(partes[2])
                    self.jogo.ganha_xp(5, f"{nome} na vlan {partes[2]}")
                except ValueError:
                    self.comando_errado("% Invalid vlan number.")
            else:
                self.comando_errado("% Use: switchport access vlan <numero>")
            return
        if partes[0] == "trunk":
            if len(partes) >= 4 and partes[1] == "allowed" and partes[2] == "vlan":
                try:
                    vlans = {int(v) for v in partes[3].split(",") if v}
                except ValueError:
                    self.comando_errado("% Invalid vlan list.")
                    return
                itf["trunk_allowed"] = vlans
                self.jogo.ganha_xp(25, f"trunk liberado para: {sorted(vlans)}")
            else:
                self.comando_errado("% Use: switchport trunk allowed vlan <a>,<b>")
            return
        self.comando_errado("% Invalid switchport command.")

    def ac_write(self):
        d = self.atual
        if d["modo"] == "user":
            self.comando_errado("% Command not allowed in this mode.")
            return
        d["saved"] = True
        print(cr("Building configuration on " + d.hostname + "...", "bold"))
        print(cr("[OK]", "green"))
        self.jogo.ganha_xp(25, f"config salva no {d.hostname}")

    def ir_para(self, cod):
        if cod in self.devices:
            d = self.devices[cod]
            d["modo"] = "user"
            d["ctx_vlan"] = None
            d["ctx_if"] = None
            self.atual = d
            print(cr(f"Conectando a {cod} via SSH...", "bold"))
            print(cr("Autenticacao bem-sucedida.", "green"))
        else:
            self.comando_errado("% Host desconhecido. Use: conectar SW-01 ou SW-02")

    # ---- loop ----

    def jogar(self):
        print()
        motd([(linha, "magenta") for linha in self.missao["cena_intro"]])
        print()
        print(cr("Voce esta no terminal do SW-01. Digite help para os comandos.", "green"))
        print()
        while True:
            linha = ler(self.prompt() + " ")
            if linha in ("eof",):
                break
            if not linha:
                continue
            partes = linha.split()
            cmd = partes[0].lower()
            arg = partes[1] if len(partes) > 1 else ""
            arg_resto = " ".join(partes[1:])

            if cmd in ("sair", "quit"):
                break
            if cmd == "help":
                print(self.help_tela())
            elif cmd == "missao":
                print(objetivo_da_missao(self.jogo, self.mid))
            elif cmd == "progresso":
                print(self.ver_progresso())
            elif cmd == "detonado":
                print(mostrar_detonado(self.jogo, self.missao["capitulo"]))
            elif cmd == "dica":
                print(self.dica())
            elif cmd == "show":
                if arg == "vlan":
                    print(self.show_vlan_brief())
                elif arg == "running-config":
                    print(self.show_running())
                elif arg == "interfaces" and partes[2:3] == ["trunk"]:
                    print(self.show_trunk())
                elif arg == "trunk":
                    print(self.show_trunk())
                elif arg == "switches":
                    print(self.ver_switches())
                else:
                    self.comando_desconhecido(linha)
            elif cmd == "enable":
                self.ac_enable()
            elif cmd == "configure":
                if arg in ("terminal", "t"):
                    self.ac_conf_t()
                else:
                    self.comando_errado("% Incomplete command. (configure terminal)")
            elif cmd in ("conf", "config"):
                self.ac_conf_t() if arg in ("t", "terminal") else self.comando_errado("% Use configure terminal.")
            elif cmd == "vlan":
                self.ac_vlan(arg)
            elif cmd == "name":
                self.ac_name(arg_resto)
            elif cmd == "interface":
                self.ac_interface(arg)
            elif cmd == "int":
                self.ac_interface(arg)
            elif cmd == "switchport":
                self.ac_switchport(arg_resto)
            elif cmd == "write":
                if arg in ("memory", "mem"):
                    self.ac_write()
                else:
                    self.comando_errado("% Incomplete command. (write memory)")
            elif cmd in ("wr", "save"):
                self.ac_write()
            elif cmd == "end":
                d = self.atual
                d["ctx_vlan"] = None
                d["ctx_if"] = None
                d["modo"] = "priv"
            elif cmd == "exit":
                d = self.atual
                if d["modo"] == "conf-vlan":
                    d["ctx_vlan"] = None
                    d["modo"] = "conf"
                elif d["modo"] == "conf-if":
                    d["ctx_if"] = None
                    d["modo"] = "conf"
                elif d["modo"] == "conf":
                    d["modo"] = "priv"
                elif d["modo"] == "priv":
                    d["modo"] = "user"
                else:
                    print(cr("% exit not allowed in user mode.", "yellow"))
            elif cmd == "conectar":
                self.ir_para(arg)
            else:
                self.comando_desconhecido(linha)

            if self.venceu():
                self.fim_da_missao()
                return

    def ver_switches(self):
        linhas = [cr("Switches ligados:", "bold")]
        for cod, d in self.devices.items():
            ok = checar_missao(self.mid, d)
            linhas.append(f"  {cr(cod, 'green')}  {cr('PRONTO', 'green') if ok else cr('FALTA', 'yellow')}")
        return "\n".join(linhas)

    def venceu(self):
        return all(checar_missao(self.mid, d) for d in self.devices.values())

    def fim_da_missao(self):
        m = self.missao
        self.jogo.missoes[self.mid] = "concluida"
        self.jogo.ganha_xp(m["recompensa"], "missao concluida")
        print()
        print(cr("=" * 60, "green"))
        print(cr(f"   MISSAO CUMPRIDA  -  DC CORP  (capitulo {m['capitulo']})", "green"))
        print(cr("=" * 60, "green"))
        print()
        if self.mid == "m1":
            print(cr('Janaina: "Olha so. Primeiro dia, rede do 15 de volta.', "magenta"))
            print(cr('  O Valente ja ficou sabendo e mandou um selinho de aprovacao.', "magenta"))
            print(cr('  Amanha juntamos os andares. Vai janta, estagiario."', "magenta"))
        elif self.mid == "m2":
            print(cr('Janaina: "Trunk configurado, VLAN 20 do RH no ar, e liberdade com', "magenta"))
            print(cr('  limite. Assim que se faz. O Valente quer te ver."', "magenta"))
            print(cr('  (Ele nunca quer ver ninguem. Cuidado.)', "dim"))
        print()
        print(cr("Voltando a central de operacoes...", "dim"))


# ---------------------------------------------------------------------------
# CENTRAL DE OPERACOES
# ---------------------------------------------------------------------------

BANNER = r"""
   __________  ____  ______    ____     _____
  / __/  _/  |/  / / __/ /   / __/    / ___/
 / _// / / /|_/ / / _// /__ / _/     / /__
/___/___/_/  /_/ /___/____/___/      \___/

       SISTEMA DE TREINAMENTO E PROGRESSAO
"""


def proxima_missao(jogo):
    for m in MISSOES.values():
        if m["id"] not in jogo.missoes and m["estado"] == 1:
            return m["id"]
    return None


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
        atual = proxima_missao(jogo)
        if atual is None:
            print()
            print(cr("Todas as missoes disponiveis foram concluidas!", "green"))
            print(cr("(Proximos capitulos entram na proxima atualizacao do jogo.)", "dim"))
        print()
        print(cr("   ============  CENTRAL DE OPERACOES  ============", "bold"))
        print("   1) Iniciar proxima missao" + (f"  [{MISSOES[atual]['titulo']}]" if atual else ""))
        print("   2) Mapa de missoes (todos os capitulos)")
        print("   3) Detonado (guia passo a passo)")
        print("   4) Perfil (nivel, XP, cargo)")
        print("   5) Sair")
        print(cr("   ===============================================", "dim"))
        escolha = ler("  > ").strip()
        if escolha == "eof":
            break
        if escolha == "1":
            if atual:
                TerminalGame(jogo, atual).jogar()
            else:
                print(cr("Nenhuma missao disponivel agora. Fim de expediente.", "yellow"))
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
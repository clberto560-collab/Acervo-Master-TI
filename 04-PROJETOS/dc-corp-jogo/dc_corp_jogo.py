# -*- coding: utf-8 -*-
"""DC Corp - Dia 1: Restaure a Rede do Andar 15 (protótipo jogável).

Você é o novo técnico de TI da DC Corp. No primeiro dia, a rede do andar 15
caiu: as VLANs sumiram das configurações dos switches. Sua missão é recriar
a VLAN 10 (TI) nos dois switches e salvar as configurações, usando a CLI
Cisco simulada — os mesmos comandos usados em equipamentos reais.

Como jogar: python dc_corp_jogo.py
Comandos no momento: help, dica, missao, conectar, sair
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


def motd(linhas, delay=0.05):
    if not INTERATIVO:
        for linha in linhas:
            print(linha)
        return
    for linha in linhas:
        print(linha)
        time.sleep(delay)


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


class Jogo:
    def __init__(self):
        self.switches = {"SW-01": novo_switch("SW-01"), "SW-02": novo_switch("SW-02")}
        self.atual = None          # switch conectado (None = hub)
        self.xp = 0
        self.erros = 0
        self.acertos = 0
        self.comandos_usados = set()
        self.range_ip = 29

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
        linhas = []
        linhas.append(cr("Diagrama up/ativo dos switches do andar 15:", "bold"))
        for cod, s in self.switches.items():
            v10 = "VLAN 10: TI" if s["vlan10_ok"] else "VLAN 10: AUSENTE"
            save = "salvo" if s["saved"] else "nao salvo"
            linhas.append(f"  {cr(cod, 'green')} | {v10} | config {cr(save, 'yellow')}")
        return "\n".join(linhas)

    def vitoria(self):
        return all(
            s["vlan10_ok"] and s["saved"] for s in self.switches.values()
        )

    def ganha_xp(self, pontos, motivo):
        self.xp += pontos
        self.acertos += 1
        print(cr(f"   [+{pontos} XP] {motivo}", "green"))

    def comando_desconhecido(self, cmd):
        self.erros += 1
        print(cr("% Invalid input detected at '^' marker.", "red"))
        print("   " + cmd)
        print("   " + " " * (len(cmd.split()[0]) if cmd.split() else 0) + "^")
        print(cr("Digite help para ver os comandos disponiveis.", "dim"))

    def comando_errado(self, msg):
        self.erros += 1
        print(cr(msg, "red"))

    def help_switch(self):
        s = self.atual
        base = [
            cr("== COMANDOS DO " + s["hostname"] + " ==", "bold"),
            "  enable                          entra no modo privilegiado",
            "  show vlan brief                 mostra as VLANs do switch",
            "  show running-config             mostra a configuracao atual",
            "  conectar SW-01|SW-02            troca de equipamento",
            "  missao / dica                   objetivo e pista",
            "  help / sair                     ajuda / encerra",
        ]
        if s["modo"] == "priv":
            base.insert(2, "  configure terminal (conf t)     entra no modo de configuracao")
            base.append("  exit / end                      desce um nivel / volta ao modo privilegiado")
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

    def help_hub(self):
        return "\n".join(
            [
                cr("== CENTRO DE OPERACOES DC CORP ==", "bold"),
                "  conectar SW-01 / SW-02     abre o terminal do switch",
                "  missao                      lembra do objetivo",
                "  help / sair                 ajuda / encerra",
            ]
        )

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

    # ---------- acoes do switch ----------

    def ac_show_vlan(self):
        s = self.atual
        linhas = []
        linhas.append("")
        linhas.append("VLAN Name                             Status    Ports")
        linhas.append("---- -------------------------------- --------- ---------------")
        for vid, nome in s["vlans"].items():
            if vid == 1:
                linhas.append(f"{vid:<4} {nome:<32} active    Fa0/1-24")
            else:
                linhas.append(f"{vid:<4} {nome:<32} active")
        linhas.append("")
        return "\n".join(linhas)

    def ac_show_running(self):
        s = self.atual
        ativo = "saving/atualizada" if s["saved"] else "nao salva (startup-config antiga)"
        partes = [
            "Building configuration...",
            "",
            "Current configuration, " + ativo,
            "!",
            "hostname " + s["hostname"],
            "!",
        ]
        for vid, nome in s["vlans"].items():
            partes.append("vlan %d" % vid)
            partes.append(" name %s" % nome)
            partes.append("!")
        partes += [
            "interface FastEthernet 0/1",
            " switchport mode access",
            " switchport access vlan " + (str(10) if s["vlan10_ok"] else "1"),
            "!",
            "end",
        ]
        return "\n".join(partes)

    def ac_show_version(self):
        return "\n".join(
            [
                "DC-Corp Switch (Simulated)  --  4GB DRAM  --  imaged v15.2(6)E",
                "System uptime is 0 days, 0 hours, 12 minutes",
                "Running IOS: DC-Corp IOS Educational Simulator 1.0",
            ]
        )

    def ac_enable(self):
        s = self.atual
        if s["modo"] != "user":
            self.comando_errado("% Command not allowed in this mode.")
            return
        s["modo"] = "priv"
        print(cr("Senha de enable: ************", "dim"))
        print(cr("Enable granted. Bem-vindo ao modo privilegiado.", "green"))
        self.ganha_xp(5, "nivel privilegiado alcancado")

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
            self.ganha_xp(20, f"VLAN {vid} criada no {s['hostname']}")

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
            self.ganha_xp(30, f"VLAN {vid} nomeada TI no {s['hostname']}")
        elif vid == 10:
            print(cr("(o nome do departamento parece errado... TI cobra pelo nome correto)", "dim"))
        else:
            print(f"VLAN {vid} renomeada para {arg}.")

    def ac_write(self):
        s = self.atual
        if s["modo"] == "user":
            self.comando_errado("% Command not allowed in this mode.")
            return
        if s["modo"] != "priv":
            print("(salvando a partir do modo privilegiado faz mais sentido: end primeiro)")
        s["saved"] = True
        print(cr("Building configuration on " + s["hostname"] + "...", "bold"))
        print(cr("[OK]", "green"))
        self.ganha_xp(30, f"configuracao salva no {s['hostname']}")

    def ac_end(self):
        s = self.atual
        s["ctx_vlan"] = None
        s["modo"] = "priv"

    def ac_exit(self):
        s = self.atual
        if s["modo"] == "config" or s["modo"] == "conf":
            s["ctx_vlan"] = None
            s["modo"] = "priv"
        elif s["modo"] == "conf-vlan":
            s["ctx_vlan"] = None
            s["modo"] = "conf"
        elif s["modo"] == "priv":
            s["modo"] = "user"
        else:
            print(cr("Connection closed. Voltando ao centro de operacoes.", "yellow"))
            self.atual = None

    # ---------- processador de comandos ----------

    def processar_hub(self, linha):
        partes = linha.split()
        cmd = partes[0]
        arg = partes[1] if len(partes) > 1 else ""
        if cmd in ("sair", "quit", "exit"):
            return False
        if cmd == "help":
            print(self.help_hub())
            return True
        if cmd == "missao":
            print(self.missao())
            return True
        if cmd == "dica":
            print(self.dica())
            return True
        if cmd == "conectar":
            if arg not in self.switches:
                self.comando_desconhecido(linha)
                return True
            self.atual = self.switches[arg]
            self.atual["modo"] = "user"
            print(cr(f"Conectando a {arg} via SSH...", "bold"))
            print(cr("Autenticacao bem-sucedida.", "green"))
            return True
        if cmd == "show" and arg == "switches":
            print(self.ver_switches())
            return True
        self.comando_desconhecido(linha)
        return True

    def processar_switch(self, linha):
        s = self.atual
        partes = linha.split()
        if not partes:
            return True
        cmd = partes[0].lower()
        arg = partes[1] if len(partes) > 1 else ""
        arg_resto = " ".join(partes[1:])

        self.comandos_usados.add(cmd)

        if cmd in ("sair", "quit"):
            return False
        if cmd == "help":
            print(self.help_switch())
            return True
        if cmd == "missao":
            print(self.missao())
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
            if arg == "startup-config":
                s = self.atual
                print(str(s["saved"]))
                print("Conteudo da startup-config: sda é a mais recente" if s["saved"] else "startup-config DESATUALIZADA (voce ainda nao salvou!)")
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
            if arg == "t" or arg == "terminal":
                self.ac_conf_t()
                return True
            self.comando_errado("% Do you want to enter configuration mode? -> configure terminal")
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
                print(cr(f"Conectando a {arg}...", "bold"))
            else:
                self.comando_errado("% Host desconhecido. Use: conectar SW-01 ou SW-02")
            return True
        self.comando_desconhecido(linha)
        return True

    def missao(self):
        ok = [cod for cod, s in self.switches.items() if s["vlan10_ok"] and s["saved"]]
        return "\n".join(
            [
                cr("== MISSAO: RESTAURE A VLAN 10 (TI) ==", "bold"),
                "O andar 15 ficou sem rede porque as VLANs sumiram da config.",
                "Em CADA switch (SW-01 e SW-02) voce deve:",
                "  1) criar a vlan 10   ->  vlan 10",
                "  2) nomear como TI    ->  name TI",
                "  3) salvar a config   ->  write memory",
                "",
                cr(f"Concluidos: {len(ok)}/2  (total em andamento: {self.xp} XP)", "green"),
            ]
        )

    def rodar(self):
        motd(
            [
                cr("==================================================================", "bold"),
                cr("   DC CORP  -  SIMULADOR ESTRATEGICO DE TI  v0.1  (protótipo)", "bold"),
                cr("==================================================================", "bold"),
            ]
        )
        print()
        if INTERATIVO:
            motd(
                [
                    cr("[ Dia 1 - manha ]", "yellow"),
                    "Seu primeiro dia na DC Corp. O gerente de infra, Sr. Valente, chama:",
                    cr('"Rapaz, o andar 15 ficou mudo. A rede toda caiu e as VLANs', "magenta"),
                    cr('  sumiram da configuracao dos switches. Tu entende de switch?"', "magenta"),
                    cr('"- Entendo sim, senhor. Primeiro dia e ja to apagando incendio."', "blue"),
                    cr('"Entao usa o SSH nos switches SW-01 e SW-02 e resolve logo. TI nao pode', "magenta"),
                    cr('  parar, menino. Sem TI nao existe DC Corp."', "magenta"),
                ],
                0.015,
            )
            print()
            try:
                input(cr("  [Enter] para assumir o posto no terminal...", "dim"))
            except EOFError:
                return
        else:
            motd(
                [
                    cr("[ Modo nao-interativo detectado ]", "dim"),
                    cr("[ Initializing SW-01 terminal... ]", "dim"),
                ]
            )
        self.atual = self.switches["SW-01"]
        print(cr("Voce esta no terminal do SW-01. Digite help para ver os comandos.", "green"))
        print()
        try:
            while True:
                try:
                    linha = input(self.prompt() + " ").strip()
                except EOFError:
                    return
                if not linha:
                    continue
                if self.atual is None:
                    continuar = self.processar_hub(linha)
                else:
                    continuar = self.processar_switch(linha)
                if not continuar:
                    break
                if self.vitoria():
                    self.fim_de_jogo()
                    return
        except KeyboardInterrupt:
            print()
            print(cr("(Ctrl+C) O Sr. Valente grunhiu e voltou para a sala dele.", "dim"))

    def fim_de_jogo(self):
        self.xp += 100
        print()
        print(cr("==================================================================", "bold"))
        print(cr("                MISSAO CUMPRIDA  -  DC CORP", "green",))
        print(cr("==================================================================", "bold"))
        print()
        qtd = self.xp
        if self.erros == 0:
            nota = "S+"
        elif self.erros <= 3:
            nota = "A"
        elif self.erros <= 7:
            nota = "B"
        else:
            nota = "C+"
        print(f"  XP total:        {qtd}")
        print(f"  Comandos usados: {len(self.comandos_usados)} diferentes")
        print(f"  Erros de comando:{self.erros}")
        print(f"  Avaliacao do Sr. Valente: {cr(nota, 'yellow')}")
        print()
        print(cr('Sr. Valente: "Hehe, primeiro dia e ja resolveu a rede do 15."', "magenta"))
        print(cr('            "Guarda isso, menino: TI e resolver problema dos outros,', "magenta"))
        print(cr('             antes que eles descubram que da pra resolver sozinho."', "magenta"))
        print()
        print(cr("Proximo passo (proximos niveis): VLAN entre 2 switches, ACL,", "dim"))
        print(cr("DHCP, depois pfSense, Zabbix e defesa cibernetica...", "dim"))
        print(cr("DC CORP - nivel desbloqueado: 'Estagiario que salvou a sexta-feira'.", "cyan"))


def main():
    jogo = Jogo()
    try:
        jogo.rodar()
    except KeyboardInterrupt:
        print()
        print(cr("Sessao encerrada.", "dim"))
    print(cr("Sessao de treino encerrada. A DC Corp agradece.", "dim"))


if __name__ == "__main__":
    main()
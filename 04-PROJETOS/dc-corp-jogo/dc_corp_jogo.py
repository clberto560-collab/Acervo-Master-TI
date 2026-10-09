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

import json
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

ARQ_SAVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_dc_corp.json")


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
    def __init__(self, nome="Cleber"):
        self.nome = nome
        self.xp = 0
        self.acertos = 0
        self.erros = 0
        self.missoes = {}

    def salvar(self):
        try:
            dados = {
                "nome": self.nome,
                "xp": self.xp,
                "acertos": self.acertos,
                "erros": self.erros,
                "missoes": self.missoes,
            }
            with open(ARQ_SAVE, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    @staticmethod
    def carregar():
        if not os.path.exists(ARQ_SAVE):
            return Personagem()
        try:
            with open(ARQ_SAVE, "r", encoding="utf-8") as f:
                dados = json.load(f)
            p = Personagem(dados.get("nome", "Cleber"))
            p.xp = int(dados.get("xp", 0))
            p.acertos = int(dados.get("acertos", 0))
            p.erros = int(dados.get("erros", 0))
            p.missoes = dados.get("missoes", {})
            return p
        except (OSError, ValueError, KeyError):
            return Personagem()

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
        "estado": 1,
        "lv": 3,
        "npc": "Sr. Valente (CEO)",
        "ambientacao": "Os andares viram redes separadas. Agora precisa ligar tudo com roteadores.",
        "objetivo": "Configurar roteamento estatico entre redes e NAT para a Internet.",
        "aprender": "Tabela de rotas, rota estatica, default route e NAT/PAT.",
        "recompensa": 600,
        "cena_intro": [
            "O Sr. VALENTE chama na sala. Videochamada mentirinha:",
            '"Rapaz. A DC Corp tem rede interna, mas o povo ainda usa pendrive',
            '  pra passar relatorio de um andar pro outro. Eu nao pago o Provedor',
            '  pra isso, nao ta certo isso."',
            '"Chegou o EQUIPINHO da sorte (um roteador RT-01). Teu trabalho:',
            '  configurar esse trem (valendo wow) e fazer a rede 192.168.10.0',
            '  falar com o mundo em 8.8.8.8. Nenhum IP vazando, hein. Traduz isso."',
        ],
        "guia": [
            "1) No RT-01:  enable",
            "2) LAN: configure terminal -> interface fa0/0 -> ip address 192.168.10.1 255.255.255.0 -> no shutdown",
            "3) WAN/Provedor: interface fa0/1 -> ip address 200.100.50.2 255.255.255.252 -> no shutdown",
            "4) Saida pro mundo: (config) -> ip route 0.0.0.0 0.0.0.0 200.100.50.1",
            "5) Marque os lados do NAT: em fa0/0 digite ip nat inside; em fa0/1, ip nat outside",
            "6) Libere a rede interna: access-list 1 permit 192.168.10.0 0.0.0.255",
            "7) Traduza tudo: ip nat inside source list 1 interface fa0/1 overload",
            "8) Salve: end -> write memory",
            "9) Prove que ta no mundo:  ping 8.8.8.8  (tem que dar 4/4)",
            "10) Diagnostico se travar:  show ip route  e  show ip nat translations  |  progresso  |  dica",
        ],
    },
    "m4": {
        "id": "m4",
        "capitulo": 4,
        "titulo": "O Muro da Empresa",
        "estado": 1,
        "lv": 4,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "O financeiro descobriu que o RH acessa os servidores da diretoria. Briga feia.",
        "objetivo": "Criar regras de firewall: bloquear a VLAN do RH de acessar a rede da diretoria.",
        "aprender": "ACL (Cisco) e regras de firewall, ordem das regras e contadores.",
        "recompensa": 800,
        "cena_intro": [
            "Supervisora JANAINA fecha a cara:",
            '"Rapaz, coisa feia. O Financeiro pegou o estagiario do RH',
            '  bisbilhotando os servidores da Diretoria (rede 192.168.10.0).',
            '  Briga que tu nao quer ver."',
            '"O roteador RT-01 ja ta de pe: de um lado o RH (fa0/1,',
            '  192.168.20.0), do outro a Diretoria (fa0/0, 192.168.10.0).',
            '  Teu role: escrever uma ACL que TRANCA o RH na Diretoria, mas',
            '  deixa o TI navegar normal. E sem esquecer a ordem das regras."',
        ],
        "guia": [
            "1) No RT-01:  enable",
            "2) Crie a lista de acesso 100:  configure terminal",
            "3) REGRAS NA ORDEM CERTA (a 1a que bate vale):",
            "   a) Barre o RH na Diretoria:  access-list 100 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255",
            "   b) Deixe TODO o resto passar:  access-list 100 permit ip any any",
            "4) Aplique na porta que recebe o RH:  interface fa0/1 -> ip access-group 100 in",
            "5) Salve:  end -> write memory",
            "6) Prove: rode  simular trafego  (RH -> Diretoria tem que ser BLOQUEADO e",
            "   TI -> Internet tem que ser LIBERADO)",
            "7) Confira os contadores:  show access-lists",
            "8) Testes:  progresso  (todos os requisitos) e  dica  se travar.",
        ],
    },
    "m5": {
        "id": "m5",
        "capitulo": 5,
        "titulo": "Trunk ou Access Trocado",
        "estado": 1,
        "lv": 5,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "Depois da festa dos trunks, alguem embaralhou os papeis: o uplink virou porta comum e o PC da sala virou trunk. Nada sobe direito.",
        "objetivo": "Corrigir o SW-01: fa0/1 como access (VLAN 10/TI), fa0/24 como trunk 802.1Q, testar o trafego e salvar.",
        "aprender": "Diferenca entre porta access e trunk no 802.1Q, e como diagnosticar porta trocada.",
        "recompensa": 1000,
        "cena_intro": [
            'Supervisora JANAINA LOPES aponta pro painel:',
            '"Estagiario, o cabeamento ta ``no seco``: o PC da sala sobe no modo',
            '  trunk e o uplink virou porta comum. Resumindo: ninguem conversa',
            '  com ninguem. Entra no SW-01 e resolve essa bagunca de layer 2."',
            '"(Dica: show interfaces trunk e show running-config entregam o erro.)"',
        ],
        "guia": [
            "1) Diagnostique:  show running-config  e  show interfaces trunk",
            "2) Repare que fa0/1 esta como trunk (errado: e porta de escritorio)",
            "3) Repare que fa0/24 esta como access (errado: e o uplink/trunk)",
            "4) Corrija fa0/24: configure terminal -> interface fa0/24 -> switchport mode trunk",
            "5) Libere a VLAN: switchport trunk allowed vlan 10",
            "6) Corrija fa0/1: interface fa0/1 -> switchport mode access -> switchport access vlan 10",
            "7) Saia e teste:  simular trafego  (PC da sala deve conectar na VLAN 10)",
            "8) Salve:  write memory",
        ],
    },
    "m6": {
        "id": "m6",
        "capitulo": 6,
        "titulo": "A VLAN Fantasma",
        "estado": 1,
        "lv": 6,
        "npc": "Supervisora Janaina Lopes",
        "ambientacao": "A VLAN 20 do RH nao atravessa o trunk, e no SHOW VLAN BRIEF do SW-02 existe uma VLAN 999 que ninguem mandou criar. Trafego fantasma perambulando.",
        "objetivo": "No SW-01 e SW-02: liberar apenas as VLANs 10 e 20 no trunk, configurar a VLAN nativa 99, exterminar a VLAN fantasma (999) e salvar tudo.",
        "aprender": "Allowed vlan no trunk, VLAN nativa (native) e caca a VLAN fantasma.",
        "recompensa": 1200,
        "cena_intro": [
            'JANAINA fecha a cara pro monitor:',
            '"O RH ta gritando que a rede nao ve mais o servidor da TI. E pior:',
            '  tem uma VLAN 999 na config do SW-02. Vtrunk de fantasma cruzando',
            '  o corredor. A limpa ela e libera so o que precisa passar."',
            '"(VLAN nativa padrao da DC: 99. Ah, e confere os DOIS switches.)"',
        ],
        "guia": [
            "1) Diagnostique a porta trunk nos dois:  show interfaces trunk",
            "2) Perceba: a VLAN 20 NAO esta no allowed vlan, e a 999 esta.",
            "3) Corrija o trunk (nos dois switches): interface fa0/24 -> switchport trunk allowed vlan 10,20",
            "4) Ajuste a VLAN nativa: switchport trunk native vlan 99",
            "5) Extermine a fantasma no SW-02: configure terminal -> no vlan 999",
            "6) Teste o trafego:  simular trafego  em cada equipamento",
            "7) Salve:  write memory  em cada um",
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
    linhas.append(cr("Para a JORNADA completa do Acervo (tema -> topicos):  trilha", "dim"))
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# JORNADA DE APRENDIZADO (espelha o Acervo Master TI)
# ---------------------------------------------------------------------------
# Cada "tema" e um mundo (fase da empresa); cada topico e uma trilha de
# MISSOES. Uma missao tem "id" (usado pela engine), "titulo" e "situacao".
# ids "m1".."m9" = missoes com engine (JOGAVEL/CONCLUIDA); ids novos sem
# engine (ex: "r1-1") sao o roadmap -> EM BREVE. "requer" = pre-requisito:
# voce so destrava o proximo topico (e a proxima fase da empresa) com a base.
# Cada trilha puxa a proxima: a DC Corp cresce na ordem abaixo.

def _mis(seq):
    return [{"id": i, "titulo": t, "situacao": s} for i, t, s in seq]

TRILHA = [
    {
        "tema": "Redes",
        "fase": "O estagiario ressuscita a rede velha da DC Corp, andar por andar.",
        "topicos": [
            {"nome": "Modelo OSI", "horas": 8, "requer": [],
             "missoes": _mis([
                 ("r1-1", "O cabo no lugar errado", "um andar inteiro nao comunica: achar em qual camada o problema mora"),
                 ("r1-2", "A culpa e de quem", "navega na web mas nao chega no servidor interno: separar as camadas"),
                 ("r1-3", "Checklist de camadas", "usar as 7 camadas como roteiro de diagnostico"),
             ])},
            {"nome": "Protocolo TCP/IP", "horas": 8, "requer": ["Modelo OSI"],
             "missoes": _mis([
                 ("r2-1", "TCP ou UDP?", "o streaming da recepcao trava: escolher o transporte certo para cada servico"),
                 ("r2-2", "Os tres apertos", "conexao que nao abre: entender o handshake SYN/ACK no terminal"),
                 ("r2-3", "Mapa de portas", "mapear quais servicos e portas a DC Corp usa"),
             ])},
            {"nome": "Protocolo IPv4 e Classes", "horas": 6, "requer": ["Protocolo TCP/IP"],
             "missoes": _mis([
                 ("r3-1", "Enderecos sem padrao", "organizar os IPs da empresa por classe (A, B, C)"),
                 ("r3-2", "O IP repetido", "duas maquinas com o mesmo endereco: resolver o conflito"),
                 ("r3-3", "Rede, host ou gateway?", "decidir quando a resposta e local ou vai para o default gateway"),
             ])},
            {"nome": "IPv4: Sub-Redes, VLSM e CIDR", "horas": 12, "requer": ["Protocolo IPv4 e Classes"],
             "missoes": _mis([
                 ("r4-1", "Dividindo em pedacinhos", "quebrar a rede da Diretoria em sub-redes de tamanhos iguais"),
                 ("r4-2", "VLSM na mao", "sub-redes sob medida, cada setor com o tamanho certo"),
                 ("r4-3", "CIDR na pratica", "enxugar a tabela de rotas usando notacao /CIDR"),
             ])},
            {"nome": "Dispositivos e Topologias de Rede", "horas": 8, "requer": ["IPv4: Sub-Redes, VLSM e CIDR"],
             "missoes": _mis([
                 ("r5-1", "Qual equipamento resolve?", "escolher o aparelho certo (switch, roteador, AP) para cada situacao"),
                 ("r5-2", "Topologia do andar 15", "organizar estrela e malha no predio"),
                 ("r5-3", "Caminho reserva", "preparar um segundo link de emergencia para o almoxarifado"),
             ])},
            {"nome": "Clientes de Rede", "horas": 2, "requer": ["Dispositivos e Topologias de Rede"],
             "missoes": _mis([
                 ("r6-1", "O PC sem internet", "validar IP, mascara, gateway e DNS do cliente"),
                 ("r6-2", "Cliente DNS travado", "corrigir a resolucao de nomes de uma maquina"),
             ])},
            {"nome": "Protocolos e Servicos de Rede", "horas": 8, "requer": ["Protocolo TCP/IP"],
             "missoes": _mis([
                 ("r7-1", "Servicos em ordem", "subir e enxergar DHCP, DNS, HTTP e FTP na rede certa"),
                 ("r7-2", "Portas e protocolos", "liberar no firewall o servico que a firma precisa"),
                 ("r7-3", "O vizinho ARP", "resolver erros de ARP no cenario da DC"),
                 ("r7-4", "O carteiro digital", "subir DHCP (DORA, lease, pool) e DNS de verdade"),
             ])},
            {"nome": "Switches Ethernet - Parte I", "horas": 10,
             "requer": ["Dispositivos e Topologias de Rede", "Protocolos e Servicos de Rede"],
             "missoes": _mis([
                 ("m1", "VLAN na mao, porta a porta", "diagramar as VLANs da DC Corp e configurar porta por porta"),
                 ("m2", "Trunk entre os andares", "estender as VLANs entre os switches com etiqueta 802.1Q"),
                 ("m5", "Trunk ou Access Trocado", "portas embaralhadas: uplink como access e PC como trunk"),
                 ("m6", "A VLAN Fantasma", "nativa errada, allowed vlan sem a rede certa e VLAN fantasma no trunk"),
             ])},
            {"nome": "Switches Ethernet - Parte II", "horas": 10, "requer": ["Switches Ethernet - Parte I"],
             "missoes": _mis([
                 ("r9-1", "Tag e untag", "desenhar como o 802.1Q marca e desmarca os frames no trunk"),
                 ("r9-2", "VLAN permitida demais", "enxugar as allowed vlan do trunk que trafega lixo"),
                 ("r9-3", "Porta de acesso blindada", "aplicar port security nas portas de acesso"),
             ])},
            {"nome": "Protocolo Spanning Tree de A a Z", "horas": 10,
             "requer": ["Switches Ethernet - Parte II"],
             "missoes": _mis([
                 ("r10-1", "O laco fatal", "dois cabos unindo os switches formam um loop de broadcast: ativar o STP"),
                 ("r10-2", "Quem manda?", "escolher a root bridge certa da rede"),
                 ("r10-3", "Porta bloqueada de proposito", "entender os papeis das portas (root, designated, blocked)"),
             ])},
            {"nome": "Roteamento IP e RIP", "horas": 6,
             "requer": ["IPv4: Sub-Redes, VLSM e CIDR"],
             "missoes": _mis([
                 ("m3", "Estradas da DC Corp", "rotas estaticas e NAT/PAT para a empresa se comunicar"),
                 ("r11-2", "A rota sumiu", "o ping para de funcionar: achar a rota estatica errada"),
                 ("r11-3", "RIP na pratica", "subir o RIP entre os roteadores e ver as rotas aprenderem sozinhas"),
             ])},
            {"nome": "Internet - NAT, Proxy e BGP", "horas": 4,
             "requer": ["Roteamento IP e RIP"],
             "missoes": _mis([
                 ("m4", "O Muro da Empresa", "ACL e firewall controlando quem fala com quem na borda"),
                 ("r12-2", "PAT esgotando", "muitos PCs, um IP de saida: fazer o overload dar conta"),
                 ("r12-3", "Proxy na manga", "implantar proxy/cache para economizar o link"),
                 ("r12-4", "O vizinho BGP", "fazer o peering com o provedor de internet"),
             ])},
            {"nome": "Wireless LAN (Redes sem fio)", "horas": 8,
             "requer": ["Protocolos e Servicos de Rede", "Clientes de Rede"],
             "missoes": _mis([
                 ("r13-1", "Wi-Fi sem nome", "configurar SSID e seguranca do acesso sem fio"),
                 ("r13-2", "O canto sem sinal", "escolher canal e posicao dos APs para cobrir o predio"),
                 ("r13-3", "Convidado do lado de fora", "rede de visitantes isolada em VLAN proprio"),
             ])},
            {"nome": "Network Troubleshooting", "horas": 6,
             "requer": ["Protocolos e Servicos de Rede", "Roteamento IP e RIP"],
             "missoes": _mis([
                 ("r14-1", "O andar 15 caiu", "diagnostico guiado: ping, traceroute, ARP ate achar o problema"),
                 ("r14-2", "Lentidao misteriosa", "caca ao gargalo que ninguem acha"),
                 ("r14-3", "Caos documentado", "padronizar as configs para o proximo estagiario sobreviver"),
                 ("r14-4", "Espionando o trafego", "capturar trafego, filtrar e achar a anomalia"),
             ])},
        ],
    },
    {
        "tema": "Cabeamento",
        "fase": "A DC Corp cresceu: antes de equipamento novo, a casa fica arrumada.",
        "topicos": [
            {"nome": "Cabeamento Estruturado Metalico", "horas": 16, "requer": ["Modelo OSI"],
             "missoes": _mis([
                 ("c1-1", "Do rack ao patch panel", "roteirizar o cabo de cada posto ate o painel certo"),
                 ("c1-2", "Panel desorganizado", "achar e patchar o ponto fisico certo de cada sala"),
                 ("c1-3", "Norma em dia", "escolher o cabo certo (CAT5e/6) e respeitando a norma"),
             ])},
            {"nome": "Cabeamento Estruturado Fibra", "horas": 16,
             "requer": ["Cabeamento Estruturado Metalico"],
             "missoes": _mis([
                 ("c2-1", "Fibra entre predios", "subir o backbone de fibra ligando os dois predios"),
                 ("c2-2", "Emendas e conectores", "emendar e conectar a fibra no ponto certo"),
                 ("c2-3", "Padrao TIA/ANSI", "organizar o projeto segundo a norma de infraestrutura"),
             ])},
            {"nome": "Cabeamento Profissional", "horas": 24, "requer": ["Cabeamento Estruturado Fibra"],
             "missoes": _mis([
                 ("c3-1", "A casa de cabos perfeita", "organizar racks, dutos e identificacao do DSO"),
                 ("c3-2", "A arte do patch", "padrao de cores e criado-cruzado sob controle"),
                 ("c3-3", "Caminho limpo", "evitar interferencia e entupimento nos caminhos de cabos"),
             ])},
            {"nome": "Cabeamento - Gestao de Equipe", "horas": 16, "requer": ["Cabeamento Profissional"],
             "missoes": _mis([
                 ("c4-1", "Time no ritmo", "dividir a obra entre os pontos e prazos"),
                 ("c4-2", "O ponto perdido", "liderar a busca do ponto errado sem estourar o prazo"),
                 ("c4-3", "Padrao pra equipe", "criar um procedimento que ate o novato segue"),
             ])},
            {"nome": "Certificacao de Enlaces em Par Metalico", "horas": 16,
             "requer": ["Cabeamento Estruturado Metalico"],
             "missoes": _mis([
                 ("c5-1", "O testador acusou", "enlace que nao certifica: crosstalk e comprimento fora"),
                 ("c5-2", "Lendo o relatorio", "interpretar o laudo do certificador de par metalico"),
                 ("c5-3", "Do FAIL ao PASS", "corrigir o que reprovou e re-testar ate certificar"),
             ])},
            {"nome": "Cabos de Fibra Optica (caracteristicas)", "horas": 16,
             "requer": ["Cabeamento Estruturado Fibra"],
             "missoes": _mis([
                 ("c6-1", "Monomodo ou multimodo?", "escolher a fibra certa para cada distancia"),
                 ("c6-2", "Conectores e cores", "identificar LC/SC e os padroes de cor dos conectores"),
                 ("c6-3", "Perda que faz sentido", "entender atenuacao em dB por quilometro"),
             ])},
            {"nome": "Certificacao de Enlaces Opticos (Tier 1)", "horas": 16,
             "requer": ["Cabos de Fibra Optica (caracteristicas)"],
             "missoes": _mis([
                 ("c7-1", "Teste Tier 1", "certificar o enlace optico no padrao"),
                 ("c7-2", "O resultado estranho", "interpretar perda e reflexao do laudo"),
                 ("c7-3", "Passa ou reprova?", "decidir com a potencia medida se o enlace esta aprovado"),
             ])},
            {"nome": "Teste de Enlaces Opticos com OTDR", "horas": 16,
             "requer": ["Certificacao de Enlaces Opticos (Tier 1)"],
             "missoes": _mis([
                 ("c8-1", "O OTDR na mao", "lancar e ler a curva do enlace"),
                 ("c8-2", "Onde quebrou?", "achar a ruptura na curva do OTDR"),
                 ("c8-3", "Medir e comparar", "comparar a medida com o desenho do projeto"),
             ])},
            {"nome": "Orcamento de Perda e Potencia Optica", "horas": 16,
             "requer": ["Teste de Enlaces Opticos com OTDR"],
             "missoes": _mis([
                 ("c9-1", "A conta do enlace", "somar as perdas e ver se cabem no orcamento"),
                 ("c9-2", "Potencia do laser", "conferir se o transceiver atende a distancia"),
                 ("c9-3", "Folga de seguranca", "decidir se o projeto passa com margem"),
             ])},
            {"nome": "Taxa de Ocupacao de Caminhos", "horas": 16,
             "requer": ["Orcamento de Perda e Potencia Optica"],
             "missoes": _mis([
                 ("c10-1", "Caminho cheio", "calcular a ocupacao dos dutos e caminhos da obra"),
                 ("c10-2", "Crescer sem obra", "estimar quanto ainda cabe antes de furar parede"),
             ])},
            {"nome": "Pratica com Tecnologia em Fibra Optica", "horas": 8,
             "requer": ["Taxa de Ocupacao de Caminhos"],
             "missoes": _mis([
                 ("c11-1", "O desafio da torre", "montar o enlace completo do predio ao topo"),
                 ("c11-2", "Entregando a obra", "consolidar o relatorio final do projeto"),
             ])},
        ],
    },
    {
        "tema": "Mikrotik",
        "fase": "Casa arrumada: chega o roteador de borda que o Sr. Valente comprou.",
        "topicos": [
            {"nome": "MTCNA (Oficial)", "horas": 24,
             "requer": ["Protocolo TCP/IP", "Roteamento IP e RIP"],
             "missoes": _mis([
                 ("mk1-1", "Primeiro login", "acessar o RouterOS e configurar o basico"),
                 ("mk1-2", "IP na borda", "enderecar as interfaces do roteador"),
                 ("mk1-3", "DHCP dos dois lados", "cliente e servidor DHCP no Mikrotik"),
                 ("mk1-4", "Masquerade", "NAT de saida com o jeitinho RouterOS"),
                 ("mk1-5", "Firewall do Valente", "regras basicas de protecao da borda"),
             ])},
            {"nome": "MTCRE (Oficial)", "horas": 16, "requer": ["MTCNA (Oficial)"],
             "missoes": _mis([
                 ("mk2-1", "Rotas estaticas", "rotas manuais no RouterOS"),
                 ("mk2-2", "OSPF na mao", "protocolo de roteamento dinamico"),
                 ("mk2-3", "Fallback de link", "dois provedores: se um cair, o outro assume"),
             ])},
            {"nome": "MTCSE (Oficial)", "horas": 16, "requer": ["MTCRE (Oficial)"],
             "missoes": _mis([
                 ("mk3-1", "VPN site a site", "tunel entre a matriz e a filial"),
                 ("mk3-2", "Guest isolado", "wifi de visitante separado e seguro"),
                 ("mk3-3", "Filtro de trafego", "regras avancadas de firewall"),
             ])},
        ],
    },
    {
        "tema": "Ubiquiti",
        "fase": "Wi-Fi pra firma inteira, em cima da fibra ja certificada.",
        "topicos": [
            {"nome": "UFSP (Oficial)", "horas": 6,
             "requer": ["Wireless LAN (Redes sem fio)", "Cabeamento Estruturado Fibra"],
             "missoes": _mis([
                 ("ub1-1", "Adotar o AP", "colocar o equipamento no controlador UniFi"),
                 ("ub1-2", "SSID padrao", "configurar a rede sem fio da DC"),
                 ("ub1-3", "Sites e redes", "organizar os ambientes no painel"),
             ])},
            {"nome": "UWA (Oficial)", "horas": 16, "requer": ["UFSP (Oficial)"],
             "missoes": _mis([
                 ("ub2-1", "O sinal nao alcanca", "canais, potencia e interferencia no mundo RF"),
                 ("ub2-2", "Roaming sem dor", "cliente andando pela empresa muda de AP sem cair"),
                 ("ub2-3", "Projeto RF", "desenhar a cobertura de um andar inteiro"),
                 ("ub2-4", "Ache o cliente", "localizar o dispositivo no mapa"),
             ])},
        ],
    },
    {
        "tema": "Huawei",
        "fase": "O contrato grande exige padrao enterprise: a DC Corp vira provedora.",
        "topicos": [
            {"nome": "Curso Huawei Oficial", "horas": 16,
             "requer": ["MTCNA (Oficial)", "UWA (Oficial)"],
             "missoes": _mis([
                 ("hw1-1", "VLAN no Huawei", "criar VLANs e trunks no VRP"),
                 ("hw1-2", "Roteamento e NAT no Huawei", "levar o que voce ja sabe para o padrao enterprise"),
                 ("hw1-3", "Diagnostico VRP", "achar e corrigir problema no equipamento Huawei"),
             ])},
        ],
    },
    {
        "tema": "Zabbix",
        "fase": "Tudo no ar: agora ninguem dorme. Monitoramento 24h.",
        "topicos": [
            {"nome": "Zabbix do Zero", "horas": 16,
             "requer": ["Network Troubleshooting", "Protocolos e Servicos de Rede"],
             "missoes": _mis([
                 ("zb1-1", "Primeiro host", "adicionar o primeiro equipamento da DC no Zabbix"),
                 ("zb1-2", "Trigger de alerta", "criar alerta de CPU e interface"),
                 ("zb1-3", "Painel do Valente", "dashboard mostrando os andares em tempo real"),
                 ("zb1-4", "Auto-discovery", "varredura que acha os hosts sozinha"),
             ])},
        ],
    },
    {
        "tema": "DataCenter",
        "fase": "O desfecho: consolidar a DC Corp num data center de verdade.",
        "topicos": [
            {"nome": "Fundamentos em DataCenter", "horas": 16,
             "requer": ["Zabbix do Zero", "Cabeamento Profissional"],
             "missoes": _mis([
                 ("dc1-1", "Climatizando a sala", "resfriamento, energia e cabos do DC na mao"),
                 ("dc1-2", "Rede do DC", "topologia simples do data center (spine e leaf)"),
                 ("dc1-3", "O dia da migracao", "mover a DC Corp inteira para o DC novo"),
             ])},
        ],
    },
    {
        "tema": "Programacao",
        "fase": "Python: o estagiario ensina a infra a se configurar sozinha.",
        "topicos": [
            {"nome": "Python do Zero", "horas": 24, "requer": ["Modelo OSI"],
             "missoes": _mis([
                 ("pr1-1", "Primeiro script", "print, variaveis e o primeiro codigo do estagiario"),
                 ("pr1-2", "Decisoes e lacos", "if e for varrendo a lista de IPs da DC"),
                 ("pr1-3", "Funcoes do dia a dia", "funcoes que checam conectividade de um equipamento"),
             ])},
            {"nome": "Automacao de Rede", "horas": 16,
             "requer": ["Python do Zero", "Switches Ethernet - Parte II"],
             "missoes": _mis([
                 ("pr2-1", "Gerador de VLANs", "script que gera as configs das VLANs sozinho"),
                 ("pr2-2", "Backup das configs", "salvar o running-config de todos os equipamentos"),
                 ("pr2-3", "Varredura da rede", "descobrir o que esta vivo na rede da DC"),
             ])},
            {"nome": "Netmiko e Ansible", "horas": 16,
             "requer": ["Automacao de Rede", "Roteamento IP e RIP"],
             "missoes": _mis([
                 ("pr3-1", "Subindo config via Netmiko", "empurrar a config automatica para o switch"),
                 ("pr3-2", "Playbook raiz", "Ansible rodando a configuracao das VLANs"),
                 ("pr3-3", "A infra que se configura sozinha", "o grande gol da automacao na DC Corp"),
             ])},
        ],
    },
]


def missao_badge(jogo, mid):
    if mid in jogo.missoes:
        return cr("CONCLUIDA ", "green")
    m = MISSOES.get(mid)
    if m is not None and status_missao(jogo, mid) == 1:
        return cr("JOGAVEL   ", "cyan")
    return cr("EM BREVE  ", "yellow")


def estado_topico(jogo, top):
    feito = sum(1 for m in top["missoes"] if m["id"] in jogo.missoes)
    total = len(top["missoes"])
    if feito == total > 0:
        return "concluido", cr("CONCLUIDO ", "green")
    if any(m["id"] in MISSOES for m in top["missoes"]):
        return "proximo", cr("JOGAVEL   ", "cyan")
    return "breve", cr("EM BREVE  ", "yellow")


def topico_liberado(jogo, top):
    for req in top.get("requer", []):
        tr = achar_topico(req)
        if tr is None:
            continue
        if not all(m["id"] in jogo.missoes for m in tr["missoes"]):
            return False, req
    return True, None


def achar_topico(nome):
    for trilha in TRILHA:
        for top in trilha["topicos"]:
            if top["nome"] == nome:
                return top
    return None


def texto_trilha(jogo):
    linhas = [cr("== JORNADA DE APRENDIZADO (Acervo Master TI) ==", "bold"),
              cr("Uma trilha destrava a outra: a DC Corp cresce na ordem dos mundos.", "dim"),
              ""]
    geral = {"jogaveis": 0, "concluidos": 0, "total": 0}
    for trifase in TRILHA:
        linhas.append(cr(f"[ {trifase['tema'].upper()} ]", "cyan"))
        linhas.append(cr(f"  Fase: {trifase['fase']}", "dim"))
        horas_tema = sum(t["horas"] for t in trifase["topicos"])
        for top in trifase["topicos"]:
            estado, badge = estado_topico(jogo, top)
            geral["total"] += 1
            if estado == "concluido":
                geral["concluidos"] += 1
            elif estado == "proximo":
                geral["jogaveis"] += 1
            liberado, falta = topico_liberado(jogo, top)
            travado = "" if liberado or estado == "proximo" else cr(f"  (primeiro: {falta})", "red")
            linhas.append("")
            linhas.append(cr(f"  > {top['nome']} ({top['horas']}h)", "bold") + " " + badge + travado)
            for mi in top["missoes"]:
                linhas.append(f"      {mi['titulo']:<45} {missao_badge(jogo, mi['id'])}")
        linhas.append(cr(f"  total: {horas_tema}h  |  xp de meta: {horas_tema * 100}", "dim"))
        linhas.append("")
    linhas.append(cr("RESUMO:" + f" {geral['concluidos']}/{geral['total']} topicos concluidos"
                                   f"  |  {geral['jogaveis']} desses tem missao jogavel hoje", "yellow"))
    linhas.append(cr("(JOGAVEL = tem terminal funcionando | EM BREVE = ja esta no roadmap do jogo)", "dim"))
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
    def __init__(self, codigo, vlans_iniciais=None, interfaces=None, saved_inicial=False, kind="switch"):
        self.codigo = codigo
        self.hostname = codigo
        self.kind = kind
        self.modo = "user"
        self.ctx_vlan = None
        self.ctx_if = None
        self.vlans = vlans_iniciais if vlans_iniciais is not None else {1: "default"}
        self.interfaces = interfaces or {}
        for nome in list(self.interfaces):
            self.interfaces[norm_if(nome)] = self.interfaces.pop(nome)
        self.saved = saved_inicial
        self.routes = []
        self.nat_acl_num = None
        self.nat_acl_permits = []
        self.nat_source = None
        self.nat_inside = set()
        self.nat_outside = set()
        self.acl_listas = {}
        self.firewall_tested = False
        self.trafego_ok = False

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

    def trunk_carrega(self, *vlans):
        t = self.interfaces.get("fa0/24")
        if not (t and t["mode"] == "trunk" and t["trunk_allowed"] is not None):
            return False
        return set(vlans) <= t["trunk_allowed"]

    def native_vlan(self, nome="fa0/24"):
        return self.interfaces.get(nome, {}).get("native_vlan", 1)

    def acl_aplicada(self, nome_if, direcao):
        return self.interfaces.get(nome_if, {}).get(f"acl_{direcao}")

    def acl_deny_rh_diretoria(self):
        for num, regras in self.acl_listas.items():
            idx_deny = -1
            idx_permit = -1
            for i, r in enumerate(regras):
                if (r["acao"] == "deny" and r["src"] == ("192.168.20.0", "0.0.0.255")
                        and r["dst"] == ("192.168.10.0", "0.0.0.255")):
                    idx_deny = i
                    break
            for i, r in enumerate(regras):
                if r["acao"] == "permit" and r["dst"] == ("any", "any") and i > idx_deny:
                    idx_permit = i
                    break
            if idx_deny != -1 and idx_permit != -1:
                return num
        return None

    def firewall_ok(self):
        num = self.acl_deny_rh_diretoria()
        return num is not None and self.acl_aplicada("fa0/1", "in") == num

    def if_ip(self, nome):
        return self.interfaces.get(nome, {}).get("ip")

    def if_up(self, nome):
        return bool(self.interfaces.get(nome, {}).get("up", True))

    def tem_rota_tunel(self):
        for dest, mask, next_hop in self.routes:
            if dest == "0.0.0.0" and mask == "0.0.0.0":
                return True
        return False

    def nat_completo(self):
        if not (self.nat_inside and self.nat_outside and self.nat_source and self.nat_acl_num):
            return False
        acl_permite_lan = any(
            p[0] == "192.168.10.0" and p[1] == "0.0.0.255" for p in self.nat_acl_permits
        )
        return acl_permite_lan


def checar_missao(mid, d):
    if mid == "m1":
        return d.vlan_ok(10, "TI") and d.saved
    if mid == "m2":
        t = d.interfaces.get("fa0/24")
        ok_vlan20 = d.vlan_ok(20, "RH")
        ok_trunk = bool(t) and t["mode"] == "trunk" and t["trunk_allowed"] is not None and {10, 20} <= t["trunk_allowed"]
        return ok_vlan20 and ok_trunk and d.saved
    if mid == "m3":
        lan = d.interfaces.get("fa0/0")
        wan = d.interfaces.get("fa0/1")
        ok_lan = bool(lan) and lan["mode"] == "access" and lan["ip"] == "192.168.10.1/255.255.255.0" and d.if_up("fa0/0") and "fa0/0" in d.nat_inside
        ok_wan = bool(wan) and wan["ip"] == "200.100.50.2/255.255.255.252" and d.if_up("fa0/1") and "fa0/1" in d.nat_outside
        ok_rotas = d.tem_rota_tunel()
        return ok_lan and ok_wan and ok_rotas and d.nat_completo() and d.saved
    if mid == "m4":
        return d.firewall_ok() and d.firewall_tested and d.saved
    if mid == "m5":
        p = d.interfaces.get("fa0/1")
        ok_pc = bool(p) and p["mode"] == "access" and p["access_vlan"] == 10
        return ok_pc and d.trunk_carrega(10) and d.trafego_ok and d.saved
    if mid == "m6":
        ok_tr = d.trunk_carrega(10, 20)
        sem_fantasma = 999 not in d.vlans
        return ok_tr and sem_fantasma and d.native_vlan() == 99 and d.trafego_ok and d.saved
    return False


class TerminalGame:
    def __init__(self, jogo, mid):
        m = MISSOES[mid]
        self.jogo = jogo
        self.mid = mid
        self.missao = m

        def base_interface(up=True):
            return {"mode": "access", "access_vlan": 1, "trunk_allowed": None, "ip": None, "up": up,
                    "acl_in": None, "acl_out": None}

        def device_vazio(cod, kind="switch", up=True):
            return Device(
                cod,
                vlans_iniciais={1: "default"},
                interfaces={
                    "fa0/1": base_interface(up),
                    "fa0/24": base_interface(up),
                },
                kind=kind,
            )

        if mid == "m3":
            r = device_vazio("RT-01", kind="router", up=False)
            r.interfaces = {
                "fa0/0": base_interface(up=False),
                "fa0/1": base_interface(up=False),
            }
            self.devices = {"RT-01": r}
        elif mid == "m4":
            r = device_vazio("RT-01", kind="router", up=True)
            r.interfaces = {
                "fa0/0": base_interface(up=True),  # Diretoria/TI  192.168.10.0/24
                "fa0/1": base_interface(up=True),  # RH            192.168.20.0/24
            }
            r.interfaces["fa0/0"]["ip"] = "192.168.10.1/255.255.255.0"
            r.interfaces["fa0/1"]["ip"] = "192.168.20.1/255.255.255.0"
            self.devices = {"RT-01": r}
        elif mid == "m5":
            s = device_vazio("SW-01")
            s.vlans = {1: "default", 10: "TI", 20: "RH"}
            s.interfaces["fa0/1"] = {"mode": "trunk", "access_vlan": 1, "trunk_allowed": {10},
                                     "ip": None, "up": True, "acl_in": None, "acl_out": None}
            s.interfaces["fa0/24"] = {"mode": "access", "access_vlan": 1, "trunk_allowed": None,
                                      "ip": None, "up": True, "acl_in": None, "acl_out": None}
            self.devices = {"SW-01": s}
        elif mid == "m6":
            s1 = device_vazio("SW-01")
            s1.vlans = {1: "default", 10: "TI", 20: "RH"}
            s1.interfaces["fa0/24"] = {"mode": "trunk", "access_vlan": 1, "trunk_allowed": {10, 999},
                                       "ip": None, "up": True, "acl_in": None, "acl_out": None}
            s2 = device_vazio("SW-02")
            s2.vlans = {1: "default", 10: "TI", 999: "fantasma"}
            s2.interfaces["fa0/24"] = {"mode": "trunk", "access_vlan": 1, "trunk_allowed": {10, 999},
                                       "ip": None, "up": True, "acl_in": None, "acl_out": None}
            self.devices = {"SW-01": s1, "SW-02": s2}
        else:
            self.devices = {"SW-01": device_vazio("SW-01"), "SW-02": device_vazio("SW-02")}

        if mid == "m2":
            for cod, d in self.devices.items():
                d.vlans = {1: "default", 10: "TI"}
                d.saved = False
        self.atual = self.devices[list(self.devices.keys())[0]]
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
            if self.mid == "m3":
                lan = d.interfaces.get("fa0/0")
                wan = d.interfaces.get("fa0/1")
                if lan and lan["ip"] and lan["up"] and "fa0/0" in d.nat_inside:
                    requisitos.append("LAN fa0/0 ok (IP+no shutdown+NAT in)")
                else:
                    requisitos.append("LAN fa0/0: pendente")
                if wan and wan["ip"] and wan["up"] and "fa0/1" in d.nat_outside:
                    requisitos.append("WAN fa0/1 ok (IP+no shutdown+NAT out)")
                else:
                    requisitos.append("WAN fa0/1: pendente")
                if d.tem_rota_tunel():
                    requisitos.append("default route ok")
                else:
                    requisitos.append("default route: pendente")
                if d.nat_completo():
                    requisitos.append("NAT ok (ACL + source overload)")
                else:
                    requisitos.append("NAT: pendente")
            if self.mid == "m4":
                num = d.acl_deny_rh_diretoria()
                if num is not None:
                    requisitos.append(f"ACL {num}: nega RH->Diretoria 1o")
                else:
                    requisitos.append("ACL negando RH->Diretoria: pendente")
                if d.acl_aplicada("fa0/1", "in"):
                    requisitos.append("aplicada in fa0/1")
                else:
                    requisitos.append("apl. in fa0/1: pendente")
                if d.firewall_tested:
                    requisitos.append("teste de trafego ok")
                else:
                    requisitos.append("teste de trafego: nao rodou")
            if self.mid == "m5":
                if d.trunk_carrega(10):
                    requisitos.append("uplink trunk liberando VLAN 10")
                else:
                    requisitos.append("uplink fa0/24 como trunk 10: pendente")
                p = d.interfaces.get("fa0/1")
                if p and p["mode"] == "access" and p["access_vlan"] == 10:
                    requisitos.append("PC fa0/1 access VLAN 10")
                else:
                    requisitos.append("PC fa0/1 access VLAN 10: pendente")
                if d.trafego_ok:
                    requisitos.append("teste de trafego ok")
                else:
                    requisitos.append("teste de trafego: nao rodou")
            if self.mid == "m6":
                if d.trunk_carrega(10, 20):
                    requisitos.append("trunk permitindo so 10 e 20")
                else:
                    requisitos.append("trunk allowed vlan 10,20: pendente")
                if 999 not in d.vlans:
                    requisitos.append("VLAN fantasma 999 nao existe")
                else:
                    requisitos.append("VLAN fantasma 999 AINDA existe")
                if d.native_vlan() == 99:
                    requisitos.append("native vlan 99")
                else:
                    requisitos.append("native vlan 99: pendente")
                if d.trafego_ok:
                    requisitos.append("teste de trafego ok")
                else:
                    requisitos.append("teste de trafego: nao rodou")
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
        if self.mid == "m3":
            if not (d.if_ip("fa0/0") and d.if_up("fa0/0")):
                return "LAN: interface fa0/0 -> ip address 192.168.10.1 255.255.255.0, depois no shutdown"
            if not (d.if_ip("fa0/1") and d.if_up("fa0/1")):
                return "WAN: interface fa0/1 -> ip address 200.100.50.2 255.255.255.252, depois no shutdown"
            if "fa0/0" not in d.nat_inside or "fa0/1" not in d.nat_outside:
                return "Marque o NAT: dentro de interface fa0/0 digite ip nat inside; em fa0/1, ip nat outside"
            if not d.tem_rota_tunel():
                return "Falta a saida pro mundo: ip route 0.0.0.0 0.0.0.0 200.100.50.1"
            if not d.nat_completo():
                return "Falta traduzir: config global -> access-list 1 permit 192.168.10.0 0.0.0.255 e ip nat inside source list 1 interface fa0/1 overload"
            if not d.saved:
                return "Falta salvar: write memory"
            return "Tudo pronto. Confira com: ping 8.8.8.8"
        if self.mid == "m4":
            if d.acl_deny_rh_diretoria() is None:
                return "Crie a regra que BARRA o RH: access-list 100 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255"
            if not d.acl_aplicada("fa0/1", "in"):
                return "Aplique a ACL na porta de entrada do RH: interface fa0/1 -> ip access-group 100 in"
            if not d.firewall_tested:
                return "Falta conferir: rode  simular trafego  e veja o contador no show access-lists"
            if not d.saved:
                return "Falta salvar: write memory"
            return "Muro de pe. Olha o contador no show access-lists."
        if self.mid == "m5":
            if not d.trunk_carrega(10):
                return "Uplink errado: interface fa0/24 -> switchport mode trunk -> switchport trunk allowed vlan 10"
            p = d.interfaces.get("fa0/1")
            if not (p and p["mode"] == "access" and p["access_vlan"] == 10):
                return "Porta do PC trocada: interface fa0/1 -> switchport mode access -> switchport access vlan 10"
            if not d.trafego_ok:
                return "Confirme que o PC conecta:  simular trafego"
            if not d.saved:
                return "Falta salvar: write memory"
            return "Portas na ordem certa. O show interfaces trunk nao mente mais."
        if self.mid == "m6":
            if not d.trunk_carrega(10, 20):
                return "Trunk so com 10 e 20: interface fa0/24 -> switchport trunk allowed vlan 10,20"
            if d.native_vlan() != 99:
                return "VLAN nativa padrao da DC: interface fa0/24 -> switchport trunk native vlan 99"
            if 999 in d.vlans:
                return "Mate a fantasma: configure terminal -> no vlan 999 (quando estiver no SW-02)"
            if not d.trafego_ok:
                return "Rode  simular trafego  neste equipamento"
            if not d.saved:
                return "Falta salvar: write memory"
            return "Trunk enxuto. A fantasma virou po."
        return "Digite help para ver comandos."

    def help_tela(self):
        d = self.atual
        eh_router = d.kind == "router"
        if d["modo"] == "user":
            if eh_router:
                linhas = [
                    cr(f"== COMANDOS DO {d.hostname} ==", "bold"),
                    "  enable                          modo privilegiado",
                    "  show ip route / interfaces trunk",
                    "  ping 8.8.8.8                    testa a saida",
                    "  missao / progresso / detonado / dica",
                    "  trilha (jornada do Acervo) / help / sair",
                ]
            else:
                linhas = [
                    cr(f"== COMANDOS DO {d.hostname} ==", "bold"),
                    "  enable                          modo privilegiado",
                    "  show vlan brief / running-config",
                    "  show interfaces trunk / show switches",
                    "  conectar SW-01|SW-02            troca de equipamento",
                    "  missao / progresso / detonado / dica",
                    "  trilha (jornada do Acervo) / help / sair",
                ]
        elif d["modo"] == "priv":
            if eh_router:
                linhas = [
                    cr("== MODO PRIVILEGIADO (roteador) ==", "bold"),
                    "  configure terminal              modo de configuracao",
                    "  show ip route / show ip nat translations / show access-lists",
                    "  ping 8.8.8.8                    testa o trajeto completo",
                    "  simular trafego                 testa o firewall (ACL)",
                    "  write memory                    salva a config",
                    "  exit / end",
                ]
            else:
                linhas = [
                    cr("== MODO PRIVILEGIADO (switch) ==", "bold"),
                    "  configure terminal              modo de configuracao",
                    "  show vlan brief / running-config / interfaces trunk",
                    "  simular trafego                 testa a camada 2 (trunk/ACL)",
                    "  write memory                    salva a config",
                    "  exit / end                      navegacao",
                ]
        elif d["modo"] == "conf":
            linhas = [
                cr("== CONFIGURACAO GLOBAL ==", "bold"),
                "  vlan <numero>                   cria/entra na VLAN",
                "  no vlan <numero>                remove uma VLAN do switch",
                "  interface fa0/24                entra na interface",
                "  ip route <rede> <masc> <next-hop>   rota estatica",
                "  access-list <n> permit|deny <src> <wild> [<dst> <wild>]  ACL",
                "  ip nat inside source list <n> interface <if> overload   NAT",
                "  end / exit",
            ]
        elif d["modo"] == "conf-vlan":
            linhas = [
                cr(f"== VLAN {d.ctx_vlan} ==", "bold"),
                "  name <nome>                     nomeia a VLAN",
                "  exit / end                      sai",
            ]
        else:
            if eh_router:
                linhas = [
                    cr(f"== INTERFACE {d.ctx_if} (roteador) ==", "bold"),
                    "  ip address <ip> <mascara>      poe o endereco",
                    "  no shutdown                    sobe a porta",
                    "  ip nat inside | outside        marca o lado do NAT",
                    "  ip access-group <n> in|out     aplica a ACL",
                    "  exit / end",
                ]
            else:
                linhas = [
                    cr(f"== INTERFACE {d.ctx_if} (switch) ==", "bold"),
                    "  switchport mode trunk           vira trunk",
                    "  switchport mode access          vira porta comum",
                    "  switchport access vlan <n>      poe a porta na VLAN",
                    "  switchport trunk allowed vlan <a>,<b>   limita VLANs",
                    "  switchport trunk native vlan <n>   VLAN nativa (sem tag)",
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
        if d.kind == "router":
            return cr("Roteador nao tem VLAN. E dispositivo de nivel 3: use show ip route.", "yellow")
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
            if d.kind == "router":
                partes.append(" no shutdown" if itf["up"] else " shutdown")
                if itf["ip"]:
                    ip, masc = itf["ip"].split("/")
                    partes.append(f" ip address {ip} {masc}")
                if nome_if in d.nat_inside:
                    partes.append(" ip nat inside")
                if nome_if in d.nat_outside:
                    partes.append(" ip nat outside")
                if itf.get("acl_in"):
                    partes.append(f" ip access-group {itf['acl_in']} in")
                if itf.get("acl_out"):
                    partes.append(f" ip access-group {itf['acl_out']} out")
            elif itf["mode"] == "trunk":
                partes.append(" switchport mode trunk")
                if itf.get("native_vlan") is not None:
                    partes.append(f" switchport trunk native vlan {itf['native_vlan']}")
                if itf["trunk_allowed"] is not None:
                    partes.append(" switchport trunk allowed vlan " +
                                  ",".join(str(v) for v in sorted(itf["trunk_allowed"])))
            else:
                partes.append(" switchport mode access")
                partes.append(f" switchport access vlan {itf['access_vlan']}")
            partes.append("!")
        if d.kind == "router":
            for dest, masc, next_hop in d.routes:
                partes.append(f"ip route {dest} {masc} {next_hop}")
            for num in sorted(d.acl_listas):
                for regra in d.acl_listas[num]:
                    if regra["proto"]:
                        partes.append(f"access-list {num} {regra['acao']} {regra['proto']} {regra['src'][0]} {regra['src'][1]} {regra['dst'][0]} {regra['dst'][1]}")
                    else:
                        partes.append(f"access-list {num} {regra['acao']} {regra['src'][0]} {regra['src'][1]}")
            if d.nat_acl_num is not None:
                for rede, wildcard in d.nat_acl_permits:
                    partes.append(f"access-list {d.nat_acl_num} permit {rede} {wildcard}")
            if d.nat_source:
                partes.append(f"ip nat inside source list {d.nat_acl_num} interface {d.nat_source['interface']} overload")
        partes.append("end")
        return "\n".join(partes)

    def show_ip_route(self):
        d = self.atual
        if d.kind != "router":
            return cr("Switch L2 nao roteia. Use show vlan brief.", "yellow")
        if not d.routes and not any(d.if_ip(n) for n in d.interfaces):
            return "Tabela de rotas vazia. (Configure as interfaces e as rotas!)"
        linhas = ["", "Codes: C - connected, S - static"]
        for nome_if in d.ordem_interfaces():
            ip = d.if_ip(nome_if)
            if ip:
                end_ip, masc = ip.split("/")
                octetos = [int(o) for o in end_ip.split(".")]
                if octetos[2] in (10, 20, 30):
                    rede = f"{octetos[0]}.{octetos[1]}.{octetos[2]}.0"
                    linhas.append(f"C  {rede} is directly connected, {nome_if}")
        for dest, masc, next_hop in d.routes:
            linhas.append(f"S  {dest}/0.0.0.0 [1/0] via {next_hop}" if dest == "0.0.0.0" else f"S  {dest}/16 [1/0] via {next_hop}")
        linhas.append("")
        return "\n".join(linhas)

    def show_nat(self):
        d = self.atual
        if d.kind != "router":
            return cr("NAT e recurso de roteador/borda.", "yellow")
        if d.if_ip("fa0/1") and d.nat_source:
            wan_ip = d.if_ip("fa0/1").split("/")[0]
            return "\n".join([
                "",
                "Pro Inside Global      Inside Local       Outside Global    Outside Local",
                "icmp 200.100.50.2:1024 192.168.10.25:1024 8.8.8.8:0          8.8.8.8:0",
                f"(amostra: host 192.168.10.25 saiu como {wan_ip})",
                "",
            ])
        return cr("Nenhuma traducao NAT configurada/ativa ainda.", "yellow")

    def show_trunk(self):
        d = self.atual
        if not d.trunk_info():
            return cr("Nenhuma porta em modo trunk.", "yellow")
        linhas = ["", "Port        Mode         Encapsulation  Status        Native vlan",
                  "------      ------------ -------------  ------------- -------------"]
        for nome_if, allowed in d.trunk_info():
            linhas.append(f"{nome_if:<12} on          802.1q         trunking      {d.native_vlan(nome_if)}")
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

    def show_access_lists(self):
        d = self.atual
        if not d.acl_listas:
            return cr("Nenhuma access-list configurada ainda.", "yellow")
        linhas = ["", "Access-lists configuradas:"]
        for num in sorted(d.acl_listas):
            linhas.append(f"IP access list {num}")
            for i, regra in enumerate(d.acl_listas[num]):
                if regra["proto"]:
                    partes = f"{regra['acao'].upper():<7} {regra['proto']:<3} {regra['src'][0].upper():<15} {regra['src'][1]:<11} {regra['dst'][0].upper():<15} {regra['dst'][1]}"
                else:
                    partes = f"{regra['acao'].upper():<7} {regra['src'][0].upper():<15} {regra['src'][1]:<11}"
                base = f"    {i+1} {partes}"
                if regra["contador"]:
                    linhas.append(f"{base}   (match: {regra['contador']})")
                else:
                    linhas.append(base)
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
            d["interfaces"][nome] = {"mode": "access", "access_vlan": 1, "trunk_allowed": None, "ip": None, "up": False if d.kind == "router" else True,
                                     "acl_in": None, "acl_out": None}
            print(cr(f"(criando interface {nome} no simulador)", "dim"))
        d["ctx_if"] = nome
        d["modo"] = "conf-if"
        print(f"Entrando na interface {nome}...")

    def ac_switchport(self, arg_resto):
        d = self.atual
        if d.kind == "router":
            self.comando_errado("% switchport nao existe em roteador. Use ip address / ip nat.")
            return
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
                return
            if len(partes) >= 4 and partes[1] == "native" and partes[2] == "vlan":
                try:
                    vid = int(partes[3])
                except ValueError:
                    self.comando_errado("% Invalid vlan number.")
                    return
                if not (1 <= vid <= 4094):
                    self.comando_errado("% VLAN id must be between 1 and 4094.")
                    return
                itf["native_vlan"] = vid
                self.jogo.ganha_xp(30, f"native vlan {vid} em {nome}")
                print(cr(f"VLAN nativa do trunk {nome} = {vid} (frames sem tag agora ficam nessa VLAN).", "green"))
                return
            self.comando_errado("% Use: switchport trunk allowed vlan <a>,<b>  |  switchport trunk native vlan <n>")
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

    def ac_no(self, arg_resto):
        d = self.atual
        if d["modo"] == "conf-if":
            if arg_resto.lower().startswith("shutdown"):
                d["interfaces"][d["ctx_if"]]["up"] = True
                self.jogo.ganha_xp(10, f"{d['ctx_if']} no shutdown")
                print(cr(f"Interface {d['ctx_if']} UP.", "green"))
            else:
                self.comando_errado("% Use: no shutdown")
            return
        if d["modo"] == "conf":
            partes = arg_resto.lower().split()
            if partes and partes[0] == "vlan":
                try:
                    vid = int(partes[1])
                except (ValueError, IndexError):
                    self.comando_errado("% Use: no vlan <numero>")
                    return
                if vid not in d["vlans"]:
                    self.comando_errado(cr("% VLAN " + str(vid) + " nao existe neste switch.", "yellow"))
                    return
                if vid == 1:
                    self.comando_errado("% Nao da pra derrubar a VLAN 1 (default).")
                    return
                morto = d["vlans"].pop(vid, None)
                for itf in d["interfaces"].values():
                    if itf.get("trunk_allowed"):
                        itf["trunk_allowed"].discard(vid)
                self.jogo.ganha_xp(40, f"VLAN {vid} exterminada")
                print(cr(f"VLAN {vid} ({morto}) removida do banco e liberada dos trunks.", "green"))
                return
            self.comando_errado("% Use: no vlan <numero> (ou em interface: no shutdown)")
            return
        self.comando_errado("% no is only allowed in configuration mode.")

    def ac_ip(self, partes):
        d = self.atual
        if not partes:
            self.comando_errado("% Incomplete command.")
            return
        cmd = [p.lower() for p in partes]
        if d["modo"] == "conf-if":
            if cmd[0] == "address":
                if len(cmd) < 2:
                    self.comando_errado("% Use: ip address <ip> <mascara>")
                    return
                masc = cmd[2] if len(cmd) >= 3 else "255.255.255.0"
                d["interfaces"][d["ctx_if"]]["ip"] = f"{cmd[1]}/{masc}"
                self.jogo.ganha_xp(20, f"{d['ctx_if']} ip {cmd[1]}")
            elif cmd[0] == "access-group":
                if len(cmd) < 3 or cmd[2] not in ("in", "out"):
                    self.comando_errado("% Use: ip access-group <numero> in|out")
                    return
                try:
                    num = int(cmd[1])
                except ValueError:
                    self.comando_errado("% Numero de ACL invalido.")
                    return
                d["interfaces"][d["ctx_if"]][f"acl_{cmd[2]}"] = num
                self.jogo.ganha_xp(25, f"ACL {num} aplicada em {d['ctx_if']} {cmd[2]}")
                print(cr(f"ACL {num} aplicada em {d['ctx_if']} (entrada {cmd[2]}).", "green"))
            elif cmd[0] == "nat":
                if len(cmd) < 2:
                    self.comando_errado("% Use: ip nat inside | ip nat outside")
                    return
                if cmd[1] == "inside":
                    d.nat_inside.add(d["ctx_if"])
                    self.jogo.ganha_xp(10, f"{d['ctx_if']} NAT inside")
                    print(cr(f"Interface {d['ctx_if']} marcada como lado interno (inside).", "yellow"))
                elif cmd[1] == "outside":
                    d.nat_outside.add(d["ctx_if"])
                    self.jogo.ganha_xp(10, f"{d['ctx_if']} NAT outside")
                    print(cr(f"Interface {d['ctx_if']} marcada como lado externo (outside).", "yellow"))
                else:
                    self.comando_errado("% Use: ip nat inside | ip nat outside")
            else:
                self.comando_errado("% Em interface use: ip address | ip nat inside | ip nat outside")
            return
        if d["modo"] == "conf":
            if cmd[0] == "route":
                if len(cmd) < 4:
                    self.comando_errado("% Use: ip route <rede> <mascara> <next-hop>")
                    return
                d.routes.append((cmd[1], cmd[2], cmd[3]))
                self.jogo.ganha_xp(30, "rota estatica criada")
                if cmd[1] == "0.0.0.0":
                    print(cr("Default route para o mundo configurada.", "green"))
            elif cmd[0] == "nat" and cmd[1:4] == ["inside", "source", "list"]:
                try:
                    num = int(cmd[4])
                except (ValueError, IndexError):
                    self.comando_errado("% Numero de access-list invalido.")
                    return
                if len(cmd) == 8 and cmd[5] == "interface" and cmd[7] == "overload":
                    d.nat_acl_num = num
                    d.nat_source = {"acl": num, "interface": cmd[6]}
                    self.jogo.ganha_xp(40, "NAT overload configurado")
                    print(cr("NAT inside source ... overload aplicado.", "green"))
                else:
                    self.comando_errado("% Use: ip nat inside source list <n> interface <if> overload")
            else:
                self.comando_errado("% Em config global use: ip route | ip nat inside source list")
            return
        self.comando_errado("% ip command not allowed in this mode.")

    def ac_access_list(self, arg_resto):
        d = self.atual
        if d["modo"] != "conf":
            self.comando_errado("% access-list is only allowed in configuration mode.")
            return
        partes = arg_resto.split()
        if len(partes) < 4 or partes[1].lower() not in ("permit", "deny"):
            self.comando_errado("% Use: access-list <n> permit|deny ip <src> <wild> <dst> <wild>  (ou  <src> <wild> p/ permit simples)")
            return
        try:
            num = int(partes[0])
        except ValueError:
            self.comando_errado("% Valor invalido.")
            return
        acao = partes[1].lower()
        p = [x.lower() for x in partes]
        proto = None
        if p[2] in ("ip", "tcp", "udp", "icmp"):
            proto = p[2]
            if len(p) >= 7:
                src = (p[3], p[4])
                dst = (p[5], p[6])
            elif len(p) == 5 and p[3] == "any" and p[4] == "any":
                src = ("any", "any")
                dst = ("any", "any")
            else:
                self.comando_errado("% Use: access-list <n> deny ip <src> <wildcard> <dst> <wildcard>")
                return
        else:
            src = (p[2], p[3])
            dst = ("any", "any")
        regra = {"acao": acao, "proto": proto, "src": src, "dst": dst, "contador": 0}
        d.acl_listas.setdefault(num, []).append(regra)
        if acao == "permit":
            d.nat_acl_num = num
            if src[0] != "any":
                d.nat_acl_permits.append(src)
        self.jogo.ganha_xp(15, f"ACL {num} {acao} {src[0]} -> {dst[0]}")
        print(cr(f"Lista de acesso {num}: regra {acao} adicionada (regras na lista: {len(d.acl_listas[num])}).", "yellow"))

    def verificar_trafego_simples(self, regra, src_ip, dst_ip):
        def bate(par, ip):
            rede, wild = par
            if rede == "any":
                return True
            quartos = [int(x) for x in rede.split(".")]
            masc = [255 - int(w) for w in wild.split(".")] if wild != "0.0.0.0" else [255] * 4
            alvo = [int(x) for x in ip.split(".")]
            return all((q & m) == (t & m) for q, m, t in zip(quartos, masc, alvo))
        if regra["acao"] == "permit":
            return bate(regra["src"], src_ip) and bate(regra["dst"], dst_ip)
        if regra["acao"] == "deny":
            return None if (bate(regra["src"], src_ip) and bate(regra["dst"], dst_ip)) else False
        return False

    def ac_simular(self, resto):
        d = self.atual
        if d["modo"] != "priv":
            self.comando_errado("% simular is only allowed in privileged mode.")
            return
        if self.mid == "m5":
            print()
            print(cr("== SIMULANDO TRAFEGO LAYER 2 ==", "bold"))
            p = d.interfaces.get("fa0/1")
            if not (p and p["mode"] == "access" and p["access_vlan"] == 10):
                print(cr("  PC da sala B   : nao sobe. A porta esta como "
                         + ("trunk!" if p and p["mode"] == "trunk" else "errada."), "red"))
                print(cr("  (porta de escritorio precisa ser access VLAN 10)", "dim"))
            else:
                print(cr("  PC da sala B   : CONECTOU na VLAN 10 (access)", "green"))
            if d.trunk_carrega(10):
                print(cr("  Uplink SW      : leva a VLAN 10 ate o nucleo", "green"))
            else:
                print(cr("  Uplink SW      : nao libera a VLAN 10 (confira o trunk fa0/24)", "red"))
            print()
            if (p and p["mode"] == "access" and p["access_vlan"] == 10) and d.trunk_carrega(10):
                d.trafego_ok = True
                print(cr("Trunk na ordem: PC da sala conversa com o nucleo. E o Valente dorme.", "green"))
                self.jogo.ganha_xp(50, "teste de trafego concluido")
            else:
                print(cr("Ainda nao: porta do PC e/ou uplink estao no lugar errado.", "yellow"))
            return
        if self.mid == "m6":
            print()
            print(cr("== SIMULANDO TRAFEGO DO TRUNK ==", "bold"))
            if d.trunk_carrega(10, 20):
                print(cr("  VLAN 20 (RH) : atravessou o trunk e chegou na TI", "green"))
            else:
                print(cr("  VLAN 20 (RH) : se perdeu no meio do caminho (allowed vlan sem 20)", "red"))
            if d.native_vlan() == 99:
                print(cr("  Native 99    : trafego sem tag nao vaza e nao mistura", "green"))
            else:
                print(cr("  Native      : errada! Frames sem tag vao parar na VLAN errada.", "red"))
                print(cr("  (padrao da DC Corp: switchport trunk native vlan 99)", "dim"))
            if 999 in d.vlans:
                print(cr("  FANTASMA 999 : broadcast fantasma perambulando no link!", "red"))
            else:
                print(cr("  FANTASMA     : nenhuma VLAN sem dono. Limpeza concluida.", "green"))
            print()
            if d.trunk_carrega(10, 20) and d.native_vlan() == 99 and 999 not in d.vlans:
                d.trafego_ok = True
                print(cr("Link saudavel: so as VLANs 10 e 20 passam, sem fantasma. Missao de layer 2.", "green"))
                self.jogo.ganha_xp(50, "teste de trafego concluido")
            else:
                print(cr("Trunk ainda meio suja: allowed, native e/ou a fantasma 999.", "yellow"))
            return
        num_acl = d.acl_aplicada("fa0/1", "in")
        regras = d.acl_listas.get(num_acl, [])
        num_ok = num_acl == d.acl_deny_rh_diretoria()
        print()
        print(cr("== SIMULANDO TRAFEGO ==", "bold"))
        ok_rh = True
        ok_ti = True

        origem, destino = "192.168.20.15", "192.168.10.30"
        bloqueado = False
        for regra in regras:
            if regra["acao"] == "deny" and self.verificar_trafego_simples(regra, origem, destino) is None:
                bloqueado = True
                regra["contador"] += 1
                print(cr(f"  RH -> Diretoria   : BLOQUEADO  (deny bateu, contador {regra['contador']})", "green"))
                break
            if regra["acao"] == "permit" and self.verificar_trafego_simples(regra, origem, destino):
                break
        if not bloqueado:
            ok_rh = False
            if not regras:
                print(cr("  RH -> Diretoria   : LIBERADO! Nenhuma ACL aplicada na porta.", "red"))
            else:
                print(cr("  RH -> Diretoria   : LIBERADO! A regra deny nao veio antes.", "red"))

        origem, destino = "192.168.10.5", "200.100.50.1"
        liberado = False
        for regra in regras:
            if regra["acao"] == "deny" and self.verificar_trafego_simples(regra, origem, destino) is None:
                break
            if regra["acao"] == "permit" and self.verificar_trafego_simples(regra, origem, destino):
                liberado = True
                regra["contador"] += 1
                break
        if liberado:
            print(cr("  TI -> Internet    : LIBERADO", "green"))
        else:
            ok_ti = False
            print(cr("  TI -> Internet    : BLOQUEADO! Falta o permit generico no fim.", "red"))

        print()
        if ok_rh and ok_ti and num_ok:
            d.firewall_tested = True
            print(cr("Firewall validado: RH preso, TI navegando.", "green"))
            self.jogo.ganha_xp(50, "teste de trafego concluido")
        else:
            print(cr("Ainda nao: a config nao bloqueia o RH e libera o TI ao mesmo tempo.", "yellow"))
            print(cr("Dica: a ordem das regras manda (a primeira que bate vale).", "dim"))

    def ac_ping(self):
        d = self.atual
        if d.kind != "router":
            self.comando_errado("% Switch L2 nao pinga. Use ping em um roteador.")
            return
        print()
        print("PING 8.8.8.8 (8.8.8.8) from um host da LAN 192.168.10.x: 32 data bytes")
        if not (d.if_ip("fa0/0") and d.if_up("fa0/0")):
            print(cr("Reply from 192.168.10.1: Destination host unreachable.", "red"))
            print(cr("LAN sem ip/up na fa0/0: nenhum host conseguiu nem sair do predio.", "yellow"))
            return
        if not d.tem_rota_tunel():
            print("Request timed out. 0/4 receptions")
            print(cr("O pacote subiu do host, chegou no roteador e... nao tinha pra onde ir: falta a rota pro mundo.", "yellow"))
            return
        if not d.nat_completo():
            print("Request timed out. 0/4 receptions")
            print(cr("Pacote com IP privado 192.168.10.25 chegou na borda e morreu: NAT nao traduziu.",
                     "yellow"))
            print(cr("Confira a ACL (permit 192.168.10.0/0.0.0.255), os lados inside/outside e o overload.", "dim"))
            return
        if not d.if_ip("fa0/1"):
            print("Request timed out. 0/4 receptions")
            return
        print(cr("Reply from 8.8.8.8: bytes=32 time=1ms TTL=57", "green"))
        print(cr("Reply from 8.8.8.8: bytes=32 time=1ms TTL=57", "green"))
        print(cr("Reply from 8.8.8.8: bytes=32 time=1ms TTL=57", "green"))
        print(cr("Reply from 8.8.8.8: bytes=32 time=1ms TTL=57", "green"))
        print(cr("Round-trip min/avg/max = 1/1/2 ms", "green"))
        print(cr("4/4. O host da DC Corp ta NA INTERNET. O Valente vai chorar de orgulho.",
                 "green"))
        self.jogo.ganha_xp(20, "ping de sucesso")

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
            self.comando_errado("% Host desconhecido. Disponiveis: " + ", ".join(self.devices))

    # ---- loop ----

    def jogar(self):
        print()
        motd([(linha, "magenta") for linha in self.missao["cena_intro"]])
        print()
        print(cr(f"Voce esta no terminal do {self.atual.hostname}. Digite help para os comandos.", "green"))
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
            elif cmd in ("trilha", "jornada"):
                print(texto_trilha(self.jogo))
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
                elif arg == "access-lists":
                    print(self.show_access_lists())
                elif arg == "ip":
                    sub = partes[2:3]
                    if sub == ["route"]:
                        print(self.show_ip_route())
                    elif sub == ["nat"]:
                        print(self.show_nat())
                    else:
                        self.comando_desconhecido(linha)
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
            elif cmd == "no":
                self.ac_no(arg_resto)
            elif cmd == "ip":
                self.ac_ip(partes[1:])
            elif cmd == "access-list":
                self.ac_access_list(arg_resto)
            elif cmd == "simular":
                if arg == "trafego":
                    self.ac_simular(arg_resto)
                else:
                    self.comando_errado("% Use: simular trafego")
            elif cmd == "ping":
                self.ac_ping()
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
        linhas = [cr("Equipamentos da missao:", "bold")]
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
        elif self.mid == "m3":
            print(cr('Valente: "O mundo. A DC CORP TAXA NA INTERNET! O povo ainda', "magenta"))
            print(cr('  vai chorar de alegria. E olha, ROUTING michel. Aguenta esse"', "magenta"))
            print(cr('  emprego, garoto, que daqui a pouco voce me cobra."', "magenta"))
            print(cr('  (A Janaina deu o polegar por tras da porta.)', "dim"))
        elif self.mid == "m4":
            print(cr('Janaina: "Muro de pe. O RH nao decola mais na Diretoria e o', "magenta"))
            print(cr('  gato do Valente costurou o link do TI sem cerol. ACL na veia.', "magenta"))
            print(cr('  So falta voce me garantir a proxima."', "magenta"))
            print(cr('  (No painel dela, o contador da sua deny sobe: 1 batida.)', "dim"))
        elif self.mid == "m5":
            print(cr('Janaina: "Porta de PC com VLAN de andar, uplink no modo certo.', "magenta"))
            print(cr('  Voce achou a bagunca de layer 2 sozinho, sem eu dar a mao.', "magenta"))
            print(cr('  E o povo que tava no ``no ar``? Ta de volta. Bom sinal."', "magenta"))
            print(cr('  (A Janaina anotou no caderninho dela: RESPONDEU SOZINHO.)', "dim"))
        elif self.mid == "m6":
            print(cr('Janaina: "Allowed vlan enxuto, nativa padrao, fantasma virou po.', "magenta"))
            print(cr('  Quando a VLAN 20 sair do RH e chegar na TI inteira, sabe', "magenta"))
            print(cr('  de quem vai ser o merito? Da config. E de quem configurou? Seu."', "magenta"))
            print(cr('  (E o aposento do Sr. Valente voltou a ter silencio.)', "dim"))
        print()
        print(cr("Voltando a central de operacoes...", "dim"))
        if self.jogo.salvar():
            print(cr("Progresso salvo automaticamente em save_dc_corp.json.", "green"))


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
        print("   5) Trilha de Aprendizado (Acervo)")
        print("   6) Sair")
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
            print()
            print(texto_trilha(jogo))
        elif escolha == "6":
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
        elif escolha in ("trilha", "jornada"):
            print()
            print(texto_trilha(jogo))
        else:
            print(cr("Comando nao reconhecido. Use os numeros 1 a 6.", "red"))
    if jogo.salvar():
        print(cr("Progresso salvo em save_dc_corp.json.", "green"))


def main():
    jogo = Personagem.carregar()
    if jogo.missoes:
        print(cr(f"(save encontrado: {jogo.xp} XP, {len(jogo.missoes)} missoes concluidas)", "dim"))
    try:
        central(jogo)
    except KeyboardInterrupt:
        print()
        print(cr("Conexao encerrada. O Valente ja vai ouvir sobre isso.", "dim"))
        jogo.salvar()
    print()
    print(cr("Sessao encerrada. A DC Corp agradece. Volte sempre, estagiario.", "dim"))


if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""DC CORP - MODO HISTORIA (prototipo visual)

O mesmo jogo, agora com cara de historia em quadrinhos:
  - narrativa com cenas desenhadas na tela + baloes de conversa;
  - nas missoes, o TERMINAL abre de um lado e o DETONADO (guia) do outro;
  - a engine de terminal (dc_corp_jogo.py) e reaproveitada inteira.

Como rodar:  python dc_corp_gui.py
Requer: Python 3 com tkinter (ja vem no Windows). Sem dependencias.
"""

import queue
import re
import sys
import threading
import tkinter as tk
from tkinter import font as tkfont

import dc_corp_jogo as core

ANSI = re.compile(r"\x1b\[[0-9;]*m")

U = {
    "fundo": "#0e1116",
    "painel": "#151a22",
    "painel2": "#1b2330",
    "borda": "#2a3345",
    "texto": "#e6edf3",
    "dim": "#8a94a6",
    "ciano": "#35d0ba",
    "roxo": "#8a63d2",
    "verde": "#3fae4a",
    "amarelo": "#e0b23a",
    "vermelho": "#d94f5a",
    "entrada": "#02050a",
    "term": "#8ff0c8",
    "term_dim": "#4d6b63",
}

NPC_CORES = {
    "Janaina": "#d94f9a",
    "Valente": "#3fae4a",
    "Santos": "#4a7fd9",
}


def _noop(*a, **k):
    return None


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DC CORP - Modo Historia (prototipo visual)")
        self.configure(bg=U["fundo"])
        self.geometry("1160x760")
        self.minsize(980, 640)

        self.jogo = core.Personagem.carregar()
        self.fila_saida = queue.Queue()
        self.fila_entrada = queue.Queue()
        self.mid = None
        self.tg = None
        self.thread = None
        self._stdout_ant = sys.stdout

        self._montar_fontes()
        self._montar_hud()
        self._montar_cena()
        self._montar_missao()
        self._montar_overlay()

        self.after(50, self._drenar_saidas)
        self.protocol("WM_DELETE_WINDOW", self._fechar)
        self._ir_titulo()

    # ------------------------------------------------------------ fontes

    def _montar_fontes(self):
        fam = "Consolas"
        self.f_tit = tkfont.Font(family=fam, size=17, weight="bold")
        self.f_grd = tkfont.Font(family=fam, size=12, weight="bold")
        self.f_nrm = tkfont.Font(family=fam, size=11)
        self.f_bal = tkfont.Font(family=fam, size=13, weight="bold")
        self.f_txt = tkfont.Font(family=fam, size=12)
        self.f_det = tkfont.Font(family=fam, size=10)

    # ------------------------------------------------------------ HUD

    def _montar_hud(self):
        self.hud = tk.Frame(self, bg=U["painel"], height=66)
        self.hud.pack(fill="x")
        self.hud.pack_propagate(False)
        left = tk.Frame(self.hud, bg=U["painel"])
        left.pack(side="left", padx=14, pady=8)
        self.l_titulo = tk.Label(left, text="DC CORP", font=self.f_tit,
                                 fg=U["ciano"], bg=U["painel"])
        self.l_titulo.pack(side="left")
        self.l_sub = tk.Label(left, text=" SISTEMA DE TREINAMENTO E PROGRESSAO",
                              font=self.f_nrm, fg=U["dim"], bg=U["painel"])
        self.l_sub.pack(side="left", padx=(8, 0))
        right = tk.Frame(self.hud, bg=U["painel"])
        right.pack(side="right", padx=14, pady=8)
        self.l_hud = tk.Label(right, text="", font=self.f_grd,
                              fg=U["amarelo"], bg=U["painel"])
        self.l_hud.pack()
        self._atualizar_hud()

    def _atualizar_hud(self):
        j = self.jogo
        cargo = core.cargo_atual(j.xp)
        self.l_hud.config(text=f"  XP {j.xp}   ::   {cargo}  ")
        cap = ""
        if self.mid and self.mid in core.MISSOES:
            m = core.MISSOES[self.mid]
            cap = f"  |  MISSAO: Cap.{m['capitulo']} {m['titulo']}"
        self.l_titulo.config(text="DC CORP" + (cap if cap else ""))

    # ------------------------------------------------------------ cena / balao

    def _montar_cena(self):
        self.f_cena = tk.Frame(self, bg=U["fundo"])
        self.f_bal = tk.Frame(self.f_cena, bg=U["painel"], height=170)
        self.f_bal.pack(fill="x", side="bottom")
        self.f_bal.pack_propagate(False)
        self.canvas = tk.Canvas(self.f_cena, bg="#0b0e14", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.b_nome = tk.Label(self.f_bal, text="", font=self.f_bal,
                               fg=U["ciano"], bg=U["painel"])
        self.b_nome.pack(anchor="w", padx=22, pady=(12, 0))
        self.b_txt = tk.Label(self.f_bal, text="", font=self.f_txt,
                              fg=U["texto"], bg=U["painel"], justify="left",
                              wraplength=1080, anchor="w")
        self.b_txt.pack(anchor="w", padx=22, pady=(4, 0))
        self.b_btn = tk.Button(self.f_bal, text="continuar ->", font=self.f_nrm,
                               fg=U["fundo"], bg=U["ciano"], activebackground=U["roxo"],
                               activeforeground=U["texto"], bd=0, padx=14, pady=4,
                               command=self._proxima_fala)
        self.b_btn.place(relx=0.98, rely=0.93, anchor="se")

    def _limpar_cena(self):
        self.canvas.delete("all")
        self.b_nome.config(text="")
        self.b_txt.config(text="")
        self.b_btn.config(state="disabled")

    def _ir_cena(self, mid):
        self.f_missao.pack_forget()
        self.f_cena.pack(fill="both", expand=True)
        self.mid = mid
        self._atualizar_hud()
        self._falas = list(core.MISSOES[mid]["cena_intro"])
        self._fal_idx = 0
        self._desenhar_cenario(mid)
        self._proxima_fala()

    def _proxima_fala(self):
        if not getattr(self, "_falas", []):
            return
        if self._fal_idx >= len(self._falas):
            self.b_nome.config(text="[ fim da cena ]")
            self.b_txt.config(text="Seu terminal esta pronto. Bora trabalhar!")
            self.b_btn.config(text="abrir terminal ->", state="normal",
                              command=self._abrir_missao)
            return
        falas = self._falas
        nome_npc = core.MISSOES[self.mid]["npc"].split("(")[0].strip()
        self.b_nome.config(text=nome_npc or "DC CORP",
                           fg=NPC_CORES.get(nome_npc.split(" ")[-1], U["ciano"]))
        alvo = falas[self._fal_idx]
        if alvo.startswith('"'):
            alvo = alvo.strip('"')
        self._fal_idx += 1
        self._digitar(self.b_txt, alvo, self.b_btn)

    def _digitar(self, label, texto, btn):
        btn.config(state="disabled", text="...")
        idx = {"n": 0}

        def passo():
            txt = texto[: idx["n"]]
            label.config(text=txt)
            idx["n"] += 2
            if idx["n"] < len(texto):
                self.after(18, passo)
            else:
                label.config(text=texto)
                btn.config(state="normal", text="continuar ->")

        passo()

    # ------------------------------------------------------------ cenario procedural

    def _desenhar_cenario(self, mid):
        c = self.canvas
        c.delete("all")
        W, H = 1160, 470
        cap = core.MISSOES[mid]["capitulo"]
        ceu = (("#04060d", "#16284a") if cap in (1, 2) else
               ("#140b1f", "#5a2b8f") if cap == 4 else
               ("#10081d", "#c98a3f"))
        import random
        rng = random.Random(cap)
        sky = H - 90
        passos = 32
        for i in range(passos):
            t = i / (passos - 1)
            c.create_rectangle(0, int(sky * i / passos), W,
                               int(sky * (i + 1) / passos) + 1,
                               fill=self._grad(ceu[0], ceu[1], t), outline="")
        # estrelas / detalhes do ceu
        for _ in range(cap * 18):
            x = rng.randrange(10, W - 10)
            y = rng.randrange(10, 190)
            c.create_oval(x, y, x + 1, y + 1, fill="#cfe0ff", outline="")
        # predios ao fundo
        cortes = ["#141d2e", "#182338", "#101828", "#1c2840"]
        x = -20
        i = 0
        while x < W + 30:
            bw = rng.randrange(70, 150)
            bh = rng.randrange(180, 380)
            c.create_rectangle(x, H - 90 - bh, x + bw, H - 90,
                               fill=cortes[i % len(cortes)], outline="")
            for j in range(0, bh - 60, 34):
                xx = int(x + 12)
                while xx < int(x + bw) - 8:
                    acesa = rng.random() < 0.55
                    c.create_rectangle(xx, H - 76 - bh + j, xx + 12, H - 76 - bh + j + 10,
                                       fill="#f5c25a" if acesa else "#0b1120", outline="")
                    xx += 30
            i += 1
            x += bw + rng.randrange(6, 30)
        # chao
        c.create_rectangle(0, H - 90, W, H, fill="#05070c", outline="")
        # lagrima da DC no ceu
        c.create_oval(W - 220, 26, W - 160, 86, fill="#ff4f7b", outline="#ff8ba8")
        c.create_text(W - 190, 56, text="DC", fill="#1a0a14", font=self.f_grd)
        # firewall (cap 4) ganha muro escuro na frente
        if cap == 4:
            c.create_rectangle(0, H - 180, W, H - 150, fill="#0a0d14", outline="")
            x = 0
            while x < W:
                c.create_rectangle(x, H - 180, x + 26, H - 150, fill="#151c29", outline="")
                x += 58
        # silhueta do NPC
        nome_npc = core.MISSOES[mid]["npc"]
        cor_npc = U["roxo"]
        for k, v in NPC_CORES.items():
            if k.lower() in nome_npc.lower():
                cor_npc = v
        self._silhueta(200, H - 96, cor_npc, "npc")
        # voce (estagiario)
        self._silhueta(W - 230, H - 96, "#7d8aa0", "voce")

    @staticmethod
    def _grad(a, b, t):
        def ch(x, y):
            return round(int(x, 16) + (int(y, 16) - int(x, 16)) * t)
        return "#%02x%02x%02x" % (ch(a[1:3], b[1:3]), ch(a[3:5], b[3:5]), ch(a[5:7], b[5:7]))

    def _silhueta(self, x, y, cor, papel):
        c = self.canvas
        altura = 180 if papel == "npc" else 150
        larg = 60 if papel == "npc" else 50
        # sombra
        c.create_oval(x - 55, y - 12, x + 55, y + 2, fill="#000000", outline="")
        # corpo
        c.create_oval(x - larg, y - altura - 58, x + larg, y - altura + 40, fill=cor, outline="")
        c.create_oval(x - 24, y - altura - 130, x + 24, y - altura - 58, fill=cor, outline="")
        # bracos
        c.create_rectangle(x - larg - 8, y - altura - 10, x - larg + 10, y - altura + 46,
                           fill=cor, outline="")
        c.create_rectangle(x + larg - 10, y - altura - 10, x + larg + 8, y - altura + 46,
                           fill=cor, outline="")
        # pernas
        c.create_rectangle(x - 26, y - altura + 34, x - 6, y, fill=cor, outline="")
        c.create_rectangle(x + 6, y - altura + 34, x + 26, y, fill=cor, outline="")
        if papel == "npc":
            c.create_oval(x - 34, y - altura - 148, x + 34, y - altura - 82,
                          fill=cor, outline="#f0f2f7", width=3)
        else:
            c.create_oval(x - 22, y - altura - 126, x + 22, y - altura - 72,
                          fill=cor, outline="#f0f2f7", width=2)

    # ------------------------------------------------------------ tela de missao

    def _montar_missao(self):
        self.f_missao = tk.Frame(self, bg=U["fundo"])
        self.f_missao.columnconfigure(0, weight=3)
        self.f_missao.columnconfigure(1, weight=2)
        self.f_missao.rowconfigure(0, weight=1)

        # terminal
        p_term = tk.Frame(self.f_missao, bg=U["painel"], padx=10, pady=10)
        p_term.grid(row=0, column=0, sticky="nsew")
        self.term = tk.Text(p_term, bg=U["entrada"], fg=U["term"], insertbackground=U["term"],
                            font=self.f_txt, wrap="none", bd=0, padx=12, pady=10)
        self.term.tag_configure("dim", foreground=U["term_dim"])
        self.term.pack(fill="both", expand=True)
        self.ent = tk.Entry(p_term, bg=U["entrada"], fg=U["texto"],
                            insertbackground=U["ciano"], font=self.f_txt, bd=0,
                            highlightthickness=1, highlightbackground=U["borda"])
        self.ent.pack(fill="x", pady=(8, 0), ipady=6)
        self.ent.bind("<Return>", lambda e: self._enviar())

        # painel direito
        p_dir = tk.Frame(self.f_missao, bg=U["painel"], padx=10, pady=10)
        p_dir.grid(row=0, column=1, sticky="nsew")
        tb = tk.Frame(p_dir, bg=U["painel2"])
        tb.pack(fill="x", pady=(0, 8))
        self.b_detonado = tk.Button(tb, text="DETONADO", font=self.f_nrm,
                                    bg=U["painel2"], fg=U["ciano"], bd=0,
                                    command=lambda: self._painel_detonado())
        self.b_detonado.pack(side="left", padx=(0, 6))
        self.b_obj = tk.Button(tb, text="MISSAO", font=self.f_nrm,
                               bg=U["painel2"], fg=U["amarelo"], bd=0,
                               command=lambda: self._painel_objetivo())
        self.b_obj.pack(side="left", padx=(0, 6))
        self.b_prog = tk.Button(tb, text="PROGRESSO", font=self.f_nrm,
                                bg=U["painel2"], fg=U["verde"], bd=0,
                                command=lambda: self._painel_dinamico(self.tg.ver_progresso))
        self.b_prog.pack(side="left", padx=(0, 6))
        self.b_dica = tk.Button(tb, text="DICA", font=self.f_nrm,
                                bg=U["painel2"], fg=U["vermelho"], bd=0,
                                command=lambda: self._painel_dinamico(self.tg.dica))
        self.b_dica.pack(side="left")
        self.b_trilha = tk.Button(tb, text="TRILHA", font=self.f_nrm,
                                  bg=U["painel2"], fg=U["roxo"], bd=0,
                                  command=self._painel_trilha)
        self.b_trilha.pack(side="left", padx=(6, 0))
        self.guia = tk.Text(p_dir, bg=U["painel2"], fg=U["texto"],
                            font=self.f_det, wrap="word", bd=0, padx=10, pady=10)
        self.guia.pack(fill="both", expand=True)

    def _painel_detonado(self):
        if not self.mid:
            return
        txt = ["== DETONADO - GUIA PASSO A PASSO ==",
               ""]
        for m in core.MISSOES.values():
            if m["id"] == self.mid:
                txt.append(f"CAPITULO {m['capitulo']}: {m['titulo']}")
                txt.append(f"  {m['ambientacao']}")
                txt.append("")
                txt.append(f"OBJETIVO: {m['objetivo']}")
                txt.append("")
                txt.append("[ passo a passo ]")
                txt += ["  " + g for g in m["guia"]]
        self._set_guia("\n".join(txt))

    def _painel_objetivo(self):
        if not self.mid:
            return
        m = core.MISSOES[self.mid]
        self._set_guia(f"CAPITULO {m['capitulo']}: {m['titulo']}\n\n"
                       f"{m['ambientacao']}\n\n"
                       f"OBJETIVO: {m['objetivo']}\n\n"
                       f"APRENDE: {m['aprender']}\n\n"
                       f"RECOMPENSA: {m['recompensa']} XP")

    def _painel_dinamico(self, fn):
        try:
            txt = fn() if self.tg else "ainda nao ha terminal ativo."
        except Exception as exc:
            txt = f"(erro ao consultar: {exc})"
        self._set_guia(txt)

    def _painel_trilha(self):
        self._set_guia(core.texto_trilha(self.jogo))

    def _set_guia(self, txt):
        self.guia.config(state="normal")
        self.guia.delete("1.0", "end")
        self.guia.insert("1.0", txt)
        self.guia.config(state="disabled")

    def _abrir_missao(self):
        if not self.mid:
            return
        if self.thread and self.thread.is_alive():
            return
        self._overlay_esconder()
        self.f_cena.pack_forget()
        self.f_missao.pack(fill="both", expand=True)
        self.term.config(state="normal")
        self.term.delete("1.0", "end")
        self.term.config(state="disabled")
        self.ent.config(state="normal")
        self.ent.delete(0, "end")
        self._painel_detonado()
        self.tg = core.TerminalGame(self.jogo, self.mid)
        self._stdout_ant = sys.stdout
        self._ler_orig = core.ler
        self._motd_orig = core.motd
        sys.stdout = _Redir(self.fila_saida)
        core.INTERATIVO = False
        core.ler = self._ler
        core.motd = _noop
        self.thread = threading.Thread(target=self._rodar_thread, daemon=True)
        self.thread.start()
        self.ent.focus_set()

    def _rodar_thread(self):
        try:
            self.tg.jogar()
        except Exception as exc:
            self.fila_saida.put(("out", f"\n[erro-interno-debug] {exc}\n"))
        finally:
            sys.stdout = self._stdout_ant
            core.ler = self._ler_orig
            core.motd = self._motd_orig
            self.fila_saida.put(("fim", self.mid in self.jogo.missoes))

    def _ler(self, prompt=""):
        self.fila_saida.put(("prompt", prompt))
        return self.fila_entrada.get()

    def _enviar(self):
        if not self.thread or not self.thread.is_alive():
            return
        txt = self.ent.get().strip()
        if not txt:
            return
        self.term.config(state="normal")
        self.term.insert("end", txt + "\n")
        self.term.config(state="disabled")
        self.term.see("end")
        self.ent.delete(0, "end")
        self.fila_entrada.put(txt)

    # ------------------------------------------------------------ drenagem da fila

    def _drenar_saidas(self):
        try:
            while True:
                tipo, valor = self.fila_saida.get_nowait()
                if tipo == "out":
                    txt = ANSI.sub("", valor)
                    if txt:
                        self.term.config(state="normal")
                        self.term.insert("end", txt)
                        self.term.config(state="disabled")
                        self.term.see("end")
                elif tipo == "prompt":
                    self.term.config(state="normal")
                    self.term.insert("end", ANSI.sub("", valor))
                    self.term.config(state="disabled")
                    self.term.see("end")
                    self.ent.focus_set()
                elif tipo == "fim":
                    self._fim_missao(valor)
        except queue.Empty:
            pass
        self.after(50, self._drenar_saidas)

    def _fim_missao(self, concluida):
        self.ent.config(state="disabled")
        recomp = core.MISSOES[self.mid]["recompensa"] if self.mid else 0
        self._atualizar_hud()
        if concluida:
            self._overlay(f"MISSAO CUMPRIDA\n\nCap.{core.MISSOES[self.mid]['capitulo']} concluido!\n\n"
                          f"+{recomp} XP\n\nXP total: {self.jogo.xp}",
                          "Continuar", self._depois_missao)
        else:
            self._overlay("Missao encerrada sem concluir.\n\n(O save so grava missao vencida.)",
                          "Tentar de novo", self._abrir_missao)

    def _depois_missao(self):
        self._overlay_esconder()
        self.tg = None
        self.thread = None
        prox = core.proxima_missao(self.jogo)
        if prox:
            self._ir_cena(prox)
        else:
            self._ir_final()

    # ------------------------------------------------------------ overlay

    def _montar_overlay(self):
        self.overlay = tk.Frame(self, bg="#020409")
        self.painel_ov = tk.Frame(self.overlay, bg=U["painel"], padx=40, pady=34,
                                  highlightthickness=2, highlightbackground=U["borda"])
        self.painel_ov.place(relx=0.5, rely=0.45, anchor="center")
        self.ov_txt = tk.Label(self.painel_ov, text="", font=self.f_tit, fg=U["texto"],
                               bg=U["painel"], justify="center")
        self.ov_txt.pack()
        self.ov_btn = tk.Button(self.painel_ov, text="", font=self.f_grd,
                                fg=U["fundo"], bg=U["ciano"], bd=0, padx=18, pady=6)
        self.ov_btn.pack(pady=(18, 0))

    def _overlay(self, txt, btntxt, comando):
        self.ov_txt.config(text=txt)
        self.ov_btn.config(text=btntxt)
        self.ov_btn.config(command=comando)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _overlay_esconder(self):
        self.overlay.place_forget()

    # ------------------------------------------------------------ titulo / final

    def _ir_titulo(self):
        self.f_cena.pack_forget()
        self.f_missao.pack_forget()
        self._painel_overlay_titulo = tk.Frame(self, bg=U["fundo"])
        self._painel_overlay_titulo.pack(fill="both", expand=True)
        banner = ("   ________  ____  ______    ____     _____\n"
                  "  / __/  _/  |/  / / __/ /   / __/    / ___/\n"
                  " / _// / / /|_/ / / _// /__ / _/     / /__\n"
                  "/___/___/_/  /_/ /___/____/___/      \\___/\n\n"
                  "  SISTEMA DE TREINAMENTO E PROGRESSAO")
        tk.Label(self._painel_overlay_titulo, text=banner, font=self.f_tit,
                 fg=U["ciano"], bg=U["fundo"], justify="left").pack(pady=(90, 6))
        tk.Label(self._painel_overlay_titulo, text=core.cargo_atual(self.jogo.xp),
                 font=self.f_grd, fg=U["amarelo"], bg=U["fundo"]).pack()
        if self.jogo.missoes:
            tk.Label(self._painel_overlay_titulo,
                     text=f"(save encontrado: {self.jogo.xp} XP, "
                          f"{len(self.jogo.missoes)} missoes concluidas)",
                     font=self.f_nrm, fg=U["dim"], bg=U["fundo"]).pack(pady=(6, 0))
        btns = tk.Frame(self._painel_overlay_titulo, bg=U["fundo"])
        btns.pack(pady=30)
        start = tk.Button(btns, text="INICIAR / CONTINUAR", font=self.f_grd,
                          fg=U["fundo"], bg=U["ciano"], bd=0, padx=20, pady=8,
                          command=lambda: (self._painel_overlay_titulo.pack_forget(),
                                           self._depois_missao()))
        start.pack(side="left", padx=10)
        quit = tk.Button(btns, text="SAIR", font=self.f_grd,
                         fg=U["texto"], bg=U["painel2"], bd=0, padx=20, pady=8,
                         command=self.destroy)
        quit.pack(side="left", padx=10)

    def _ir_final(self):
        self.f_cena.pack_forget()
        self.f_missao.pack_forget()
        self._painel_overlay_titulo = tk.Frame(self, bg=U["fundo"])
        self._painel_overlay_titulo.pack(fill="both", expand=True)
        champ = ("  ====================\n"
                 "   TODAS AS MISSOES\n"
                 "      CONCLUIDAS\n"
                 "  ====================")
        tk.Label(self._painel_overlay_titulo, text=champ, font=self.f_tit,
                 fg=U["verde"], bg=U["fundo"], justify="center").pack(pady=(110, 10))
        tk.Label(self._painel_overlay_titulo, text=f"{core.cargo_atual(self.jogo.xp)}"
                                                   f"  |  {self.jogo.xp} XP",
                 font=self.f_grd, fg=U["amarelo"], bg=U["fundo"]).pack()
        tk.Button(self._painel_overlay_titulo, text="O VALENTE APROVOU - SAIR",
                  font=self.f_grd, fg=U["fundo"], bg=U["verde"], bd=0,
                  padx=20, pady=8, command=self.destroy).pack(pady=30)

    # ------------------------------------------------------------ fechar

    def _fechar(self):
        self.destroy()


class _Redir:
    def __init__(self, fila):
        self.fila = fila

    def write(self, txt):
        if txt.strip() or txt.endswith("\n"):
            self.fila.put(("out", txt))
        return len(txt)

    def flush(self):
        pass


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
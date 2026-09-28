# Modulo 5 — VLAN, VTP e STP (Camada 2 avancada)

> Trilha: Redes | Mes 1, Semana 2 | Aula 5

## Objetivo

Separar logicamente uma LAN em redes menores (VLAN), entender por que STP impede loops e o que o VTP faz (ou deixou de fazer). E o coracao do Projeto 1 (topologia com switches isolando redes).

## Teoria

### VLAN (Virtual LAN)

- Divide um switch **logicamente**: criam-se "redes locais virtuais". Uma VLAN = um dominio de broadcast separado.
- Comportamento:
  - **MACs de VLANs diferentes nao se enxergam** na camada 2 (isolamento).
  - Para conversarem: precisa de **camada 3 (roteador)** ou **L3 switch**.
- Usos: departamentos (TI, RH, Guests), seguranca (isolar servidores/guest), qualidade de servico.

### Tag 802.1Q (o "etiqueta" da VLAN)

- No frame Ethernet entra o campo **VLAN ID (12 bits, 1-4094)**.
- **Access port:** pertence a 1 VLAN; sai sem tag. Ligado a PC/camera/impressora.
- **Trunk port:** leva varias VLANs; sai **com tag**. Ligado switch<->switch, switch<->roteador.
- **Native VLAN** (default 1): trafego nao etiquetado que vem/va num trunk. **Regra: mudar a native VLAN default** (seguranca — evita "VLAN hopping").

### VTP (VLAN Trunking Protocol) — quase historico

- Sincroniza VLANs entre switches de um dominio VTP.
- Versoes 1/2 tinham um risco serio: um switch "corrompido"/desatualizado pode trocar as VLANs de um dominio inteiro — por isso na pratica **desabilite VTP e configure VLANs manualmente**. Hoje na maioria dos labs/empresas: `vtp mode transparent` ou off.

### STP (Spanning Tree Protocol)

- Para que: em rede com **caminhos redundantes** (2 cabos), sem controle haveria **loop**: frames circulando infinitamente, switch com MAC flutuando, broadcast storm (tempestade de broadcast) derrubando a LAN.
- STP constroi uma **arvore sem loops**: elege **root bridge** e bloqueia portas redundantas que criariam loop.
- Processo simplificado:
  1. Elege-se **Root Bridge** (menor bridge ID = prioridade + MAC).
  2. Cada switch escolhe sua **Root Port** (melhor caminho ate a raiz).
  3. Cada segmento elege um **Designated Port**; os demais ficam **blocking**.
- Estados de porta: Blocking -> Listening -> Learning -> Forwarding.
- **Tipos:** STP classico (802.1D, lento ~30s), RSTP (802.1w, rapido ~2s), MSTP (multi-instancia).
- **PortFast:** porta de acesso (PC) entra direto em forwarding — evita espera de 30s. Em trunk: handshake.

## Exemplo pratico (o caso clasico)

- Switch A e switch B ligados por trunk.
- VLAN 10 = TI, VLAN 20 = RH, VLAN 30 = Guests.
- Sem roteamento: PC da VLAN 10 nao ve PC da VLAN 20 (isolamento).
- Adicionar um roteador com subinterfaces (router-on-a-stick) faz VLANs conversarem:
  ```
  interface g0/0.10
    encapsulation dot1Q 10
    ip address 10.0.10.1 255.255.255.0
  interface g0/0.20
    encapsulation dot1Q 20
    ip address 10.0.20.1 255.255.255.0
  ```

## Lab guiado (60 min) — Nucleo do Projeto 1

Topologia: **1 switch + 1 switch (trunk) + 4 PCs + 1 roteador**.

1. **Crie VLANs** no switch:
   ```
   vlan 10
     name TI
   vlan 20
     name RH
   ```
2. **Portas de acesso:**
   ```
   interface fastEthernet 0/1          (PC-A)
     switchport mode access
     switchport access vlan 10
   ```
   Repita para PC-B (vlan 10), PC-C (vlan 20), PC-D (vlan 20).
3. **Trunk entre switches:**
   ```
   interface fastEthernet 0/24
     switchport mode trunk
     switchport trunk allowed vlan 10,20
   ```
4. Configure IPs: PCs VLAN 10: 10.0.10.x/24; VLAN 20: 10.0.20.x/24.
5. **Testes esperados:**
   - Ping PC-A -> PC-B (mesma VLAN): OK (mesmo dominio broadcast).
   - Ping PC-A -> PC-C (VLANs diferentes): **FALHA** (sem roteador) -> prove o isolamento.
6. Roteador com subinterfaces (exemplo acima) + IP dos PCs com gateway nas respectivas VLANs.
7. Ping PC-A -> PC-C: agora OK (roteado).
8. (Opcional) no Wireshark no trunk, filtre `vlan` e veja a **tag 802.1Q** nos frames.
9. (Opcional) no lab com 2 switches ligados em ANEL, rode `show spanning-tree` sem STP ativo (se o simulador permitir desligar — observe tempestade); depois `spanning-tree mode rapid-pvst` e veja portas em blocking/forwarding.

## Verificacao — "sei que aprendi quando..."

- [ ] Crio VLANs, configuro access e trunk no switch sem consulta
- [ ] Explico o isolamento: motivo por que VLAN 10 nao conversa com VLAN 20 na camada 2
- [ ] Descrevo o que a tag 802.1Q adiciona ao frame e onde ela aparece (trunk)
- [ ] Explico em 2 frases o problema que o STP resolver (loop -> broadcast storm)
- [ ] Sei que VTP e normalmente desabilitado por seguranca (config manual das VLANs)

## Conexao com o roadmap

- Este e o lab central do **Projeto 1 (FA-1)**. Será usado de novo em:
  - Seguranca: VLAN guest/floor separation, Port Security (Mes 4).
  - Projeto 4: 3 VLANs + firewalls entre elas.

## Para ir alem (opcional)

- Ler mais: "802.1X" (autenticação de porta — futuro: RADIUS).
- Testar "private VLANs" em um switch mais avancado (isolamento de membros da mesma VLAN).
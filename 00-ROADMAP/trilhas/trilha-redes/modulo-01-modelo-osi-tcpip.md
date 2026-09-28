# Modulo 1 — Modelo OSI e Modelo TCP/IP

> Trilha: Redes | Mes 1, Semana 1 | Aula 1

## Objetivo

Entender que a comunicacao em rede nao e "magia": e dividida em camadas, cada uma com uma funcao. Ao terminar, voce explica o caminho de um dado do app ate o cabo e vice-versa.

## Teoria

### A ideia de camadas

Uma rede entrega dados do ponto A ao B. Como isso e complexo, dividiu-se o problema em **camadas**. Cada camada:

- so conversa com a camada imediatamente acima e abaixo;
- tem uma funcao unica;
- usa "servicos" da camada de baixo e presta "servicos" para a de cima.

Analogia: **logistica de entrega de uma carta**. Voce (aplicacao) escreve a mensagem e entrega ao correio (transporte). O correio nao precisa entender o conteudo — ele so precisa saber **o destino** (carta errada seria um baguncamento de camadas). Por tras, o caminhao cuida do endereco fisico, o aviao do trajeto, etc. Cada etapa adiciona/tira o "envelope" certo.

### Modelo OSI (referencia, 7 camadas)

| Camada | Nome | Funcao | Exemplo de equipamento |
|--------|------|--------|------------------------|
| 7 | Aplicacao | Interface com o usuario (dados do app) | navegador, e-mail, HTTP |
| 6 | Apresentacao | Formata/criptografa dados (codificacao) | SSL, JPEG, UTF-8 (conceito) |
| 5 | Sessao | Abre/fecha sessao entre apps, checkpoints | autenticacao de conexao |
| 4 | Transporte | Entrega fim-a-fim, confiabilidade, portas | TCP / UDP |
| 3 | Rede | Enderecamento logico (IP), roteamento | Roteador |
| 2 | Enlace | Acesso ao meio, MAC, frames | Switch |
| 1 | Fisica | Bits no meio fisico (cabo, fibra, ondas) | cabos, placas, radio |

Mnemonico (de baixo p/ cima): **"Pra Fibra **? (nao memorizar mnemonicos engessados — o que importa e a funcao)"** — recomendado: criar o seu proprio.

### Modelo TCP/IP (operacional, 4 camadas)

O mundo real usa o TCP/IP (mais simples). Correspondencia aproximada com OSI:

| TCP/IP | Faz o papel de (OSI) | Principais protocolos |
|--------|----------------------|-----------------------|
| Aplicacao | 7 + 6 + 5 | HTTP, DNS, SMTP, SSH, FTP, DHCP |
| Transporte | 4 | TCP, UDP |
| Rede (Internet) | 3 | IP, ICMP, ARP* |
| Host/rede (Acesso) | 2 + 1 | Ethernet, Wi-Fi |

\* ARP na camada 3/2 (faz ponte IP <-> MAC) — ver modulo de Camada 2.

### O que importa de verdade

- **Dados descem** do app ate o cabo (empacotando em cada camada) e **sobem** no destino (desempacotando).
- Cada camada adiciona seu **cabecalho** (header). Resultado: o dado cresce a cada camada (uma "matrioska de datas").
- App <-> processador: **mensagem**; Transporte -> **segmento**; Rede -> **pacote**; Enlace -> **frame**; Fisica -> **bits**. (Nomenclatura-cliche, cobra em prova CCNA.)

## Exemplo pratico: voce acessa o site `exemplo.com`

1. **Aplicacao:** HTTPS gera a requisicao (HTTP GET).
2. **Transporte:** TCP corta, numera, garante entrega (porta 443 destino).
3. **Rede:** adiciona IP de origem/destino (IP do seu PC -> IP do servidor).
4. **Enlace:** frame com MACs (gateway MAC -> ...).
5. **Fisica:** bits trafegam no cabo/wifi.

No servidor, o caminho e inverso ate o HTTPS processar a resposta.

## Lab guiado (30 min)

Objetivo: **ver camadas na pratica** com Wireshark (ou tcpdump, se Linux).

1. Baixe/instale o Wireshark. *(Se nao tiver, alternativa: `ping` + `tracert` no CMD)*
2. Inicie a captura na interface ativa (wifi ou cabo).
3. No navegador, acesse `exemplo.com` e recarregue.
4. Pause a captura e filtre: `http` ou `dns`.
5. Abra um pacote. Note os "envelopes" empilhados no painel de detalhes:
   - **Frame** (Fisica/Enlace: dados do quadro)
   - **Ethernet II** (Enlace: MAC origem/destino)
   - **Internet Protocol** (Rede: IP origem/destino, TTL)
   - **TCP** (Transporte: porta 443, sequencia)
   - **HTTP** (Aplicacao)
6. Marcou cada camada que a Teoria acima descreveu na tela do Wireshark.

Roteiro alternativo sem Wireshark:
- `ipconfig` (ver seu IP, que e camada 3)
- `ipconfig /all` (MAC do adaptador, que e camada 2)
- `ping exemplo.com` (ICMP, usa IP para resolver)
- `tracert -d exemplo.com` (mostra saltos de roteamento)

## Verificacao — "sei que aprendi quando..."

- [ ] Desenho (sem olhar) a pilha OSI de baixo para cima com a funcao de cada camada
- [ ] Explico a diferenca OTIMIZADA entre OSI (referencia) e TCP/IP (operacional)
- [ ] No Wireshark, identifiquei manualmente: frame, Ethernet, IP, TCP, HTTP num unico pacote
- [ ] Sei dizer o header que cada camada adiciona (ethernet, IP, TCP)
- [ ] Resumo em 1 frase: "rede e dividida em camadas para separar responsabilidades e permitir interoperabilidade"

## Conexao com o roadmap

- Este modulo e a fundacao dos M1 e M4 (Rede/Seguranca). A camada 4 (transport) sera detalhada no Modulo 7; a camada 2 no Modulo 4/5; a camada 3 no Modulo 2 e 6.

## Para ir alem (opcional)

- Artigo: "How the OSI Model Works" (compare com o que leu aqui).
- Padrao de cabos: RJ45 qual categoria vs blindagem (fisica) — apenas curiosidade agora.
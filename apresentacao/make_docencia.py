"""Gera apresentacao/docencia/index.html — aula de estágio docência (90 min)
"Gerenciamento de Recursos em Redes SDN", no formato Beamer UDESC-CCT da v4.

Uso (de dentro de apresentacao/docencia):  python3 make_docencia.py .

Reaproveita de ../v4/index.html o CSS (bloco <style>), o script da footline e alguns slides do QCTP
(arquitetura, vídeos e resultados), procurados pelo título <h2>.
"""
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
V4 = (OUT / ".." / "v4" / "index.html").resolve().read_text(encoding="utf-8")

CSS_V4 = re.search(r"<style>(.*?)</style>", V4, re.S).group(1)


def v4_section(title):
    """Devolve o <section> da v4 cujo <h2> começa com `title`."""
    for m in re.finditer(r"<section data-timing=\"\d+\">.*?</section>", V4, re.S):
        if re.search(r"<h2>" + re.escape(title), m.group(0)):
            return m.group(0)
    raise KeyError(title)


def retime(sec, t):
    return re.sub(r'data-timing="\d+"', f'data-timing="{t}"', sec, count=1)


EXTRA_CSS = r"""
/* --- docência --- */
.toc li.off{color:#a9a9d6}.toc li.off .n{background:#a9a9d6}
.toc.sm li{font-size:27px;margin:0 0 17px!important}
.code{font-family:"DejaVu Sans Mono",monospace;font-size:16.5px;background:#f4f4fb;border-left:4px solid var(--st);
      padding:10px 14px;white-space:pre;line-height:1.38;color:#111;border-radius:3px}
.code .k{color:#3333b2;font-weight:700}.code .c{color:#777}
table.t.sm{font-size:23px}table.t.sm th,table.t.sm td{padding:9px 11px;vertical-align:top;line-height:1.28}
table.t.md{font-size:24px}table.t.md th,table.t.md td{padding:11px 12px;vertical-align:top;line-height:1.3}
.cols>table{align-self:start}
.layer span{font-size:22px!important}
.ex h3{background:var(--signal)!important}
.ex{background:#fff6e6!important}
.g22{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;height:100%}
.g22>div{display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fafaff;border:1px solid var(--line);border-radius:5px;padding:6px}
.g22 img{max-width:100%;max-height:175px}
.g22 .cap{font-size:17px}
.icons{display:flex;gap:26px;align-items:center;justify-content:center;margin:6px 0}
.icons img{height:84px}
.vs{font-size:34px;color:var(--st);font-weight:700}
.q{font-size:24px;color:var(--signal);font-weight:700;margin-top:10px}
.small{font-size:21px!important;line-height:1.38!important}
.card ul li{font-size:22px;line-height:1.35}
.figbox{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%}
.secpg .tbox{background:var(--st);color:#fff;border-radius:9px;padding:20px 40px;box-shadow:3px 4px 7px rgba(0,0,0,.35);text-align:center;font-size:40px;margin:10px auto 30px;width:70%}
"""

FOOT_TITLE = "Gerenciamento de Recursos em SDN · PPGCAP"

SECS = ["Redes de computadores e SDN no mundo real",
        "Fluxos e Qualidade de Serviço",
        "Arquitetura SDN: controlador, interfaces, OpenFlow e P4",
        "Gerenciamento de redes: convencional × SDN",
        "QoS em redes SDN",
        "FLOWPRI-SDN",
        "QCTP: levando o QoS ao transporte",
        "Fechamento"]

slides = []


def S(t, title, body, notes):
    slides.append(f"""<section data-timing="{t}">
  <div class="bar"><h2>{title}</h2></div>
  <div class="body">{body}</div>
  <aside class="notes">{notes}</aside>
</section>""")


def divider(i, t=20, notes="Transição de seção."):
    items = "\n".join(
        f'    <li class="{"" if k == i else "off"}"><span class="n">{k + 1}</span>{s}</li>'
        for k, s in enumerate(SECS))
    slides.append(f"""<section data-timing="{t}">
  <div class="bar"><h2>{SECS[i]}</h2></div>
  <div class="body"><ol class="toc sm">
{items}
  </ol></div>
  <aside class="notes">{notes}</aside>
</section>""")


def img(src, h=420, cap=None, style="", force=False):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    hh = f"height:{h}px;max-width:100%;object-fit:contain" if force else f"max-height:{h}px"
    return f'<div class="figbox"><img class="fig" src="media/{src}" style="{hh};{style}">{c}</div>'


def vid(src):
    return f'<div class="vid" style="height:100%"><video data-autoplay muted controls src="media/{src}"></video></div>'


# ===================================================================================== ABERTURA
slides.append("""<section data-timing="40">
  <div class="tp">
    <div class="tbox"><h1>Gerenciamento de Recursos em Redes SDN</h1>
      <div class="st">fluxos, QoS, SDN/P4, gerenciamento e os frameworks FLOWPRI-SDN e QCTP</div></div>
    <div class="au">Nilton José Mocelin Júnior<sup>1</sup></div>
    <div class="inst"><sup>1</sup>Dept. de Ciência da Computação - DCC<br>
      Programa de Pós-Graduação em Computação Aplicada - PPGCAP<br>
      Universidade do Estado de Santa Catarina - UDESC<br>
      89219-710 Joinville, SC, Brasil<br>nilton.junior@edu.udesc.br</div>
    <div class="dt">Estágio de Docência · 10 de novembro de 2026</div>
    <div class="logos"><img src="media/udesc/ppgcap.jpeg" style="height:84px">
      <img src="media/udesc/udesc.png" style="height:84px"><img src="media/udesc/dcclogo.png" style="height:62px"></div>
  </div>
  <aside class="notes">Apresentar-se. Pergunta de abertura para a turma: "quando a videochamada trava, de quem é a culpa?" Deixar 2–3 respostas e seguir. (40 s)</aside>
</section>""")

slides.append("""<section data-timing="30">
  <div class="bar"><h2>Agenda da Aula</h2></div>
  <div class="body"><ol class="toc sm">
""" + "\n".join(f'    <li><span class="n">{k + 1}</span>{s}</li>' for k, s in enumerate(SECS)) + """
  </ol></div>
  <aside class="notes">Roteiro de 90 min: ~10 min por seção, perguntas no fim. (30 s)</aside>
</section>""")

S(60, "Objetivos da aula", """<div class="cols c2">
  <div class="card"><h3>Ao final, você deve saber explicar</h3><ul>
    <li>por que fluxos disputam recursos e como isso vira atraso, jitter e perda</li>
    <li>a diferença entre <b>prioridade</b> e <b>requisito</b> de QoS</li>
    <li>planos, interfaces e regras de uma rede SDN (OpenFlow e P4)</li>
    <li>como SNMP, NETCONF e NetFlow se relacionam com o SDN</li></ul></div>
  <div class="card"><h3>… e saber usar</h3><ul>
    <li>filas HTB e regras <i>meter</i> para reservar banda</li>
    <li>marcação DSCP, VLAN e classificação de tráfego</li>
    <li>a lógica de um framework de QoS multi-domínio (FLOWPRI-SDN)</li>
    <li>a ideia de um transporte que negocia QoS (QCTP)</li></ul></div>
</div>""", "Objetivos de aprendizagem: voltar a eles no resumo final. (1 min)")

# ===================================================================================== 1. REDES
divider(0, notes="Primeiro: por que gerenciar recursos? Porque a rede cresceu e virou infraestrutura crítica.")

S(70, "Crescimento das redes de comunicação", """<div class="cols c2-wide">
  """ + img("odg/crescimento.png", 440, force=True, cap="Conexões ativas no mundo, IoT × não-IoT (IoT Analytics, dados até 2020)") + """
  <div class="stack">
    <div class="card"><h3>Mais dispositivos</h3><p>IoT já supera os dispositivos “tradicionais” — sensores, câmeras, carros, máquinas.</p></div>
    <div class="card"><h3>Mais exigência</h3><p>Vídeo, jogos, telemedicina e indústria têm <b>requisitos</b> de atraso e banda.</p></div>
    <div class="card"><h3>Mesmos enlaces</h3><p>Todos disputam os mesmos recursos finitos.</p></div>
  </div></div>""",
  "O gráfico é de 2020; atualizar o número com o relatório mais recente da IoT Analytics (State of IoT) antes da aula — conferir o valor. A mensagem: mais dispositivos e mais aplicações exigentes no mesmo enlace. (1 min 10)")

S(80, "A Internet: uma rede de redes", """<div class="cols c2">
  <div class="stack">
    <ul class="lead">
      <li>Nasce com a ARPANET (1969); hoje interliga dezenas de milhares de <b>Sistemas Autônomos</b> (AS).</li>
      <li><b>AS</b>: conjunto de redes IP sob uma mesma gerência técnica e política de roteamento.</li>
      <li>ASs trocam rotas com o <b>BGP</b> (RFC 4271).</li>
      <li>Relações comerciais: <b>trânsito</b> (pago) e <b>peering</b> (troca de tráfego).</li>
    </ul>
    <p class="q">Ninguém controla a Internet inteira — e o QoS também não atravessa domínios sozinho.</p>
  </div>
  """ + img("odg/tiers.png", 420, "ISPs Tier 1, 2 e 3: trânsito e peering") + """
</div>""", "Corrigido do rascunho: a ARPANET é de 1969. Enfatizar que cada AS tem dono e política própria — é isso que torna o QoS multi-domínio difícil. (1 min 20)")

S(60, "Pontos de troca de tráfego (IXP/PTT)", """<div class="cols c2">
  """ + img("odg/ixp.png", 400, "IXP: vários ASs trocam tráfego num ponto comum") + """
  """ + img("odg/ptt.png", 400, "IX.br: matriz de tráfego entre participantes") + """
</div>""", "IXP reduz custo e latência: tráfego local fica local. O IX.br (São Paulo) é um dos maiores do mundo em volume de tráfego. (1 min)")

S(60, "Os provedores de serviço (ISPs)", """<div class="cols c2-wide">
  <div class="card"><h3>O que um ISP vende</h3><ul>
    <li>acesso à Internet (banda contratada)</li>
    <li>serviços de e-mail, armazenamento, hospedagem</li>
    <li>rotas e canais privados (VPN, MPLS, enlaces dedicados)</li>
    <li>coleta de dados e anúncios de serviços</li></ul>
    <p class="q" style="font-size:22px">Quem garante a banda que o cliente pagou? Hoje: contrato (SLA) + superdimensionamento.</p></div>
  """ + img("odg/isp_as.png", 430, "Entidade → ISP → PTT → outros ASs") + """
</div>""", "Gancho para QoS: o cliente paga um SLA, mas raramente consegue verificar se foi cumprido. Isso volta no QoSBlockchain e no QCTP. (1 min)")

S(70, "Tipos de redes", """<div class="cols c2-wide">
  """ + img("odg/topologias.jpg", 440, "Topologias: leaf-spine (datacenter), arquitetura por serviços, hub-spoke com MEC e overlay") + """
  <div class="card"><h3>Onde cada uma aparece</h3><ul class="small">
    <li><b>Acesso</b>: residencial, Wi-Fi, rádio móvel</li>
    <li><b>Metro / backbone</b>: ISPs, transporte óptico, MPLS</li>
    <li><b>Datacenter</b>: Clos / leaf-spine, alta densidade</li>
    <li><b>Móvel (5G)</b>: núcleo baseado em serviços, borda (MEC)</li>
    <li><b>WAN corporativa</b>: SD-WAN, VPNs</li>
    <li><b>Overlay</b>: túneis VXLAN/GRE sobre a rede física</li></ul></div>
</div>""", "Cada tipo tem um problema de gerenciamento diferente; o SDN aparece em todos, com nomes diferentes. (1 min 10)")

S(80, "Da caixa preta à rede programável", """<div class="cols c2">
  <div class="card"><h3>Rede tradicional</h3><ul>
    <li>cada roteador tem seu <b>próprio plano de controle</b> (OSPF, BGP…)</li>
    <li>configuração por CLI proprietária, equipamento a equipamento</li>
    <li>novas funções dependem do fabricante → <b>ossificação</b></li>
    <li>decisões locais: um enlace congestiona enquanto outro fica ocioso</li></ul></div>
  <div class="card"><h3>Rede definida por software (SDN)</h3><ul>
    <li><b>separa</b> plano de controle e plano de dados</li>
    <li>controlador com <b>visão global</b> da topologia</li>
    <li>switches simples, programados por protocolo aberto</li>
    <li>a rede vira software: versionada, testada, automatizada</li></ul></div>
</div>""", "Base do relatório 'Da caixa preta à rede programável'. Plano de controle = decidir; plano de dados = encaminhar. (1 min 20)")

S(90, "SDN em produção: a jornada do Google", """<table class="t md">
  <tr><th></th><th>B4 (WAN, 2013)</th><th>Orion (controle, 2021)</th><th>Jupiter Evolving (DC, 2022)</th></tr>
  <tr><td><b>Problema</b></td><td>tráfego entre datacenters, enlaces mal usados com BGP/OSPF</td><td>controlador anterior (Onix) não escalava</td><td>Clos fixo caro de expandir</td></tr>
  <tr><td><b>Ideia</b></td><td>engenharia de tráfego <b>centralizada</b>, switches de silício comercial + OpenFlow</td><td>controle <b>distribuído em microsserviços</b>, orientado a intenção</td><td>comutação óptica (OCS) reconfigurada pelo Orion</td></tr>
  <tr><td><b>Resultado</b></td><td>enlaces perto de <b>100 %</b> de utilização</td><td>mesmo plano de controle para WAN e DC; lançamentos a cada 2 semanas</td><td>topologia muda com o tráfego, sem parar a rede</td></tr>
</table>
<p class="lead" style="margin-top:14px">Lição: SDN não é laboratório — é como os maiores provedores operam.</p>""",
  "B4: Jain et al. (SIGCOMM 2013); Orion: Ferguson et al. (NSDI 2021); Jupiter Evolving: Poutievski et al. (SIGCOMM 2022). B4 coexistiu com BGP/IS-IS via proxy de roteamento (RAP) — adoção gradual. (1 min 30)")

S(100, "SDN como tecnologia habilitadora do 5G", """<div class="cols c2-wide">
  """ + img("odg/5g_sdn.png", 450, "Núcleo 5G centrado em software, com controle SDN e fatias de rede") + """
  <div class="stack" style="gap:10px">
    <div class="card"><h3>5G NSA</h3><p class="small">rádio 5G sobre núcleo 4G (EPC); o eNB 4G ancora o controle — transição.</p></div>
    <div class="card"><h3>5G SA</h3><p class="small"><b>SBA</b>: funções de rede como microsserviços (AMF, SMF, PCF…).<br><b>CUPS</b>: o <b>SMF</b> (controle) programa a <b>UPF</b> (dados) via <b>PFCP/N4</b> — o mesmo papel controlador → switch.</p></div>
    <div class="card"><h3>Consequência</h3><p class="small">UPF na borda (MEC), fatiamento de rede, QoS por fluxo (5QI).</p></div>
  </div></div>""",
  "O 5G não exige OpenFlow, mas aplica o princípio do SDN: separar controle e dados e programar o plano de dados. NSA reaproveita o núcleo 4G; SA é nativo em nuvem. (1 min 40)")

S(80, "Como um provedor orquestra a rede", """<div class="layer"><b>Intenção</b><span>“circuito de 10 Mbps, &lt; 30 ms entre A e B” — API REST/JSON</span></div>
<div class="layer"><b>Orquestração</b><span>traduz a intenção num modelo (YANG/TOSCA), calcula caminho e recursos — ex.: ONAP</span></div>
<div class="layer"><b>Controle</b><span>controladores por domínio (ex.: ONOS) — sabem <i>como</i> fazer dentro do domínio</span></div>
<div class="layer"><b>Mediação</b><span>adaptadores para OpenFlow, NETCONF, PCEP, SNMP de cada fabricante</span></div>
<div class="layer"><b>Dados</b><span>switches, roteadores, VNFs — só executam as regras</span></div>""",
  "O orquestrador sabe 'o quê e para quem'; o controlador sabe 'como'. ONAP nasceu da fusão do ECOMP (AT&T) com o OPEN-O (China Mobile). O FLOWPRI e o QCTP vivem na camada de controle. (1 min 20)")

# ===================================================================================== 2. QoS
divider(1, notes="Agora o problema central: fluxos competindo.")

S(80, "Recursos são finitos: fluxos disputam o enlace", vid("FilaCongestionamento.mp4"),
  "Animação: dois fluxos, um enlace de 10 Mbps. Quando a soma passa da capacidade, a fila do switch cresce (atraso, jitter) e enche (perda). Toda métrica de QoS nasce aqui. (1 min 20)")

S(90, "Quem age quando há congestionamento?", """<div class="cols c2-wide">
  """ + vid("CongestionControlTCP.mp4") + """
  <div class="stack">
    <div class="card"><h3>O administrador</h3><p class="small">superdimensiona, cria filas, prioriza, reserva banda — decide <b>antes</b>.</p></div>
    <div class="card"><h3>O protocolo de transporte</h3><p class="small">o TCP reduz a janela <b>depois</b> de perder pacotes (AIMD, slow start) — reage.</p></div>
    <p class="q" style="font-size:21px">Os dois não conversam: o TCP não sabe que existe reserva.</p>
  </div></div>""",
  "Vídeo do controle de congestionamento do TCP (dente de serra). Essa 'cegueira' é a motivação do QCTP no fim da aula. (1 min 30)")

S(80, "Prioridade × requisitos: duas perguntas diferentes", """<div class="cols c2">
  <div class="card"><h3>Prioridade — quem é mais importante?</h3>
    <div class="icons"><img src="media/odg/ic_hosp.png"><span class="vs">&gt;</span><img src="media/odg/ic_mail.png"></div>
    <p class="small">E-mail do hospital com um exame urgente vale mais que um e-mail promocional — mesmo tipo de tráfego, <b>importância</b> diferente.</p></div>
  <div class="card"><h3>Requisitos — do que o fluxo precisa?</h3>
    <div class="icons"><img src="media/odg/ic_video.png"><span class="vs">≠</span><img src="media/odg/ic_mail.png"></div>
    <p class="small">Vídeo precisa de banda constante e atraso baixo; e-mail tolera segundos de atraso — <b>natureza</b> diferente.</p></div>
</div>
<p class="lead" style="margin-top:16px">QoS precisa das duas: <b>classe</b> (requisito) e <b>prioridade</b> dentro da classe.</p>""",
  "Exemplo do rascunho (hospital × e-mail; vídeo × e-mail), agora separando os dois eixos. O FLOWPRI usa exatamente isso: classe de serviço + 3 prioridades por classe. (1 min 20)")

S(90, "O que é um fluxo?", """<div class="cols c2">
  <div class="stack">
    <div class="card"><h3>Definição</h3><p class="small">Sequência de pacotes com a mesma <b>5-tupla</b>: IP origem, IP destino, porta origem, porta destino e protocolo.</p></div>
    <div class="card"><h3>Formas</h3><ul class="small">
      <li><b>subfluxo</b>: janela de N pacotes (ou T segundos) usada para classificar</li>
      <li><b>elefante</b> (longo, muitos bytes) × <b>rato</b> (curto)</li>
      <li><b>contínuo</b> (vídeo ao vivo) × <b>on/off</b> (navegação, rajadas)</li>
      <li>uni ou <b>bidirecional</b> (ida + ACKs)</li></ul></div>
  </div>
  <div class="stack">
    <img class="fig" src="media/odg/wireshark.png" style="max-height:200px">
    <img class="fig" src="media/odg/tupla.png" style="max-height:60px">
    <div class="cap">Captura no Wireshark: os pacotes de um mesmo fluxo compartilham a 5-tupla</div>
  </div></div>""",
  "Mostrar que o switch enxerga pacotes, não aplicações: precisa agrupar em fluxos para tratá-los. (1 min 30)")

S(90, "Métricas de QoS", """<table class="t md">
  <tr><th>Métrica</th><th>Definição</th><th>Quem sofre</th></tr>
  <tr><td><b>Atraso</b> (one-way)</td><td>tempo do envio de um pacote até sua chegada ao destino</td><td>voz, jogos, cirurgia remota</td></tr>
  <tr><td><b>Jitter</b></td><td>variação do atraso entre pacotes consecutivos</td><td>voz e vídeo ao vivo</td></tr>
  <tr><td><b>Vazão</b></td><td>taxa efetivamente entregue ao destino</td><td>streaming, downloads</td></tr>
  <tr><td><b>Largura de banda</b></td><td>capacidade necessária (ou reservada) para o fluxo</td><td>todos — é o recurso disputado</td></tr>
  <tr><td><b>Perda</b></td><td>fração de pacotes que não chega (descarte, erro)</td><td>tempo real (sem retransmissão)</td></tr>
  <tr><td><b>Tempo de resposta</b></td><td>tempo que o usuário espera numa interação</td><td>web, aplicações interativas</td></tr>
</table>""",
  "QoS = conjunto de mecanismos para melhorar desempenho e confiabilidade da transmissão. Diferenciar taxa gerada (aplicação), banda (enlace/reserva) e vazão (o que chega). (1 min 30)")

S(100, "Onde cada métrica nasce", """<table class="t sm">
  <tr><th>Causa</th><th>Onde</th><th>Métricas afetadas</th></tr>
  <tr><td>Fila do switch/roteador cresce</td><td>rede (buffer de saída)</td><td>atraso ↑, jitter ↑</td></tr>
  <tr><td>Fila cheia → descarte (tail drop)</td><td>rede</td><td>perda ↑ → TCP reduz a taxa → vazão ↓</td></tr>
  <tr><td>Erro de bit no meio físico (rádio, cabo)</td><td>enlace</td><td>perda ↑, retransmissões → atraso ↑</td></tr>
  <tr><td>Caminhos diferentes / balanceamento</td><td>rede</td><td>reordenação → TCP interpreta como perda; jitter ↑</td></tr>
  <tr><td>Buffer do emissor / janela pequena</td><td>host emissor</td><td>vazão ↓ mesmo com rede livre</td></tr>
  <tr><td>Aplicação receptora lenta (buffer cheio)</td><td>host receptor</td><td>controle de fluxo freia o emissor → vazão ↓</td></tr>
  <tr><td>Distância (propagação) e serialização</td><td>física</td><td>atraso mínimo fixo — nenhum QoS reduz</td></tr>
</table>
<p class="q" style="font-size:21px">Gerenciar recursos atua nas linhas da rede; o transporte atua nas linhas do host.</p>""",
  "Atende à nota do rascunho ('a relação entre as causas e as métricas'). Perguntar à turma: quais destas o administrador consegue resolver com filas? (as duas primeiras). (1 min 40)")

S(80, "Requisitos por aplicação: quem define?", """<div class="cols c2-wide">
  """ + img("odg/req_3gpp.png", 420, "Requisitos de atraso, jitter e perda por classe de aplicação (3GPP/ITU)") + """
  <div class="stack">
    <div class="card"><h3>Padrões</h3><ul class="small">
      <li><b>ITU-T G.1010</b>: categorias de QoS para multimídia</li>
      <li><b>ITU-T Y.1541</b>: objetivos de desempenho para IP</li>
      <li><b>3GPP TS 23.501</b>: <b>5QI</b> — perfil de QoS por fluxo no 5G</li></ul></div>
    <div class="card"><p class="small">Os valores evoluem: aplicações novas (XR, cirurgia remota) pedem atrasos cada vez menores.</p></div>
  </div></div>""",
  "As métricas não são inventadas por cada operador: vêm de 3GPP/ITU. Exemplo: voz interativa ~150 ms fim a fim é um limite clássico. (1 min 20)")

S(70, "QoS × QoE", """<div class="cols c2">
  """ + img("odg/qoe_bom.png", 340, "Vídeo com QoS adequado", force=True) + """
  """ + img("odg/qoe_ruim.png", 340, "Mesmo vídeo com perda de pacotes", force=True) + """
</div>
<p class="lead" style="margin-top:8px"><b>QoS</b> se mede na rede (ms, %, Mbps). <b>QoE</b> é a percepção do usuário (ex.: nota MOS de 1 a 5, ITU-T P.800). Bom QoS é condição para boa QoE — o usuário não vê “2 % de perda”, vê o vídeo quebrado.</p>""",
  "Mostrar as duas imagens e perguntar o que aconteceu na rede. Perda em vídeo sem retransmissão vira artefato visual. (1 min 10)")

S(120, "Exercício rápido: prioridade e requisitos", """<div class="card ex"><h3>Para cada fluxo: qual classe? qual prioridade? qual métrica mais importa?</h3>
<table class="t md" style="margin-top:6px">
  <tr><th>Fluxo</th><th>Classe</th><th>Prioridade</th><th>Métrica crítica</th></tr>
  <tr><td>Cirurgia remota (vídeo + comandos)</td><td></td><td></td><td></td></tr>
  <tr><td>Chamada VoIP</td><td></td><td></td><td></td></tr>
  <tr><td>Netflix</td><td></td><td></td><td></td></tr>
  <tr><td>Backup noturno de 2 TB</td><td></td><td></td><td></td></tr>
  <tr><td>E-mail com laudo de exame urgente</td><td></td><td></td><td></td></tr>
</table></div>""",
  "2 minutos em duplas. Respostas esperadas: cirurgia = tempo real, prioridade máxima, atraso/perda; VoIP = tempo real, atraso/jitter; Netflix = não-tempo-real (buffer), banda; backup = best-effort, vazão; e-mail urgente = best-effort/NRT com prioridade alta — requisito baixo, importância alta. (2 min)")

# ===================================================================================== 3. SDN
divider(2, notes="Agora a ferramenta: como o SDN permite agir nesses fluxos.")

S(80, "Arquitetura SDN", """<div class="cols c2-wide">
  """ + img("odg/sdn_arq.png", 470, "Camadas de aplicação, controle e dados", force=True) + """
  <div class="stack">
    <div class="card"><h3>Propriedades</h3><ul>
      <li><b>desacoplamento</b> controle × dados</li>
      <li><b>hardware</b> comum (silício comercial)</li>
      <li><b>dinamismo</b>: regras mudam em ms</li>
      <li><b>programabilidade</b>: rede via API</li></ul></div>
  </div></div>""",
  "Três camadas, duas interfaces: northbound (apps ↔ controlador) e southbound (controlador ↔ switches). (1 min 20)")

S(70, "Controlador SDN", """<div class="cols c2">
  <div class="card"><h3>O “sistema operacional” da rede</h3><ul>
    <li>visão global da topologia e do estado</li>
    <li>executa aplicações: roteamento, balanceamento, monitoramento, QoS</li>
    <li>programa as tabelas de encaminhamento dos switches</li>
    <li>exemplos: <b>POX, Ryu, Floodlight, ONOS, OpenDaylight</b></li></ul>
    <p class="small" style="margin-top:8px">P4 não é controlador: é a linguagem do plano de dados (o controlador fala P4Runtime).</p></div>
  """ + img("odg/controlador.png", 440, "Controlador entre aplicações e infraestrutura") + """
</div>""", "Corrigido do rascunho: P4 saiu da lista de controladores. FLOWPRI usa Ryu; QCTP usa um controlador Python com P4Runtime. Controlador pode ser replicado (ONOS, Orion) para não ser ponto único de falha. (1 min 10)")

S(70, "Interface Northbound", """<div class="cols c2">
  <div class="stack">
    <ul class="lead">
      <li>Onde <b>aplicações</b> conversam com o controlador (em geral REST/JSON).</li>
      <li>Trocar dados (topologia, estatísticas) e pedir regras.</li>
      <li>Apps locais, em nuvem ou em microsserviços; isoladas ou compartilhadas.</li>
    </ul>
    <img class="fig" src="media/odg/northbound_code.png" style="max-height:200px">
    <div class="cap">Endpoint REST que instala uma regra (Ryu)</div>
  </div>
  """ + img("odg/northbound_app.png", 430, "Aplicação de monitoramento cria/remove regras via REST") + """
</div>""", "Exemplo: o FLOWPRI recebe configurações JSON (switches, rotas, hosts) numa porta reservada. (1 min 10)")

S(70, "Interface Southbound", """<div class="cols c2">
  <div class="card"><h3>Controlador ↔ switch</h3><ul>
    <li>mensagens e <b>eventos</b> (pacote novo, porta caiu, regra expirou)</li>
    <li>tipos de ação: encaminhar, descartar, remarcar, enfileirar, limitar</li>
    <li><b>OpenFlow</b>: estado de fluxos (tabelas fixas)</li>
    <li><b>P4Runtime</b>: tabelas definidas pelo programa P4</li>
    <li><b>OVSDB / NETCONF</b>: configuração (portas, filas)</li></ul></div>
  """ + img("odg/p4runtime.png", 430, "P4Runtime: controlador gRPC ↔ switch") + """
</div>""", "OpenFlow muda o comportamento de encaminhamento; OVSDB/NETCONF configuram o equipamento (ex.: criar filas HTB, que o OpenFlow não cria). (1 min 10)")

S(80, "Protocolo OpenFlow: mensagens", """<table class="t md">
  <tr><th>Tipo</th><th>Mensagens</th><th>Para quê</th></tr>
  <tr><td><b>Simétricas</b></td><td>Hello, Echo Request/Reply</td><td>abrir e manter a sessão</td></tr>
  <tr><td><b>Controlador → switch</b></td><td>Features, Set-Config, <b>Flow-Mod</b>, <b>Meter-Mod</b>, Group-Mod, Packet-Out, Multipart (estatísticas)</td><td>programar e consultar o switch</td></tr>
  <tr><td><b>Assíncronas</b> (switch → controlador)</td><td><b>Packet-In</b>, Flow-Removed, Port-Status, Error</td><td>avisar eventos</td></tr>
</table>
<p class="lead" style="margin-top:14px">Configuração do equipamento fica fora do OpenFlow: <b>OVSDB</b> (Open vSwitch) ou <b>NETCONF</b>.</p>""",
  "Destacar Packet-In (switch pergunta) e Flow-Mod (controlador responde) — o par que aparece na animação seguinte. Flow-Removed é o que o FLOWPRI usa para liberar banda quando a regra expira. (1 min 20)")

S(80, "Tabelas de fluxo", """<div class="cols c2">
  <div class="stack">
    """ + img("odg/flow_table.png", 170, "Tabela de fluxo: campos de match, ação e contadores") + """
    <div class="card"><h3>Uma regra tem</h3><ul class="small">
      <li><b>match</b> (campos do cabeçalho) e <b>prioridade</b></li>
      <li><b>instruções</b>: ações, meter, goto-table</li>
      <li><b>contadores</b> (pacotes, bytes)</li>
      <li><b>timeouts</b>: idle e hard</li></ul></div>
  </div>
  """ + img("odg/match_fields.png", 440, "Campos de match do OpenFlow (L2 a L4)") + """
</div>""", "Match em L2–L4: MAC, VLAN, IP, ToS, portas. Os timeouts são usados pelo FLOWPRI (idle 2 s, hard 5 s). (1 min 20)")

S(80, "O pipeline OpenFlow em ação", vid("PipelineOpenFlow.mp4"),
  "Pacote conhecido: tabela 0 → meter → tabela 1 → fila e porta. Pacote novo: table-miss → Packet-In → controlador decide → Flow-Mod. (1 min 20)")

S(80, "Tabela de meters", """<div class="cols c2">
  <div class="stack">
    <img class="fig" src="media/odg/meter_entry.png" style="max-height:40px">
    <img class="fig" src="media/odg/meter_band.png" style="max-height:40px">
    <div class="card"><h3>Meter (OpenFlow 1.3+)</h3><ul>
      <li><b>identificador</b> único, referenciado pela regra</li>
      <li><b>contadores</b> de pacotes/bytes</li>
      <li><b>banda</b>: <i>rate</i> (kbps) + tipo: <b>drop</b> ou <b>remarcar DSCP</b></li>
      <li>acima da taxa → descarta: <b>policing</b></li></ul></div>
  </div>
  """ + img("odg/token_bucket.png", 420, "Token bucket: créditos repostos à taxa média; rajada limitada") + """
</div>""", "Meter = limitador de taxa por fluxo. Não guarda pacotes (isso é fila); descarta o excesso. É o que impede um fluxo reservado de passar da reserva. (1 min 20)")

S(100, "P4: programando o plano de dados", """<div class="cols" style="grid-template-columns:1fr 1.25fr">
  <div class="stack">
    <div class="card"><h3>OpenFlow × P4</h3><ul class="small">
      <li>OpenFlow: campos e ações <b>fixos</b> no protocolo</li>
      <li>P4: o programador define <b>parser</b>, <b>tabelas</b> e <b>deparser</b> — independente de protocolo</li>
      <li>compilado para o alvo (BMv2, Tofino); <code>p4info</code> descreve as tabelas para o P4Runtime</li>
      <li>permite cabeçalhos novos (QCTP) e telemetria in-band (INT)</li></ul></div>
    <p class="small" style="text-align:center">parser → match-action (ingress) → match-action (egress) → deparser</p>
  </div>
  <div class="code"><span class="c">// qctp_switch/qctp.p4 (trecho)</span>
<span class="k">meter</span>(MAX_FLOWS, MeterType.bytes) flow_meter;

<span class="k">table</span> qctp_flow {
    key = {
        hdr.ipv4.srcAddr: exact;
        hdr.ipv4.dstAddr: exact;
        hdr.qctp.flow_id: exact;
    }
    actions = { qos_forward; NoAction; }
}
<span class="c">// qos_forward marca DSCP, escolhe a fila
// e, na borda, policia granted_kbps</span></div>
</div>""", "Trecho real do switch do QCTP. A mesma ideia do OpenFlow (tabela + meter), mas a chave inclui um campo de um cabeçalho que não existe no OpenFlow (flow_id do QCTP). (1 min 40)")

# ===================================================================================== 4. GERENCIAMENTO
divider(3, notes="SDN não substitui o gerenciamento clássico: complementa.")

S(80, "Os pilares do gerenciamento: FCAPS", """<table class="t md">
  <tr><th>Área</th><th>Objetivo</th><th>Exemplo</th></tr>
  <tr><td><b>F</b>alhas</td><td>detectar, isolar, registrar e corrigir anomalias</td><td>alarme de enlace caído, análise de logs</td></tr>
  <tr><td><b>C</b>onfiguração</td><td>inventário, backup e versão de configurações, provisionamento</td><td>trocar a VLAN de 50 switches</td></tr>
  <tr><td><b>C</b>ontabilização (<i>Accounting</i>)</td><td>medir o uso por usuário/serviço para cobrança e cotas</td><td>volume trafegado por cliente</td></tr>
  <tr><td><b>D</b>esempenho (<i>Performance</i>)</td><td>monitorar vazão, atraso, perda e utilização</td><td>enlace a 90 % no horário de pico</td></tr>
  <tr><td><b>S</b>egurança</td><td>controle de acesso, autenticação, auditoria</td><td>quem alterou a regra do firewall?</td></tr>
</table>
<p class="small" style="margin-top:10px">Modelo ISO/IEC 7498-4 (e ITU-T M.3400). QoS toca principalmente <b>Desempenho</b>, <b>Contabilização</b> e <b>Configuração</b>.</p>""",
  "O rascunho tinha parágrafos longos; aqui uma linha por área. (1 min 20)")

S(80, "SNMP", """<div class="cols c2">
  <div class="card"><h3>Simple Network Management Protocol</h3><ul class="small">
    <li><b>gerente</b> (NMS) consulta <b>agentes</b> nos equipamentos</li>
    <li><b>MIB</b>: base hierárquica de objetos (OIDs), descrita pela <b>SMI</b></li>
    <li>operações: Get, Set, <b>Trap</b> (alerta do agente)</li>
    <li><b>RMON</b>: estatísticas de tráfego coletadas no próprio equipamento</li>
    <li>v3 adiciona autenticação e criptografia</li></ul></div>
  <div class="stack">
    <div class="code"><span class="c"># contador de bytes da interface 2</span>
snmpget -v2c -c public 10.0.0.1 \\
    IF-MIB::ifInOctets.2
IF-MIB::ifInOctets.2 = Counter32: 918273</div>
    <div class="card"><h3>Na prática</h3><p class="small">Zabbix, Prometheus (exporter SNMP), PRTG, Nagios, SolarWinds — cumprem o FCAPS com SNMP, RMON e NetFlow/IPFIX.</p></div>
  </div></div>""",
  "SNMP consulta e altera o estado interno de um dispositivo. Ótimo para contadores; ruim para configuração em massa (Set é pouco usado). (1 min 20)")

S(90, "Configurar × programar × descobrir", """<table class="t md">
  <tr><th></th><th>OpenFlow</th><th>NETCONF / YANG</th><th>BGP-LS</th></tr>
  <tr><td><b>Propósito</b></td><td>programar tabelas de encaminhamento</td><td>configurar e gerenciar dispositivos</td><td>levar a topologia (OSPF/IS-IS) ao controlador</td></tr>
  <tr><td><b>Estado</b></td><td>volátil (memória do switch)</td><td>persistente (configuração salva)</td><td>estado da rede, dinâmico</td></tr>
  <tr><td><b>Abstrai</b></td><td>a tabela de fluxo</td><td>a CLI e a base de configuração</td><td>a base link-state dos IGPs</td></tr>
  <tr><td><b>Ideal para</b></td><td>funções novas, temporárias, por fluxo</td><td>funções existentes, manutenção</td><td>redes grandes, multi-domínio</td></tr>
</table>
<p class="small" style="margin-top:10px">NETCONF (RFC 6241) troca dados XML modelados em YANG (RFC 7950): “o app de configurações do celular” da rede.</p>""",
  "Tabela do relatório 'Da caixa preta à rede programável'. Provedores usam os três juntos: NETCONF configura, OpenFlow/P4 programa, BGP-LS informa a topologia. (1 min 30)")

S(70, "NetFlow / IPFIX: observar o tráfego", """<div class="cols c2">
  <div class="stack">
    <ul class="lead">
      <li>O equipamento (<b>exportador</b>) agrega pacotes em <b>registros de fluxo</b> e os envia a um <b>coletor</b>.</li>
      <li>Quem fala com quem, quanto, por qual porta e protocolo.</li>
      <li><b>Só observa</b> — não altera nada (“extrato da conta telefônica”).</li>
      <li>IPFIX (RFC 7011) é o padrão IETF; sFlow faz amostragem.</li>
    </ul>
  </div>
  <table class="t sm">
    <tr><th></th><th>NetFlow / IPFIX</th><th>NETCONF</th></tr>
    <tr><td>Função</td><td>monitorar tráfego</td><td>configurar dispositivos</td></tr>
    <tr><td>Direção</td><td>dispositivo → coletor</td><td>gerente → dispositivo</td></tr>
    <tr><td>Formato</td><td>registros binários de fluxo</td><td>XML / YANG</td></tr>
    <tr><td>Altera o equipamento?</td><td class="no">não</td><td class="ok">sim</td></tr>
  </table>
</div>""", "NetFlow observa; NETCONF configura. Contabilização e classificação de tráfego começam nos registros de fluxo. (1 min 10)")

S(100, "Equivalência funcional no Open vSwitch", """<table class="t sm">
  <tr><th>Necessidade (gerência clássica)</th><th>SNMP / NETCONF / NetFlow</th><th>Open vSwitch / OpenFlow</th></tr>
  <tr><td>contadores de interface</td><td><code>IF-MIB::ifInOctets</code></td><td><code>ovs-ofctl dump-ports br0</code></td></tr>
  <tr><td>estado das portas</td><td><code>ifOperStatus</code></td><td><code>ovs-ofctl dump-ports-desc br0</code></td></tr>
  <tr><td>tabela MAC</td><td>BRIDGE-MIB (<code>dot1dTpFdb</code>)</td><td><code>ovs-appctl fdb/show br0</code></td></tr>
  <tr><td>contadores por fluxo</td><td>NetFlow / IPFIX</td><td><code>ovs-ofctl dump-flows br0</code></td></tr>
  <tr><td>taxa por fluxo (policiamento)</td><td>—</td><td><code>ovs-ofctl -O OpenFlow13 meter-stats br0</code></td></tr>
  <tr><td>configuração (portas, filas)</td><td>NETCONF / CLI</td><td><code>ovs-vsctl</code> (OVSDB)</td></tr>
  <tr><td>exportar fluxos</td><td>NetFlow / sFlow</td><td><code>ovs-vsctl -- set Bridge br0 netflow=@nf …</code></td></tr>
</table>
<p class="small" style="margin-top:8px">Não há equivalência 1:1 de mensagens, mas há equivalência <b>funcional</b>: SDN e SNMP são complementares.</p>""",
  "Baseado na tabela do rascunho (OVS ↔ SNMP). O OVS também exporta NetFlow/sFlow/IPFIX nativamente — dá para usar o NMS de sempre numa rede SDN. (1 min 40)")

# ===================================================================================== 5. QoS em SDN
divider(4, notes="Juntando: como implementar QoS com SDN, aproveitando o que as redes convencionais já têm.")

S(70, "Modelos de QoS das redes convencionais", """<table class="t md">
  <tr><th>Modelo</th><th>Ideia</th><th>Limitação</th></tr>
  <tr><td><b>Best-effort</b></td><td>todos iguais; a fila é FIFO</td><td>nenhuma garantia</td></tr>
  <tr><td><b>IntServ</b> (RFC 1633) + RSVP</td><td>reserva <b>por fluxo</b> em cada roteador do caminho</td><td>estado por fluxo em todo roteador → não escala</td></tr>
  <tr><td><b>DiffServ</b> (RFC 2475)</td><td>marca o pacote (DSCP) na borda; o núcleo trata por <b>classe</b></td><td>sem garantia por fluxo; marcação não atravessa domínios com confiança</td></tr>
</table>
<p class="lead" style="margin-top:14px">Ferramentas comuns aos três: <b>filas</b>, <b>túneis</b> e <b>limitadores (meters)</b>.</p>""",
  "SDN não inventa QoS novo: reaproveita filas, marcação e túneis, mas com um controlador que vê tudo. (1 min 10)")

S(70, "IntServ e RSVP", """<div class="stack" style="gap:6px">
  <img class="fig" src="media/odg/rsvp_path.png" style="max-height:110px;margin:0 auto">
  <img class="fig" src="media/odg/rsvp_resv.png" style="max-height:110px;margin:0 auto">
  <img class="fig" src="media/odg/rsvp_data.png" style="max-height:110px;margin:0 auto">
  <p class="lead">1. <b>PATH</b> da origem descobre o caminho · 2. <b>RESV</b> do destino reserva em cada salto · 3. os dados seguem pela reserva.</p>
</div>""", "Mesmo padrão de sinalização que o FLOWPRI (FRED) e o QCTP (SYN com FRED) usam — mas lá quem reserva é o controlador, não cada roteador. (1 min 10)")

S(80, "DiffServ e DSCP", """<div class="cols c2-wide">
  """ + img("odg/diffserv.png", 360, "Domínio DiffServ: a borda classifica e marca; o núcleo aplica o PHB") + """
  <div class="card"><h3>Como funciona</h3><ul class="small">
    <li>campo <b>DSCP</b>: 6 bits do antigo ToS (IPv4) / Traffic Class (IPv6)</li>
    <li>cada código define um <b>PHB</b> (comportamento por salto)</li>
    <li><b>EF</b> (46): baixa latência — voz</li>
    <li><b>AF</b>xy: 4 classes × 3 precedências de descarte</li>
    <li><b>CS</b>0–7: compatível com IP Precedence; CS0 = best-effort</li>
    <li>agrega fluxos com o mesmo requisito</li></ul></div>
</div>""", "O FLOWPRI define códigos DSCP para as suas classes de tempo real e não-tempo-real (tabelas 2 e 3 da dissertação). O QCTP marca DSCP no P4. (1 min 20)")

S(80, "Remarcação e encapsulamento", """<div class="g22">
  <div><img src="media/odg/ipv4.png"><div class="cap">IPv4: ToS/DSCP remarcável pelo switch</div></div>
  <div><img src="media/odg/vlan.png"><div class="cap">VLAN 802.1Q: prioridade PCP (3 bits) + VID</div></div>
  <div><img src="media/odg/vxlan.png"><div class="cap">VXLAN: quadro L2 dentro de UDP (overlay)</div></div>
  <div><img src="media/odg/mpls.png"><div class="cap">MPLS: rótulo de 20 bits + 3 bits de classe</div></div>
</div>""", "Em SDN, uma ação de regra muda esses campos (set_field). Remarcar = dizer aos próximos saltos como tratar; encapsular = isolar ou levar por um túnel. (1 min 20)")

S(80, "Limitar a taxa: meter × fila", """<div class="cols c2">
  <div class="card"><h3>Meter — <i>policing</i></h3><ul>
    <li>mede a taxa do fluxo e <b>descarta</b> (ou remarca) o excesso</li>
    <li>não tem buffer: não adiciona atraso</li>
    <li>por fluxo, na <b>borda</b></li>
    <li>OpenFlow: Meter-Mod; P4: <code>meter</code></li></ul></div>
  <div class="card"><h3>Fila — <i>shaping</i></h3><ul>
    <li><b>guarda</b> o excesso e o envia depois</li>
    <li>suaviza rajadas, mas adiciona atraso</li>
    <li>por classe, em cada <b>porta</b></li>
    <li>Linux/OVS: <code>tc</code> HTB via <code>ovs-vsctl</code></li></ul></div>
</div>
<p class="lead" style="margin-top:14px">Combinados: o meter impede o fluxo de passar da reserva; a fila garante a banda da classe.</p>""",
  "Distinção que costuma confundir: policing descarta, shaping atrasa. FLOWPRI e QCTP usam os dois. (1 min 20)")

S(80, "Filas HTB: garantia e empréstimo", """<div class="cols c2-wide">
  """ + vid("HTBEmprestimo.mp4") + """
  """ + img("odg/htb.png", 420, "Hierarquia HTB: raiz → classes internas → folhas, cada uma com rate (mínimo) e ceil (máximo)") + """
</div>""", "HTB (Hierarchical Token Bucket, Devera): cada classe tem rate garantido e ceil; banda ociosa é emprestada e devolvida quando o dono volta. Percentuais do FLOWPRI: CTRL 7, RT 33, NRT 35, BE 25. (1 min 20)")

S(60, "Balanceamento e telemetria", """<div class="cols c2">
  <div class="card"><h3>Balanceamento de carga</h3><ul>
    <li>redirecionar fluxos por caminhos diferentes</li>
    <li>OpenFlow <b>group table</b> (tipo <i>select</i>)</li>
    <li>engenharia de tráfego centralizada (B4)</li></ul></div>
  <div class="card"><h3>Telemetria</h3><ul>
    <li>contadores de <b>portas</b>, <b>filas</b> e <b>regras</b> (Multipart)</li>
    <li>regras de monitoramento dedicadas</li>
    <li><b>INT</b> (P4): cada switch escreve seu estado no próprio pacote</li></ul></div>
</div>""", "Sem medir não há como saber se o QoS foi entregue. O INT é usado pelo QCTP; o FLOWPRI usa regras de monitoramento na borda. (1 min)")

S(80, "Classificação de tráfego: como saber o que é cada fluxo?", """<table class="t sm">
  <tr><th>Abordagem</th><th>Como</th><th>Problema</th></tr>
  <tr><td><b>Portas</b> (IANA)</td><td>porta 443 = HTTPS, 5060 = SIP…</td><td>portas dinâmicas e tudo sobre 443 → baixa precisão</td></tr>
  <tr><td><b>Inspeção de payload</b> (DPI)</td><td>busca padrões nos bytes de dados</td><td>caro; não funciona com tráfego criptografado</td></tr>
  <tr><td><b>Auto-identificação</b></td><td>a aplicação declara o que é</td><td>exige confiança e suporte do host (é o caminho do QCTP)</td></tr>
  <tr><td><b>Estatísticas do fluxo + ML</b></td><td>tamanhos, intervalos, flags dos primeiros N pacotes</td><td>precisa de dados rotulados e treino</td></tr>
</table>
<div class="cols c2" style="height:auto;margin-top:10px">
  <img class="fig" src="media/odg/dpi_hex.png" style="max-height:150px">
  <img class="fig" src="media/odg/flows_stats.png" style="max-height:150px">
</div>""", "Com TLS em quase tudo, DPI enxerga só bytes aleatórios (imagem da esquerda). As estatísticas do fluxo (direita) continuam visíveis. (1 min 20)")

S(70, "Árvores de decisão e Random Forest", """<div class="cols c2">
  <div class="card"><h3>Ideia</h3><ul class="small">
    <li><b>árvore</b>: cada nó é uma pergunta sobre uma feature (“tamanho médio &gt; 900 B?”)</li>
    <li>cada pergunta deve reduzir a <b>entropia</b> (desordem) do conjunto — ID3</li>
    <li>folha = classe prevista</li>
    <li><b>Random Forest</b>: muitas árvores treinadas em amostras aleatórias; a <b>votação</b> decide</li>
    <li>rápida para classificar → cabe no controlador</li></ul></div>
  """ + img("odg/random_forest.png", 430, "Random Forest: três árvores votam na classe final") + """
</div>""", "Breiman (2001). Vantagem para redes: inferência barata e interpretável. (1 min 10)")

S(100, "Exercício: qual mecanismo usar?", """<div class="card ex"><h3>Associe cada situação a um mecanismo (meter, fila HTB, DSCP, VLAN/VXLAN, group table, ML)</h3><ol class="small" style="margin-top:6px">
  <li>Um cliente contratou 20 Mbps e não pode passar disso.</li>
  <li>A voz deve ter prioridade em todos os roteadores do backbone.</li>
  <li>O backup deve usar a banda que sobrar, sem atrapalhar ninguém.</li>
  <li>Dois clientes usam o mesmo prefixo IP privado no datacenter.</li>
  <li>Dois enlaces paralelos: um a 95 %, outro a 10 %.</li>
  <li>O tráfego é todo HTTPS na porta 443 e precisamos saber o que é vídeo.</li></ol></div>""",
  "Respostas: 1 meter; 2 DSCP (EF); 3 fila BE do HTB (empréstimo/ceil); 4 VXLAN/VLAN; 5 group table select / engenharia de tráfego; 6 classificação por ML. (1 min 40)")

# ===================================================================================== 6. FLOWPRI
divider(5, notes="Um framework que junta tudo isso: classificação, reserva, multi-domínio e auditoria.")

S(80, "FLOWPRI-SDN", """<div class="cols c2">
  <div class="stack">
    <div class="card"><h3>Framework de gerenciamento de recursos</h3><ul>
      <li><b>multi-domínio</b>: cada AS tem seu controlador</li>
      <li><b>classifica</b> o tráfego (ML) → requisitos</li>
      <li><b>reserva</b> banda por fluxo, com <b>prioridade</b></li>
      <li><b>QoS como serviço</b>, auditável (QoSBlockchain)</li></ul></div>
    <p class="small">Versão 1.0: Mocelin Jr. e Fiorese (2023). Versão 2.0: dissertação de mestrado (UDESC, 2025), sobre Ryu + OVS.</p>
  </div>
  """ + img("odg/flowpri_arq.png", 450, "Arquitetura do FLOWPRI-SDN 2.0: módulos no controlador e plano de dados") + """
</div>""", "Módulos: gerência de switches, gerência local de recursos (G-BAM), classificação, comunicação multi-domínio, monitoramento de QoS, QoSBlockchain. (1 min 20)")

S(80, "FRED: o documento de requisitos do fluxo", """<div class="cols" style="grid-template-columns:1fr 1.5fr">
  """ + img("odg/fred.png", 460) + """
  <div class="stack">
    <div class="card"><h3>Flow Requirements Document</h3><ul class="small">
      <li><b>identificação</b>: 5-tupla e versão IP</li>
      <li><b>QoS</b>: classe, prioridade, banda, atraso, jitter, perda, rótulo</li>
      <li><b>blockchain</b>: nome, faixas de IP dos ASs, nó gênese, pares</li>
      <li><b>code</b>: 1 = aceito, −1 = rejeitado</li></ul></div>
    <p class="small">Gerado quando um fluxo novo é classificado e enviado a <b>todos</b> os domínios da rota. O QCTP reaproveita o FRED, mas quem o declara é o próprio host.</p>
  </div></div>""",
  "FRED é a 'intenção' do fluxo. Exemplo da dissertação: classe real-time, 2 Mbps, delay 30 ms, rótulo ae-2Mbps. (1 min 20)")

S(90, "Filas e G-BAM", """<div class="cols c2">
  """ + img("odg/flowpri_filas.png", 380, "Por porta: 3 filas de prioridade em RT (33 %) e NRT (35 %), BE (25 %) e controle (7 %)") + """
  <div class="card"><h3>G-BAM: alocação de banda</h3><ol class="small">
    <li>pega a classe do FRED e verifica a banda livre nas portas de toda a rota</li>
    <li>se faltar, remove fluxos que estão <b>emprestando</b> na classe</li>
    <li>se ainda faltar, <b>empresta</b> da outra classe QoS</li>
    <li>se não der, remove fluxos de <b>menor prioridade</b></li>
    <li>senão, <b>rejeita</b> o FRED (code −1) → best-effort</li></ol>
    <p class="small" style="margin-top:6px">Backbone: agrega por classe (regras conjuntivas) em vez de regra por fluxo.</p></div>
</div>""", "HTB empresta a banda ociosa para o BE sem reserva; o G-BAM controla o empréstimo entre as classes QoS. Backbone não policia por fluxo: a borda já limitou. (1 min 30)")

S(80, "Programação das tabelas e regras meter", """<div class="cols c2">
  <div class="card"><h3>Regra QoS</h3><ul class="small">
    <li>regra de encaminhamento + <b>meter</b> com a banda do FRED</li>
    <li>envia para a fila da classe/prioridade e marca DSCP</li>
    <li><b>idle timeout 2 s</b>, <b>hard timeout 5 s</b> → renovação periódica</li>
    <li>desconta a banda da classe nas portas de entrada e saída</li></ul></div>
  <div class="card"><h3>Regra best-effort</h3><ul class="small">
    <li>sem meter: só envia para a fila BE</li>
    <li>mesmos timeouts → o fluxo pode ser reclassificado</li></ul>
    <h3 style="margin-top:12px">Remoção</h3><ul class="small">
    <li><b>ativa</b> (controlador manda) ou <b>passiva</b> (timeout)</li>
    <li>Flow-Removed → libera a banda na rota e apaga meter e FRED</li></ul></div>
</div>""", "Regras de monitoramento: regras QoS com cookie = 1, só no primeiro switch, para medir o QoS entregue. (1 min 20)")

S(90, "Classificação de tráfego no FLOWPRI", """<div class="cols c2">
  <div class="stack">
    <img class="fig" src="media/odg/classes.jpg" style="max-height:250px">
    <div class="cap">Classes: aplicação, banda e rótulo</div>
  </div>
  <div class="stack">
    <img class="fig" src="media/odg/features.jpg" style="max-height:200px">
    <div class="cap">Features calculadas por amostra de fluxo</div>
    <div class="card kpi" style="padding:8px 16px"><span class="v">98 %</span><span class="l">precisão do Random Forest em subfluxos de 10 pacotes, 8 classes de QoS</span></div>
    <p class="small">Analisar em <b>batch</b> (amostras), não pacote a pacote; separar TCP/UDP ajuda (XGBoost chega a 99 % em TCP).</p>
  </div></div>""",
  "Resultados da dissertação (cap. 5). Rótulo = classe de aplicação + banda (ex.: ae-2Mbps = áudio estático). (1 min 30)")

S(60, "Fluxo da classificação", """<div class="cols c2-wide">
  """ + img("odg/flowpri_classif.png", 450, "Pacote novo → buffer de N pacotes → features → classificador → regra QoS ou BE") + """
  <div class="card"><h3>Passo a passo</h3><ol class="small">
    <li>primeiro pacote: regra BE temporária</li>
    <li>espelha N pacotes ao controlador</li>
    <li>extrai features e classifica</li>
    <li>gera o FRED → G-BAM</li>
    <li>instala regra QoS (com meter) ou mantém BE</li></ol></div>
</div>""", "O fluxo nunca fica parado esperando o classificador: começa em best-effort. (1 min)")

S(100, "Comunicação inter-domínio: ICMPv6 139/140", """<div class="cols c2-wide">
  """ + vid("ICMPInterDominio.mp4") + """
  <div class="stack">
    <div class="card"><h3>Por que ICMP?</h3><ul class="small">
      <li>atravessa a rota com os <b>mesmos IPs</b> do fluxo</li>
      <li>ICMPv6 <b>139</b> (NI Query) leva o FRED; <b>140</b> informa rejeição</li>
      <li>IPv4: tipos 15/16</li>
      <li>cada controlador o recebe por Packet-In</li></ul></div>
    """ + img("odg/icmp_header.png", 130) + """
  </div></div>""",
  "O FRED segue o mesmo caminho dos dados, então cada domínio da rota fica sabendo. Rejeição (140) volta à origem e todos os domínios anteriores liberam a reserva. ICMPv6 NI: RFC 4620. (1 min 40)")

S(90, "QoSBlockchain v1 (Hyperledger Sawtooth)", """<div class="cols c2">
  <div class="stack">
    """ + img("odg/qosbc_arq.png", 200, "Nó Sawtooth: REST API, validador, consenso, transaction processor") + """
    <div class="card"><h3>Quem participa</h3><ul class="small">
      <li>uma blockchain por <b>par de domínios de borda</b></li>
      <li>pares: os 2 controladores FLOWPRI + 1 <b>host de gerência</b> de cada domínio</li>
      <li>50 % clientes, 50 % operadores: ninguém controla sozinho</li></ul></div>
  </div>
  <div class="stack">
    """ + img("odg/qosbc_fluxo.png", 280, "Borda de origem e destino medem e registram o QoS") + """
    <p class="small">Registra o FRED e as medições de QoS ao longo do tempo; o cliente consulta o histórico e prova violações do SLA.</p>
  </div></div>""",
  "Resposta à pergunta do ISP: quem prova que o SLA foi cumprido? No QCTP a ideia continua (camada de auditoria), mas o ledger hoje é um mock com cadeia de hashes. (1 min 30)")

# ===================================================================================== 7. QCTP
divider(6, notes="Ponte: o FLOWPRI reserva banda, mas o transporte do host continua cego.")

S(90, "Do FLOWPRI ao transporte: o que falta", """<div class="stack">
  <p class="lead">O FLOWPRI reserva 5 Mbps para o fluxo… e o TCP envia 3 (desperdiça) ou 7 (o meter descarta).</p>
  <div class="cols c3" style="height:auto">
    <div class="card"><h3>Lacuna 1</h3><p>Transporte e QoS são cegos um ao outro</p></div>
    <div class="card"><h3>Lacuna 2</h3><p>Nenhum transporte negocia QoS no handshake</p></div>
    <div class="card"><h3>Lacuna 3</h3><p>Não há auditoria fim a fim no nível do transporte</p></div>
  </div>
  <table class="t sm">
    <tr><th>Caso de uso</th><th>Precisa de</th><th>Problema hoje</th></tr>
    <tr><td><b>Telemedicina</b> (cirurgia remota)</td><td>10 Mbps, &lt; 20 ms, perda &lt; 1 %</td><td>TCP/QUIC não garantem; congestionamento põe o procedimento em risco</td></tr>
    <tr><td><b>Videoconferência corporativa</b></td><td>2 Mbps por participante, &lt; 150 ms</td><td>trava no pico; não há como provar que o SLA falhou</td></tr>
    <tr><td><b>Cloud gaming</b></td><td>25 Mbps, &lt; 20 ms, jitter &lt; 10 ms</td><td>o dente de serra do TCP vira lag</td></tr>
  </table>
</div>""", "As três lacunas do doutorado. Casos de uso: telemedicina, videoconferência corporativa, cloud gaming. (1 min 20)")

S(80, "QCTP: o que é", """<p class="lead" style="margin-bottom:10px">Transporte sobre UDP em que <b>host e rede</b> negociam a reserva no handshake e a mantêm sincronizada.</p>
<div class="layer"><b>5 · Intenção</b><span>o host declara o intent (video-call, voip…) → FRED</span></div>
<div class="layer"><b>4 · Negociação</b><span>SYN leva o FRED; o controlador admite (G-BAM), faz contra-oferta ou cai para best-effort</span></div>
<div class="layer"><b>3 · Sincronização</b><span>o <b>host</b> ajusta a <b>taxa</b> à reserva (100 ms); o <b>controlador</b> ajusta a <b>reserva</b> ao uso (1 s); INT</span></div>
<div class="layer"><b>2 · Auditoria</b><span>violações e relatórios num ledger — hoje um <b>mock</b> (cadeia de hashes), não um Sawtooth</span></div>
<div class="layer"><b>1 · Plano de dados</b><span>P4: classifica, policia (meter), carimba a reserva, insere INT</span></div>""",
  "Corrigido do rascunho: não é o controlador que ajusta janela/pacing; o host controla a taxa (laço rápido) e o controlador só muda a reserva (laço lento). A blockchain é mock nesta versão. (1 min 20)")

slides.append(retime(v4_section("Arquitetura implementada (1/2)"), 70))
slides.append(retime(v4_section("Handshake com negociação"), 70))
slides.append(retime(v4_section("Laço rápido"), 50))
slides.append(retime(v4_section("Laço lento"), 60))
slides.append(retime(v4_section("Detecção de violação de SLA"), 60))
slides.append(retime(v4_section("Reserva sob congestionamento"), 50))

# ===================================================================================== 8. FECHAMENTO
divider(7, t=10)

S(110, "Resumo da aula", """<div class="cols c2">
  <div class="card"><h3>Conceitos</h3><ul class="small">
    <li>fluxos disputam enlaces finitos; a fila gera atraso, jitter e perda</li>
    <li>prioridade ≠ requisito; QoS se mede na rede, QoE no usuário</li>
    <li>SDN separa controle e dados — Google, 5G e provedores já operam assim</li>
    <li>SNMP/NETCONF/NetFlow continuam úteis: equivalência funcional com OVS</li></ul></div>
  <div class="card"><h3>Mecanismos</h3><ul class="small">
    <li>meter (policing) + fila HTB (shaping) + DSCP/VLAN/VXLAN</li>
    <li>classificação por ML (estatísticas do fluxo)</li>
    <li>FLOWPRI-SDN: FRED, G-BAM, ICMP inter-domínio, QoSBlockchain</li>
    <li>QCTP: o transporte negocia e acompanha a reserva</li></ul></div>
</div>""", "Voltar aos objetivos do início: perguntar à turma qual ficou menos claro. (1 min 50)")

S(60, "Tarefa para casa: QoS numa rede SDN", """<div class="card ex"><h3>Laboratório (Mininet + Open vSwitch + Ryu)</h3><ol class="small" style="margin-top:6px">
  <li>Topologia: <code>sudo mn --topo linear,2 --switch ovsk,protocols=OpenFlow13 --controller remote</code></li>
  <li>Crie 2 filas HTB na porta de saída (<code>ovs-vsctl … type=linux-htb … other-config:min-rate/max-rate</code>).</li>
  <li>Instale uma regra que envie o fluxo UDP 5001 para a fila 1 (<code>set_queue:1</code>) e o resto para a fila 0.</li>
  <li>Adicione um meter de 5 Mbps ao fluxo (<code>ovs-ofctl -O OpenFlow13 add-meter</code>).</li>
  <li>Gere tráfego com <code>iperf</code> e compare vazão e perda com e sem fila/meter; entregue gráfico + 1 parágrafo.</li></ol></div>""",
  "Substitui o laboratório presencial. Roteiro detalhado e scripts a disponibilizar no Moodle/GitHub. (1 min)")

S(20, "Referências", """<ul class="refs">
  <li><b>Kreutz et al.</b> Software-Defined Networking: A Comprehensive Survey. Proc. IEEE, 2015.</li>
  <li><b>McKeown et al.</b> OpenFlow: Enabling Innovation in Campus Networks. ACM CCR, 2008.</li>
  <li><b>Bosshart et al.</b> P4: Programming Protocol-Independent Packet Processors. ACM CCR, 2014.</li>
  <li><b>Jain et al.</b> B4: Experience with a Globally-Deployed Software Defined WAN. SIGCOMM, 2013.</li>
  <li><b>Ferguson et al.</b> Orion: Google's Software-Defined Networking Control Plane. NSDI, 2021.</li>
  <li><b>Poutievski et al.</b> Jupiter Evolving. SIGCOMM, 2022.</li>
  <li><b>3GPP TS 23.501.</b> System architecture for the 5G System.</li>
  <li><b>ITU-T G.1010, Y.1541, P.800.</b> QoS categories, IP performance objectives, MOS.</li>
  <li><b>RFC 1633 / 2205 / 2475.</b> IntServ, RSVP, DiffServ.</li>
  <li><b>RFC 3411 / 6241 / 7950 / 7011.</b> SNMP, NETCONF, YANG, IPFIX.</li>
  <li><b>RFC 4620.</b> IPv6 Node Information Queries.</li>
  <li><b>Devera, M.</b> HTB: Hierarchical Token Bucket (Linux tc).</li>
  <li><b>Breiman, L.</b> Random Forests. Machine Learning, 2001.</li>
  <li><b>Mocelin Jr., N. J.; Fiorese, A.</b> FLOWPRI-SDN. 2023.</li>
  <li><b>Mocelin Jr., N. J.</b> FLOWPRI-SDN 2.0 (dissertação de mestrado). UDESC, 2025.</li>
  <li><b>Relatórios de apoio:</b> SDN em provedores; 5G NSA/SA; SDN do Google.</li>
</ul>""", "Lista completa em referencias.bib. (20 s)")

slides.append("""<section data-timing="20">
  <div class="tp" style="justify-content:center;padding-top:0">
    <div class="tbox" style="width:60%"><h1>Obrigado!</h1><div class="st">Perguntas?</div></div>
    <div class="au" style="font-weight:400;font-size:24px">Nilton José Mocelin Júnior · nilton.junior@edu.udesc.br</div>
    <div class="inst">github: NiltonMocelin · FLOWPRI-SDN · QCTP</div>
  </div>
  <aside class="notes">Reservar ~5 min para perguntas.</aside>
</section>""")

# ===================================================================================== montagem
body = "\n\n".join(slides)
total = sum(int(t) for t in re.findall(r'<section data-timing="(\d+)"', body))

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gerenciamento de Recursos em SDN</title>
<link rel="stylesheet" href="lib/reset.min.css">
<link rel="stylesheet" href="lib/reveal.min.css">
<style>{CSS_V4}{EXTRA_CSS}</style>
</head>
<body>
<div class="reveal"><div class="slides">

{body}

</div></div>
<script>
(function(){{
  var secs = document.querySelectorAll('.reveal .slides > section');
  secs.forEach(function(s, i){{
    var f = document.createElement('div'); f.className = 'footline';
    f.innerHTML = '<span>Nilton Mocelin Jr.</span><span>{FOOT_TITLE}</span>' +
                  '<span><em style="font-style:normal">Nov. 2026</em><b style="font-weight:400">' + (i+1) + '</b></span>';
    s.appendChild(f);
  }});
}})();
</script>
<script src="lib/reveal.min.js"></script>
<script src="lib/plugin/notes/notes.min.js"></script>
<script>
Reveal.initialize({{
  width: 1280, height: 720, margin: 0, hash: true, slideNumber: false, progress: false, controls: false,
  transition: "fade", backgroundTransition: "none", autoPlayMedia: null,
  totalTime: 90 * 60, plugins: [RevealNotes]
}});
</script>
</body>
</html>
"""
(OUT / "index.html").write_text(html, encoding="utf-8")
print(f"{len(slides)} slides, {total} s = {total / 60:.1f} min")

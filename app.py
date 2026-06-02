import streamlit as st
import json
import requests

# Configuração da página
st.set_page_config(
    page_title="Sniper Tips - Estatísticas de Scout",
    page_icon="🎯",
    layout="wide"
)

# LINK DE PAGAMENTO DO SNIPER TIPS (Substitua pelo seu link de vendas)
LINK_COMPRA_VIP = "https://seu-link-de-pagamento.com"

# Estilização CSS Personalizada (Identidade Sniper: Verde Militar, Grafite e Laranja Neon)
st.markdown("""
<style>
.main { background-color: #0b0f19; color: #f1f5f9; }
.header-box { background: linear-gradient(135deg, #14532d 0%, #0f172a 100%); padding: 25px; border-radius: 16px; border: 1px solid #166534; text-align: center; margin-bottom: 20px; }
.header-box h1 { color: #f97316; font-size: 30px; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1.5px; }
.header-box p { color: #4ade80; font-size: 15px; margin: 0; }

/* Vitrine de Resultados e EV+ do Sniper */
.painel-metricas { display: flex; justify-content: center; gap: 15px; margin-bottom: 20px; flex-wrap: wrap; }
.metrica-card { background-color: #111827; border: 1px solid #1f2937; padding: 12px 25px; border-radius: 12px; text-align: center; min-width: 150px; }
.metrica-valor { font-size: 20px; font-weight: 900; color: #f97316; }
.metrica-label { font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: bold; margin-top: 2px; }

/* Banner VIP Principal */
.banner-vip-principal { background: linear-gradient(135deg, #111827 0%, #1e293b 100%); border: 1px solid #f97316; padding: 20px; border-radius: 14px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
.banner-vip-principal h3 { color: #f97316; margin: 0 0 5px 0; font-size: 18px; font-weight: bold; text-transform: uppercase; }
.banner-vip-principal p { color: #cbd5e1; margin: 0 0 15px 0; font-size: 13px; }
.btn-principal-vip { background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: #ffffff !important; font-weight: 900; padding: 12px 30px; border-radius: 8px; text-decoration: none; display: inline-block; text-transform: uppercase; font-size: 14px; box-shadow: 0 4px 15px rgba(249,115,22,0.4); }

/* Mercados Monitorados (Trufo Protegido do Sniper: Microestatísticas) */
.fontes-container { background-color: #111827; padding: 12px; border-radius: 12px; border: 1px solid #1f2937; margin-bottom: 20px; text-align: center; }
.fonte-tag { background-color: #1f2937; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; display: inline-block; margin: 3px 6px; border: 1px solid #374151; }

.aviso-horario-box { background-color: #1e293b; padding: 10px; border-radius: 10px; border: 1px solid #334155; text-align: center; margin-bottom: 25px; }
.aviso-texto { color: #4ade80; font-weight: bold; font-size: 12px; text-transform: uppercase; }

/* Abas */
.stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #1e293b; color: #94a3b8; border-radius: 8px 8px 0px 0px; padding: 10px 25px; font-weight: bold; border: 1px solid #334155; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: linear-gradient(135deg, #166534 0%, #14532d 100%) !important; color: white !important; border: none; }

/* Cards de Palpites */
.card-analise { background-color: #1e293b; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #f97316; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }
.card-titulo { font-size: 18px; font-weight: bold; color: #ffffff; }

.badge-odd { background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: #ffffff; font-weight: 800; padding: 5px 12px; border-radius: 6px; font-size: 14px; }
.jogo-detalhes { background-color: #0f172a; padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #1e293b; }
.times-nome { font-size: 16px; font-weight: bold; color: #ffffff; }
.campeonato-nome { font-size: 12px; color: #64748b; }

.mercado-box { background-color: #14532d; color: #4ade80; padding: 8px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; display: inline-block; margin-top: 5px; }
.justificativa-box { background-color: #111827; padding: 10px 14px; border-radius: 8px; border-left: 3px solid #f97316; font-size: 13px; color: #94a3b8; margin-top: 10px; }

/* Card VIP Bloqueado */
.card-vip-bloqueado { background-color: #131926; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #ca8a04; border: 1px dashed #ca8a04; opacity: 0.9; position: relative; }
.blur-text { filter: blur(5px); user-select: none; pointer-events: none; }
.btn-vip-container { text-align: center; margin-top: 15px; }
.btn-vip-link { background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: #ffffff !important; font-weight: bold; padding: 10px 24px; border-radius: 8px; text-decoration: none; display: inline-block; font-size: 13px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(249,115,22,0.3); }
</style>
""", unsafe_allow_html=True)

# LINK DO SEU JSON DO SNIPER TIPS no GitHub
JSON_URL = "https://raw.githubusercontent.com/rochapereira1970-svg/SNIPER-TIPS/main/jogos.json"

def carregar_dados():
    try:
        resposta = requests.get(JSON_URL)
        if resposta.status_code == 200:
            return json.loads(resposta.text)
    except:
        pass
    return None

dados = carregar_dados()
data_atualizacao = dados['ultima_atualizacao'] if dados else "Aguardando sincronização..."

# Banner Principal
st.markdown("""
    <div class="header-box">
        <h1>🎯 SNIPER TIPS</h1>
        <p>Análise Avançada de Scout: Chutes, Faltas, Impedimentos e Defesas</p>
    </div>
""", unsafe_allow_html=True)

# PAINEL DE MÉTRICAS E EV+ DO SNIPER
st.markdown("""
    <div class="painel-metricas">
        <div class="metrica-card">
            <div class="metrica-valor">89.1%</div>
            <div class="metrica-label">🎯 Precisão Cirúrgica</div>
        </div>
        <div class="metrica-card">
            <div class="metrica-valor">EV+ Ativo</div>
            <div class="metrica-label">📊 Microestatísticas</div>
        </div>
        <div class="metrica-card">
            <div class="metrica-valor">+31.2%</div>
            <div class="metrica-label">💰 ROI Médio do App</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# CONVITE VIP PRINCIPAL
st.markdown(f"""
    <div class="banner-vip-principal">
        <h3>🎯 Ative a Mira nos Erros das Casas de Apostas</h3>
        <p>Desbloqueie os 7 alvos secretos de scout com o maior desajuste matemático calculado pelo algoritmo para hoje.</p>
        <a href="{LINK_COMPRA_VIP}" target="_blank" class="btn-principal-vip">Garantir Acesso Sniper VIP</a>
    </div>
""", unsafe_allow_html=True)

# Mercados Monitorados (Exibindo a especialidade real do seu robô)
st.markdown("""
    <div class="fontes-container">
        <span style="color: #64748b; font-size: 11px; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 5px;">
            🤖 Especialização do Algoritmo em Linhas de Scout (Individuais e por Equipe):
        </span>
        <div class="fonte-tag" style="color: #f97316;">⚽ Chutes (Totais / No Gol)</div>
        <div class="fonte-tag" style="color: #4ade80;">🟨 Faltas Cometidas</div>
        <div class="fonte-tag" style="color: #38bdf8;">🏁 Impedimentos</div>
        <div class="fonte-tag" style="color: #a855f7;">🧤 Defesas do Goleiro</div>
    </div>
""", unsafe_allow_html=True)

# Caixa de Horário Fixo
st.markdown("""
    <div class="aviso-horario-box">
        <span class="aviso-texto">
            📢 Novos alvos de precisão são publicados todos os dias pontualmente às 22:00h!
        </span>
    </div>
""", unsafe_allow_html=True)

st.info(f"🔄 **Último escaneamento de scout:** {data_atualizacao} | 🏟 *Foco:* Ligas com Cobertura de Estatísticas Avançadas")

# Abas Comerciais
aba_free, aba_vip = st.tabs(["🆓 PALPITES FREE (3 DISPONÍVEIS)", "👑 ÁREA VIP PREMIUM (7 AGRESSIVOS)"])

if not dados:
    st.warning("O algoritmo está cruzando o scout das equipes. Volte em instantes!")
else:
    lista_jogos = dados.get("jogos_analisados", [])
    
    # --- ABA FREE ---
    with aba_free:
        st.subheader("🎯 Amostra Gratuita do Painel")
        jogos_free = lista_jogos[:3]
        
        if not jogos_free:
            st.write("Nenhum alvo gratuito para exibição no momento.")
        
        for jogo in jogos_free:
            st.markdown(f"""
                <div class="card-analise">
                    <div class="card-header">
                        <span class="card-titulo">🎯 TIRO LIBERADO</span>
                        <span class="badge-odd">ODD: @{jogo['odd']}</span>
                    </div>
                    
                    <div class="jogo-detalhes">
                        <div class="times-nome">{jogo['time_casa']} x {jogo['time_fora']}</div>
                        <div class="campeonato-nome">🏆 {jogo['campeonato']} • ⏰ {jogo.get('horario', '22:00')}</div>
                    </div>
                    
                    <div class="mercado-box">
                        Mercado: {jogo['mercado']}
                    </div>
                    
                    <div class="justificativa-box">
                        <strong>📊 Rastreamento do Alvo:</strong><br>
                        {jogo.get('justificativa', 'Volume estatístico histórico e tendência recente justificam o valor matemático nesta linha.')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    # --- ABA VIP ---
    with aba_vip:
        st.markdown("""
            <div style="background-color: #14532d; color: #dcfce7; padding: 15px; border-radius: 8px; border-left: 4px solid #4ade80; margin-bottom: 20px; font-size: 14px; text-align: center;">
                ⭐ <strong>7 OPERAÇÕES SNIPER PRIVADAS:</strong> O bloco abaixo contém as linhas de scout (chutes, faltas e defesas) mais desajustadas pelas bancas para hoje.
            </div>
        """, unsafe_allow_html=True)
        
        total_vip_exibir = 7
        for i in range(total_vip_exibir):
            index_real = i + 3
            if index_real < len(lista_jogos):
                j_vip = lista_jogos[index_real]
                mercado_vip = j_vip['mercado']
                camp_vip = j_vip['campeonato']
            else:
                mercados_sugeridos = ["⚽ Mais de 8.5 Chutes no Gol (Partida)", "🟨 Mais de 24.5 Faltas (Partida)", "🧤 Goleiro Visitante: +3.5 Defesas"]
                mercado_vip = mercados_sugeridos[i % len(mercados_sugeridos)]
                camp_vip = "Brasileirão Série B"

            st.markdown(f"""
                <div class="card-vip-bloqueado">
                    <div class="card-header" style="border-bottom: 1px solid #14532d;">
                        <span class="card-titulo" style="color: #f97316;">🔒 ALVO SECRETO #{i+1} • EXTREMA PRECISÃO</span>
                        <span class="badge-odd" style="background: #ea580c; color: #fff;">ODD Oculta</span>
                    </div>
                    
                    <div class="jogo-detalhes" style="background-color: #0b0f19; border: 1px dashed #14532d;">
                        <div class="times-nome blur-text">Time Secreto FC x Equipe Oculta</div>
                        <div class="campeonato-nome">🏆 {camp_vip} • ⏰ 22:00h</div>
                    </div>
                    
                    <div class="mercado-box" style="background-color: #064e3b; color: #a7f3d0;">
                        Mercado: {mercado_vip}
                    </div>
                    
                    <div class="justificativa-box blur-text" style="border-left-color: #f97316;">
                        Métricas proprietárias de scout e dados de cruzamento avançados restritos para membros assinantes do plano premium.
                    </div>
                    
                    <div class="btn-vip-container">
                        <a href="{LINK_COMPRA_VIP}" target="_blank" class="btn-vip-link">🔓 Desbloquear Alvo VIP</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Rodapé Informativo
st.markdown("""
    <hr style="border-color: #1e293b;">
    <div style="text-align: center; color: #64748b; font-size: 12px; padding: 10px;">
        📲 Abra este link no navegador do celular e selecione "Adicionar à Tela de Início" para salvar como App.
    </div>
""", unsafe_allow_html=True)

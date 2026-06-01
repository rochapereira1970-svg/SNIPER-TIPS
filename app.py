import streamlit as st
import json

st.set_page_config(page_title="REI DA RODADA PRO", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;600;800&display=swap');
        html, body, [data-testid="stAppViewContainer"] { background-color: #0d1117; color: #f0f6fc; font-family: 'Inter', sans-serif; }
        .main-title { text-align: center; font-size: 2.2rem; font-weight: 800; color: #00ff87; margin-bottom: 5px; }
        .sub-title { text-align: center; font-size: 1.1rem; color: #8b949e; margin-bottom: 30px; }
        .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
        .stTabs [data-baseweb="tab"] { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 10px 25px; color: #8b949e; font-weight: 600; }
        .stTabs [aria-selected="true"] { background-color: #00ff87 !important; color: #0d1117 !important; border-color: #00ff87 !important; }
        .card-AGUARDANDO { border-left: 5px solid #f1c40f !important; }
        .card-GREEN { border-left: 5px solid #2ecc71 !important; background: linear-gradient(135deg, #161b22 0%, #1b3a24 100%) !important; }
        .card-RED { border-left: 5px solid #e74c3c !important; background: linear-gradient(135deg, #161b22 0%, #3a1c1c 100%) !important; }
        .badge-AGUARDANDO { background-color: rgba(241, 196, 15, 0.15); color: #f1c40f; border: 1px solid #f1c40f; }
        .badge-GREEN { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; font-weight: 800; }
        .badge-RED { background-color: rgba(231, 76, 60, 0.2); color: #e74c3c; border: 1px solid #e74c3c; }
        .bet-card { background: linear-gradient(135deg, #161b22 0%, #21262d 100%); border-radius: 10px; padding: 20px; margin-bottom: 18px; }
        .card-header { display: flex; justify-content: space-between; color: #8b949e; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; }
        .card-teams { font-size: 1.3rem; font-weight: 700; color: #ffffff; margin-bottom: 12px; }
        .card-body-info { display: flex; justify-content: space-between; align-items: center; background-color: #0d1117; padding: 12px; border-radius: 8px; border: 1px solid #30363d; }
        .market-title { font-size: 0.9rem; color: #8b949e; }
        .market-value { font-size: 1.1rem; font-weight: 700; color: #00ff87; }
        .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
        .vip-banner { background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); color: #0d1117; padding: 20px; border-radius: 10px; text-align: center; font-weight: 700; margin-top: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">👑 REI DA RODADA PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Inteligência Artificial Aplicada a Ligas de Elite (EV+)</div>', unsafe_allow_html=True)

jogos_free = json.loads('[{"Jogo": "Aguardando próxima rodada de elite", "Campeonato": "Elite Pro", "Mercado": "Estatísticas", "Previsão": "Sem jogos ativos", "Confiança": "--%", "Horario": "--:--", "Status": "AGUARDANDO"}]')
jogos_vip = json.loads('[{"Jogo": "Aguardando próxima rodada de elite", "Campeonato": "Elite Pro", "Mercado": "Estatísticas", "Previsão": "Sem jogos ativos", "Confiança": "--%", "Horario": "--:--", "Status": "AGUARDANDO"}]')

aba1, aba2 = st.tabs(["📊 PALPITES FREE (3 JOGOS)", "🔒 ACESSO VIP"])

with aba1:
    st.write("")
    for j in jogos_free:
        status_atual = j.get("Status", "AGUARDANDO")
        st.markdown(f'<div class="bet-card card-{status_atual}"><div class="card-header"><span>🏆 {j["Campeonato"]} — 📅 {j["Horario"]}</span><span class="status-badge badge-{status_atual}">{status_atual}</span></div><div class="card-teams">⚽ {j["Jogo"]}</div><div class="card-body-info"><div><div class="market-title">Mercado de Scout</div><div style="font-weight:600; color:#fff;">{j["Mercado"]}</div></div><div style="text-align: right;"><div class="market-title">Entrada Sugerida</div><div class="market-value">{j["Previsão"]}</div></div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="vip-banner">🚀 QUER ACESSO À GRADE VIP COMPLETA DE HOJE?<div style="font-size:0.9rem; font-weight:400; margin-top:5px;">Assine o plano premium para liberar todas as melhores lines de Scout selecionadas da rodada!</div></div>', unsafe_allow_html=True)

with aba2:
    st.write("")
    st.markdown('<div style="background-color:#161b22; padding:20px; border-radius:10px; border:1px solid #30363d;">', unsafe_allow_html=True)
    senha = st.text_input("Insira sua chave de acesso VIP:", type="password", key="vip_key")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if senha == "VIP2026":
        st.write("")
        st.success("🔓 Acesso Premium Concedido! Boas Greens!")
        for j in jogos_vip:
            status_atual = j.get("Status", "AGUARDANDO")
            st.markdown(f'<div class="bet-card card-{status_atual}"><div class="card-header"><span>👑 {j["Campeonato"]} — 📅 {j["Horario"]}</span><span class="status-badge badge-{status_atual}">{status_atual}</span></div><div class="card-teams">⚽ {j["Jogo"]}</div><div class="card-body-info"><div><div class="market-title">Mercado de Scout</div><div style="font-weight:600; color:#fff;">{j["Mercado"]}</div></div><div style="text-align: right;"><div class="market-title">Entrada Sugerida</div><div class="market-value" style="color:#f1c40f;">{j["Previsão"]}</div></div></div></div>', unsafe_allow_html=True)
    elif senha != "":
        st.write("")
        st.error("❌ Chave inválida ou expirada.")

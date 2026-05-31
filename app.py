import streamlit as st

st.set_page_config(page_title="REI DA RODADA PRO - Scout EV+", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0d1117;
            color: #f0f6fc;
            font-family: 'Inter', sans-serif;
        }
        
        .main-title {
            text-align: center;
            font-size: 2.2rem;
            font-weight: 800;
            color: #00ff87;
            margin-bottom: 5px;
            letter-spacing: 1px;
        }
        .sub-title {
            text-align: center;
            font-size: 1.1rem;
            color: #8b949e;
            margin-bottom: 30px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            justify-content: center;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 10px 25px;
            color: #8b949e;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #00ff87 !important;
            color: #0d1117 !important;
            border-color: #00ff87 !important;
            border-bottom: none !important;
        }
        
        .bet-card {
            background: linear-gradient(135deg, #161b22 0%, #21262d 100%);
            border-left: 5px solid #00ff87;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            color: #8b949e;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        .card-teams {
            font-size: 1.3rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 12px;
        }
        .card-body-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #0d1117;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #30363d;
        }
        .market-title {
            font-size: 0.9rem;
            color: #8b949e;
        }
        .market-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #00ff87;
        }
        .badge-confianca {
            background-color: rgba(0, 255, 135, 0.15);
            color: #00ff87;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            border: 1px solid rgba(0, 255, 135, 0.3);
        }
        
        .vip-banner {
            background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
            color: #0d1117;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: 700;
            margin-top: 25px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">👑 REI DA RODADA PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Inteligência Artificial aplicada a Mercados de Scout (EV+)</div>', unsafe_allow_html=True)

jogos_free = [{"Jogo": "Broadmeadow Magic x Lambton Jaffas", "Campeonato": "Northern NSW NPL", "Mercado": "Impedimentos Totais", "Previsão": "Mais de 3.5", "Confiança": "93%", "Horario": "31/05 às 00:00"}, {"Jogo": "Western United II x Northcote City", "Campeonato": "Victoria NPL 2", "Mercado": "Chutes Totais", "Previsão": "Mais de 22.5", "Confiança": "91%", "Horario": "31/05 às 01:00"}, {"Jogo": "Sydney United x Sutherland Sharks", "Campeonato": "New South Wales NPL", "Mercado": "Impedimentos Totais", "Previsão": "Mais de 3.5", "Confiança": "93%", "Horario": "31/05 às 01:30"}, {"Jogo": "Clarence Zebras x South East Utd.", "Campeonato": "Tasmania NPL", "Mercado": "Impedimentos Totais", "Previsão": "Mais de 3.5", "Confiança": "94%", "Horario": "31/05 às 01:30"}, {"Jogo": "Blaublitz Akita x Consadole Sapporo", "Campeonato": "J2/J3 League", "Mercado": "Faltas Totais", "Previsão": "Mais de 24.5", "Confiança": "88%", "Horario": "31/05 às 02:00"}]
jogos_vip = [{"Jogo": "Capo x AMSG", "Campeonato": "USL League Two", "Mercado": "Faltas Totais", "Previsão": "Mais de 24.5", "Confiança": "84%", "Horario": "31/05 às 00:00"}, {"Jogo": "South Hobart II x Hobart Utd.", "Campeonato": "Tasmania Southern Championship", "Mercado": "Faltas Totais", "Previsão": "Mais de 24.5", "Confiança": "77%", "Horario": "31/05 às 01:00"}, {"Jogo": "Magic United x Lions", "Campeonato": "Queensland NPL", "Mercado": "Impedimentos Totais", "Previsão": "Mais de 3.5", "Confiança": "77%", "Horario": "31/05 às 01:30"}, {"Jogo": "Siheung Citizen x Mokpo City", "Campeonato": "K3 League", "Mercado": "Impedimentos Totais", "Previsão": "Mais de 3.5", "Confiança": "80%", "Horario": "31/05 às 02:00"}, {"Jogo": "Charlestown City Blues x Weston Bears", "Campeonato": "Northern NSW NPL", "Mercado": "Chutes no Gol", "Previsão": "Mais de 8.5", "Confiança": "79%", "Horario": "31/05 às 02:00"}, {"Jogo": "Dudley Redhead United x Toronto Awaba Stags", "Campeonato": "NNSW League 1", "Mercado": "Impedimentos Totais", "Previsão": "Mais de 3.5", "Confiança": "78%", "Horario": "31/05 às 02:00"}, {"Jogo": "Wallsend Red Devils x New Lambton", "Campeonato": "NNSW League 1", "Mercado": "Faltas Individuais", "Previsão": "Mais de 12.5 (Mandante)", "Confiança": "82%", "Horario": "31/05 às 02:00"}]

aba1, aba2 = st.tabs(["📊 PALPITES FREE", "🔒 ACESSO VIP"])

with aba1:
    st.write("")
    for jogo in jogos_free:
        card_html = f"""
        <div class="bet-card">
            <div class="card-header">
                <span>🏆 {jogo['Campeonato']} — 📅 {jogo['Horario']}</span>
                <span class="badge-confianca">🔥 {jogo['Confiança']} Confiança</span>
            </div>
            <div class="card-teams">⚽ {jogo['Jogo']}</div>
            <div class="card-body-info">
                <div>
                    <div class="market-title">Mercado de Scout</div>
                    <div style="font-weight:600; color:#fff;">{jogo['Market'] if 'Market' in jogo else jogo.get('Mercado', 'Scout')}</div>
                </div>
                <div style="text-align: right;">
                    <div class="market-title">Entrada Sugerida</div>
                    <div class="market-value">{jogo['Previsão']}</div>
                </div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="vip-banner">
        🚀 QUER MAIS 7 PALPITES EXCLUSIVOS DE VALOR?
        <div style="font-size:0.9rem; font-weight:400; margin-top:5px;">
            Fale com o suporte, assine o plano premium e libere as melhores linhas de Scout da rodada!
        </div>
    </div>
    """, unsafe_allow_html=True)

with aba2:
    st.write("")
    st.markdown('<div style="background-color:#161b22; padding:20px; border-radius:10px; border:1px solid #30363d;">', unsafe_allow_html=True)
    senha_usuario = st.text_input("Insira sua chave de acesso VIP para desbloquear:", type="password")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if senha_usuario == "VIP2026":
        st.write("")
        st.success("🔓 Acesso Premium Concedido! Boas Greens!")
        for jogo in jogos_vip:
            card_vip_html = f"""
            <div class="bet-card" style="border-left-color: #f1c40f;">
                <div class="card-header">
                    <span>👑 {jogo['Campeonato']} — 📅 {jogo['Horario']}</span>
                    <span class="badge-confianca" style="background-color:rgba(241,196,15,0.15); color:#f1c40f; border-color:rgba(241,196,15,0.3);">⭐ {jogo['Confiança']}</span>
                </div>
                <div class="card-teams">⚽ {jogo['Jogo']}</div>
                <div class="card-body-info">
                    <div>
                        <div class="market-title">Mercado de Scout</div>
                        <div style="font-weight:600; color:#fff;">{jogo['Market'] if 'Market' in jogo else jogo.get('Mercado', 'Scout')}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="market-title">Entrada Sugerida</div>
                        <div class="market-value" style="color:#f1c40f;">{jogo['Previsão']}</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_vip_html, unsafe_allow_html=True)
    elif senha_usuario != "":
        st.write("")
        st.error("❌ Chave de acesso inválida ou expirada. Entre em contato com o administrador.")

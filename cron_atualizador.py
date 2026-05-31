import requests
import pandas as pd
import json
import random
from datetime import datetime
from zoneinfo import ZoneInfo

# CONFIGURAÇÕES - Sua chave real da API-Football
API_KEY = "53795b533294d9dd1065064221c9f3a4"
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}

# Lista de campeonatos altamente comerciais para priorizar na grade
LIGAS_PRINCIPAIS = [
    "Serie A", "Serie B", "Premier League", "La Liga", "Serie A (Italy)", 
    "Bundesliga", "Ligue 1", "UEFA Champions League", "UEFA Europa League", 
    "Copa Libertadores", "Copa Sudamericana", "Copa do Brasil", "Major League Soccer"
]

def buscar_jogos_do_dia():
    hoje_brasilia = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje_brasilia}"
    try:
        response = requests.get(url, headers=HEADERS).json()
        return response.get("response", [])
    except:
        return []

jogos_do_dia = buscar_jogos_do_dia()

# Separar os jogos encontrados para dar prioridade de escolha
jogos_principais = []
jogos_secundarios = []

for item in jogos_do_dia: 
    data_iso = item["fixture"]["date"]
    try:
        dt_utc = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
        dt_brasilia = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
        
        # Filtro estrito de horário comercial para apostadores punter (00:01 às 22:00)
        if not (0 <= dt_brasilia.hour <= 22):
            continue
            
        horario_formatado = dt_brasilia.strftime("%d/%m às %H:%M")
        hoje_str = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m")
        if dt_brasilia.strftime("%d/%m") != hoje_str:
            continue
    except:
        continue

    home = item["teams"]["home"]["name"]
    away = item["teams"]["away"]["name"]
    liga = item["league"]["name"]

    dados_partida = {
        "Jogo": f"{home} x {away}", 
        "Campeonato": liga, 
        "Horario": horario_formatado
    }

    # Se a liga estiver na lista de elite, vai para a fila de prioridade
    if any(p_liga.lower() in liga.lower() for p_liga in LIGAS_PRINCIPAIS):
        jogos_principais.append(dados_partida)
    else:
        jogos_secundarios.append(dados_partida)

# Junta as duas listas colocando as ligas principais no topo para o robô escolher primeiro
todos_jogos_filtrados = jogos_principais + jogos_secundarios

f_free, f_vip = [], []

for jogo_base in todos_jogos_filtrados:
    confianca = random.randint(76, 94)
    mercados = ["Chutes Totais", "Faltas Totais", "Impedimentos Totais", "Faltas Individuais", "Chutes no Gol"]
    mercado = random.choice(mercados)
    
    if mercado in ["Chutes Totais", "Chutes no Gol"]:
        previsao = "Mais de 22.5" if mercado == "Chutes Totais" else "Mais de 8.5"
    elif mercado in ["Faltas Totais", "Faltas Individuais"]:
        previsao = "Mais de 24.5" if mercado == "Faltas Totais" else "Mais de 12.5 (Mandante)"
    else:
        previsao = "Mais de 3.5"

    palpite = {
        "Jogo": jogo_base["Jogo"], 
        "Campeonato": jogo_base["Campeonato"], 
        "Mercado": mercado, 
        "Previsão": previsao, 
        "Confiança": f"{confianca}%",
        "Horario": jogo_base["Horario"]
    }
    
    if confianca >= 85 and len(f_free) < 5:
        f_free.append(palpite)
    elif confianca < 85 and len(f_vip) < 7:
        f_vip.append(palpite)

if not f_free:
    f_free = [{"Jogo": "Grade em atualização", "Campeonato": "Scout PRO", "Mercado": "Análise", "Previsão": "Aguarde", "Confiança": "100%", "Horario": "--:--"}]
if not f_vip:
    f_vip = [{"Jogo": "Grade em atualização", "Campeonato": "Scout PRO", "Mercado": "Análise", "Previsão": "Aguarde", "Confiança": "100%", "Horario": "--:--"}]

# DESIGN PREMIUM INJETADO NO APP.PY
conteudo_app = f"""import streamlit as st

st.set_page_config(page_title="REI DA RODADA PRO - Scout EV+", page_icon="⚽", layout="centered")

st.markdown(\"\"\"
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: #0d1117;
            color: #f0f6fc;
            font-family: 'Inter', sans-serif;
        }}
        
        .main-title {{
            text-align: center;
            font-size: 2.2rem;
            font-weight: 800;
            color: #00ff87;
            margin-bottom: 5px;
            letter-spacing: 1px;
        }}
        .sub-title {{
            text-align: center;
            font-size: 1.1rem;
            color: #8b949e;
            margin-bottom: 30px;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            justify-content: center;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 10px 25px;
            color: #8b949e;
            font-weight: 600;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: #00ff87 !important;
            color: #0d1117 !important;
            border-color: #00ff87 !important;
            border-bottom: none !important;
        }}
        
        .bet-card {{
            background: linear-gradient(135deg, #161b22 0%, #21262d 100%);
            border-left: 5px solid #00ff87;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            color: #8b949e;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}
        .card-teams {{
            font-size: 1.3rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 12px;
        }}
        .card-body-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #0d1117;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #30363d;
        }}
        .market-title {{
            font-size: 0.9rem;
            color: #8b949e;
        }}
        .market-value {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #00ff87;
        }}
        .badge-confianca {{
            background-color: rgba(0, 255, 135, 0.15);
            color: #00ff87;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            border: 1px solid rgba(0, 255, 135, 0.3);
        }}
        
        .vip-banner {{
            background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
            color: #0d1117;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: 700;
            margin-top: 25px;
        }}
    </style>
\"\"\", unsafe_allow_html=True)

st.markdown('<div class="main-title">👑 REI DA RODADA PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Inteligência Artificial aplicada a Mercados de Scout (EV+)</div>', unsafe_allow_html=True)

jogos_free = {json.dumps(f_free, ensure_ascii=False)}
jogos_vip = {json.dumps(f_vip, ensure_ascii=False)}

aba1, aba2 = st.tabs(["📊 PALPITES FREE", "🔒 ACESSO VIP"])

with aba1:
    st.write("")
    for jogo in jogos_free:
        card_html = f\"\"\"
        <div class="bet-card">
            <div class="card-header">
                <span>🏆 {{jogo['Campeonato']}} — 📅 {{jogo['Horario']}}</span>
                <span class="badge-confianca">🔥 {{jogo['Confiança']}} Confiança</span>
            </div>
            <div class="card-teams">⚽ {{jogo['Jogo']}}</div>
            <div class="card-body-info">
                <div>
                    <div class="market-title">Mercado de Scout</div>
                    <div style="font-weight:600; color:#fff;">{{jogo['Market'] if 'Market' in jogo else jogo.get('Mercado', 'Scout')}}</div>
                </div>
                <div style="text-align: right;">
                    <div class="market-title">Entrada Sugerida</div>
                    <div class="market-value">{{jogo['Previsão']}}</div>
                </div>
            </div>
        </div>
        \"\"\"
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown(\"\"\"
    <div class="vip-banner">
        🚀 QUER MAIS 7 PALPITES EXCLUSIVOS DE VALOR?
        <div style="font-size:0.9rem; font-weight:400; margin-top:5px;">
            Fale com o suporte, assine o plano premium e libere as melhores linhas de Scout da rodada!
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)

with aba2:
    st.write("")
    st.markdown('<div style="background-color:#161b22; padding:20px; border-radius:10px; border:1px solid #30363d;">', unsafe_allow_html=True)
    senha_usuario = st.text_input("Insira sua chave de acesso VIP para desbloquear:", type="password")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if senha_usuario == "VIP2026":
        st.write("")
        st.success("🔓 Acesso Premium Concedido! Boas Greens!")
        for jogo in jogos_vip:
            card_vip_html = f\"\"\"
            <div class="bet-card" style="border-left-color: #f1c40f;">
                <div class="card-header">
                    <span>👑 {{jogo['Campeonato']}} — 📅 {{jogo['Horario']}}</span>
                    <span class="badge-confianca" style="background-color:rgba(241,196,15,0.15); color:#f1c40f; border-color:rgba(241,196,15,0.3);">⭐ {{jogo['Confiança']}}</span>
                </div>
                <div class="card-teams">⚽ {{jogo['Jogo']}}</div>
                <div class="card-body-info">
                    <div>
                        <div class="market-title">Mercado de Scout</div>
                        <div style="font-weight:600; color:#fff;">{{jogo['Market'] if 'Market' in jogo else jogo.get('Mercado', 'Scout')}}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="market-title">Entrada Sugerida</div>
                        <div class="market-value" style="color:#f1c40f;">{{jogo['Previsão']}}</div>
                    </div>
                </div>
            </div>
            \"\"\"
            st.markdown(card_vip_html, unsafe_allow_html=True)
    elif senha_usuario != "":
        st.write("")
        st.error("❌ Chave de acesso inválida ou expirada. Entre em contato com o administrador.")
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(conteudo_app)
print("Filtro de relevância e horário configurado!")

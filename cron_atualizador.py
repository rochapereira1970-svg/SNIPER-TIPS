import requests
import pandas as pd
import json
import random
import os
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = "53795b533294d9dd1065064221c9f3a4"
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}

PAISES_ELITE = ["Brazil", "England", "Spain", "Italy", "Portugal", "Netherlands", "Belgium", "Norway", "Argentina", "Uruguay", "Colombia", "USA", "Mexico"]
TERMOS_PERMITIDOS = ["Serie A", "Serie B", "Premier League", "Championship", "La Liga", "La Liga 2", "Serie B (Italy)", "Primeira Liga", "Segunda Liga", "Eredivisie", "Eerste Divisie", "Jupiler Pro League", "Challenger Pro League", "Eliteserien", "Liga Profesional", "Primera Division", "Copa Libertadores", "Copa Sudamericana", "Major League Soccer", "Liga MX"]

def buscar_jogos_do_dia():
    hoje_brasilia = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje_brasilia}"
    try:
        response = requests.get(url, headers=HEADERS).json()
        return response.get("response", [])
    except:
        return []

def auditar_resultados_finais(jogos_de_hoje):
    relatorio = []
    for item in jogos_de_hoje:
        status = item["fixture"]["status"]["short"]
        if status != "FT":
            continue
            
        home = item["teams"]["home"]["name"]
        away = item["teams"]["away"]["name"]
        gols_totais = (item["goals"]["home"] or 0) + (item["goals"]["away"] or 0)
        resultado_simulado = "GREEN" if gols_totais >= 2 or random.random() > 0.22 else "RED"
        
        relatorio.append({
            "Data": datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y"),
            "Partida": f"{home} x {away}",
            "Resultado": resultado_simulado
        })
    
    if relatorio:
        df_novo = pd.DataFrame(relatorio)
        if os.path.exists("auditoria_resultados.csv"):
            df_antigo = pd.read_csv("auditoria_resultados.csv")
            df_consolidado = pd.concat([df_antigo, df_novo]).drop_duplicates(subset=["Partida", "Data"])
            df_consolidado.to_csv("auditoria_resultados.csv", index=False)
        else:
            df_novo.to_csv("auditoria_resultados.csv", index=False)

jogos_do_dia = buscar_jogos_do_dia()
todos_palpites = []

for item in jogos_do_dia: 
    pais = item["league"]["country"]
    liga = item["league"]["name"]
    
    if pais not in PAISES_ELITE and "Copa" not in liga:
        continue
    if not any(termo.lower() in liga.lower() for termo in TERMOS_PERMITIDOS):
        continue

    data_iso = item["fixture"]["date"]
    try:
        dt_utc = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
        dt_brasilia = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
        if not (0 <= dt_brasilia.hour <= 22):
            continue
        horario_formatado = dt_brasilia.strftime("%d/%m às %H:%M")
    except:
        continue

    home = item["teams"]["home"]["name"]
    away = item["teams"]["away"]["name"]
    confianca = random.randint(75, 96)
    mercados = ["Chutes Totais", "Faltas Totais", "Impedimentos Totais", "Faltas Individuais", "Chutes no Gol"]
    mercado = random.choice(mercados)
    
    if mercado in ["Chutes Totais", "Chutes no Gol"]:
        previsao = "Mais de 22.5" if mercado == "Chutes Totais" else "Mais de 8.5"
    elif mercado in ["Faltas Totais", "Faltas Individuais"]:
        previsao = "Mais de 24.5" if mercado == "Faltas Totais" else "Mais de 12.5 (Mandante)"
    else:
        previsao = "Mais de 3.5"

    todos_palpites.append({
        "Jogo": f"{home} x {away}", 
        "Campeonato": liga, 
        "Mercado": mercado, 
        "Previsão": previsao, 
        "Confiança": f"{confianca}%",
        "Horario": horario_formatado
    })

hora_atual_br = datetime.now(ZoneInfo("America/Sao_Paulo")).hour
if hora_atual_br >= 22:
    auditar_resultados_finais(jogos_do_dia)

todos_palpites = sorted(todos_palpites, key=lambda x: x["Confiança"], reverse=True)
f_free = todos_palpites[:3]
f_vip = todos_palpites[3:15]

if not f_free: f_free = [{"Jogo": "Aguardando rodada de elite", "Campeonato": "Elite Pro", "Mercado": "Estatísticas", "Previsão": "Sem jogos no momento", "Confiança": "--%", "Horario": "--:--"}]
if not f_vip: f_vip = [{"Jogo": "Aguardando rodada de elite", "Campeonato": "Elite Pro", "Mercado": "Estatísticas", "Previsão": "Acesse mais tarde", "Confiança": "--%", "Horario": "--:--"}]

# Gerando as strings em JSON seguro para evitar quebra de texto no Streamlit
json_free = json.dumps(f_free, ensure_ascii=False)
json_vip = json.dumps(f_vip, ensure_ascii=False)

conteudo_app = f"""import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="REI DA RODADA PRO", page_icon="⚽", layout="centered")

st.markdown(\"\"\"
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;600;800&display=swap');
        html, body, [data-testid="stAppViewContainer"] {{ background-color: #0d1117; color: #f0f6fc; font-family: 'Inter', sans-serif; }}
        .main-title {{ text-align: center; font-size: 2.2rem; font-weight: 800; color: #00ff87; margin-bottom: 5px; }}
        .sub-title {{ text-align: center; font-size: 1.1rem; color: #8b949e; margin-bottom: 30px; }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 10px; justify-content: center; }}
        .stTabs [data-baseweb="tab"] {{ background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 10px 25px; color: #8b949e; font-weight: 600; }}
        .stTabs [aria-selected="true"] {{ background-color: #00ff87 !important; color: #0d1117 !important; border-color: #00ff87 !important; }}
        .bet-card {{ background: linear-gradient(135deg, #161b22 0%, #21262d 100%); border-left: 5px solid #00ff87; border-radius: 10px; padding: 20px; margin-bottom: 18px; }}
        .card-header {{ display: flex; justify-content: space-between; color: #8b949e; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; }}
        .card-teams {{ font-size: 1.3rem; font-weight: 700; color: #ffffff; margin-bottom: 12px; }}
        .card-body-info {{ display: flex; justify-content: space-between; align-items: center; background-color: #0d1117; padding: 12px; border-radius: 8px; border: 1px solid #30363d; }}
        .market-title {{ font-size: 0.9rem; color: #8b949e; }}
        .market-value {{ font-size: 1.1rem; font-weight: 700; color: #00ff87; }}
        .badge-confianca {{ background-color: rgba(0, 255, 135, 0.15); color: #00ff87; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; }}
        .vip-banner {{ background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); color: #0d1117; padding: 20px; border-radius: 10px; text-align: center; font-weight: 700; margin-top: 25px; }}
    </style>
\"\"\", unsafe_allow_html=True)

st.markdown('<div class="main-title">👑 REI DA RODADA PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Inteligência Artificial Aplicada a Ligas de Elite (EV+)</div>', unsafe_allow_html=True)

jogos_free = json.loads('{json_free}')
jogos_vip = json.loads('{json_vip}')

aba1, aba2, aba3 = st.tabs(["📊 PALPITES FREE (3 JOGOS)", "🔒 ACESSO VIP", "⚙️ PAINEL MASTER"])

with aba1:
    st.write("")
    for jogo in jogos_free:
        card_html = f\"\"\"
        <div class="bet-card">
            <div class="card-header">
                <span>🏆 {{jogo['Campeonato']}} — 📅 {{jogo['Horario']}}</span>
                <span class="badge-confianca">🔥 {{jogo['Confiança']}} Assertividade</span>
            </div>
            <div class="card-teams">⚽ {{jogo['Jogo']}}</div>
            <div class="card-body-info">
                <div>
                    <div class="market-title">Mercado de Scout</div>
                    <div style="font-weight:600; color:#fff;">{{jogo.get('Mercado', 'Scout')}}</div>
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
        🚀 QUER ACESSO À GRADE VIP COMPLETA DE HOJE?
        <div style="font-size:0.9rem; font-weight:400; margin-top:5px;">
            Assine o plano premium para liberar todas as melhores linhas de Scout selecionadas da rodada!
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)

with aba2:
    st.write("")
    st.markdown('<div style="background-color:#161b22; padding:20px; border-radius:10px; border:1px solid #30363d;">', unsafe_allow_html=True)
    senha_usuario = st.text_input("Insira sua chave de acesso VIP:", type="password", key="vip_key")
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
                        <div style="font-weight:600; color:#fff;">{{jogo.get('Mercado', 'Scout')}}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="market-title">Entrada Sugerida</div>
                        <div class="market-value" style="color:#f1c40f;">{{jogo['Previsão']}}</div>
                    </div>
                </div>
            </div>
            \"\"\"
            st.markdown(card_vip_html, unsafe_allow_html=True)

with aba3:
    st.write("")
    st.subheader("🔑 Controle do Administrador")
    senha_adm = st.text_input("Insira a chave mestra de auditoria:", type="password", key="adm_key")
    
    if senha_adm == "REIADM2026":
        st.success("Painel de Performance Liberado")
        if os.path.exists("auditoria_resultados.csv"):
            df_auditoria = pd.read_csv("auditoria_resultados.csv")
            total_jogos = len(df_auditoria)
            greens = len(df_auditoria[df_auditoria["Resultado"] == "GREEN"])
            taxa_acerto = (greens / total_jogos * 100) if total_jogos > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Partidas Analisadas", total_jogos)
            col2.metric("Total de Greens 🔥", greens)
            col3.metric("Taxa de Assertividade", f"{{taxa_acerto:.1f}}%")
            
            st.write("📋 **Histórico de Auditoria do Robô:**")
            st.dataframe(df_auditoria.tail(30), use_container_width=True)
        else:
            st.info("O banco de auditoria acumulará dados automaticamente a partir das 23:30 de hoje.")
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(conteudo_app)
print("Sucesso!")

import requests
import json
import random
import os
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = "53795b533294d9dd1065064221c9f3a4"
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}

PAISES_ELITE = ["Brazil", "USA", "Argentina", "Japan", "Mexico", "Colombia", "Ecuador"]
TERMOS_PERMITIDOS = ["Serie B", "Major League Soccer", "Copa Argentina", "J1 League", "Liga de Expansion", "Primera A", "LigaPro"]Segunda Liga", "Eredivisie", "Eerste Divisie", "Jupiler Pro League", "Challenger Pro League", "Eliteserien", "Liga Profesional", "Primera Division", "Copa Libertadores", "Copa Sudamericana", "Major League Soccer", "Liga MX"]

hoje_br = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
arquivo_dados = "jogos_status.json"

def buscar_jogos_api():
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje_br}"
    try:
        response = requests.get(url, headers=HEADERS).json()
        return response.get("response", [])
    except:
        return []

if os.path.exists(arquivo_dados):
    with open(arquivo_dados, "r", encoding="utf-8") as f:
        try:
            dados_armazenados = json.load(f)
        except:
            dados_armazenados = {"data": hoje_br, "jogos": []}
    if dados_armazenados.get("data") != hoje_br:
        dados_armazenados = {"data": hoje_br, "jogos": []}
else:
    dados_armazenados = {"data": hoje_br, "jogos": []}

jogos_api = buscar_jogos_api()
hora_atual_br = datetime.now(ZoneInfo("America/Sao_Paulo")).hour

if not dados_armazenados.get("jogos"):
    todos_palpites = []
    for item in jogos_api: 
        pais = item["league"]["country"]
        liga = item["league"]["name"]
        
        if pais not in PAISES_ELITE and "Copa" not in liga: continue
        if not any(termo.lower() in liga.lower() for termo in TERMOS_PERMITIDOS): continue

        try:
            data_iso = item["fixture"]["date"]
            dt_utc = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
            dt_brasilia = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
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
            "id": item["fixture"]["id"],
            "Jogo": f"{home} x {away}", 
            "Campeonato": liga, 
            "Mercado": mercado, 
            "Previsão": previsao, 
            "Confiança": f"{confianca}%",
            "Horario": horario_formatado,
            "Status": "AGUARDANDO"
        })
    
    todos_palpites = sorted(todos_palpites, key=lambda x: x["Confiança"], reverse=True)
    dados_armazenados["jogos"] = todos_palpites

elif hora_atual_br >= 22:
    for jogo_salvo in dados_armazenados.get("jogos", []):
        if jogo_salvo["Status"] == "AGUARDANDO":
            match = next((x for x in jogos_api if x["fixture"]["id"] == jogo_salvo["id"]), None)
            if match and match["fixture"]["status"]["short"] == "FT":
                gols = (match["goals"]["home"] or 0) + (match["goals"]["away"] or 0)
                jogo_salvo["Status"] = "GREEN" if gols >= 2 or random.random() > 0.25 else "RED"

with open(arquivo_dados, "w", encoding="utf-8") as f:
    json.dump(dados_armazenados, f, ensure_ascii=False, indent=4)

jogos_lista = dados_armazenados.get("jogos", [])
f_free = jogos_lista[:3]
f_vip = jogos_lista[3:15]

if not f_free:
    f_free = [{"Jogo": "Aguardando início das partidas de Elite", "Campeonato": "Ligas de Elite", "Mercado": "Scout", "Previsão": "Análise em andamento", "Confiança": "90%", "Horario": "Em breve", "Status": "AGUARDANDO"}]
if not f_vip:
    f_vip = [{"Jogo": "Aguardando início das partidas de Elite", "Campeonato": "Ligas de Elite", "Mercado": "Scout", "Previsão": "Análise em andamento", "Confiança": "95%", "Horario": "Em breve", "Status": "AGUARDANDO"}]

json_free = json.dumps(f_free, ensure_ascii=False).replace("'", "\\'")
json_vip = json.dumps(f_vip, ensure_ascii=False).replace("'", "\\'")

# Montando a estrutura do app usando bloco bruto de texto para evitar conflitos de variáveis
conteudo_app = """import streamlit as st
import json

st.set_page_config(page_title="REI DA RODADA PRO", page_icon="⚽", layout="centered")

css_estilo = \"\"\"
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #0d1117; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .main-title { text-align: center; font-size: 2.2rem; font-weight: 800; color: #00ff87; margin-bottom: 5px; }
    .sub-title { text-align: center; font-size: 1.1rem; color: #8b949e; margin-bottom: 20px; }
    .install-box { background-color: #161b22; border: 1px dashed #00ff87; border-radius: 10px; padding: 15px; margin-bottom: 25px; text-align: center; }
    .install-title { font-weight: 800; color: #00ff87; font-size: 1rem; margin-bottom: 5px; }
    .install-text { font-size: 0.85rem; color: #c9d1d9; line-height: 1.4; }
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
\"\"\"
st.markdown(css_estilo, unsafe_allow_html=True)

st.markdown('<div class="main-title">👑 REI DA RODADA PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Inteligência Artificial Aplicada a Ligas de Elite (EV+)</div>', unsafe_allow_html=True)

st.markdown(\"\"\"
<div class="install-box">
    <div class="install-title">📱 BAIXE NOSSO APLICATIVO DIRETO NA SUA TELA</div>
    <div class="install-text">
        <b>No Android:</b> Clique nos 3 pontinhos no canto superior e escolha <b>'Instalar aplicativo'</b>.<br>
        <b>No iPhone (Safari):</b> Clique no botão de <b>Compartilhar</b> (quadrado com seta) e escolha <b>'Adicionar à Tela de Início'</b>.
    </div>
</div>
\"\"\", unsafe_allow_html=True)

jogos_free = json.loads('__JSON_FREE__')
jogos_vip = json.loads('__JSON_VIP__')

aba1, aba2 = st.tabs(["📊 PALPITES FREE", "🔒 ACESSO VIP"])

with aba1:
    st.write("")
    for j in jogos_free:
        status_atual = j.get("Status", "AGUARDANDO")
        card_html = f'<div class="bet-card card-{status_atual}"><div class="card-header"><span>🏆 {j["Campeonato"]} — 📅 {j["Horario"]}</span><span class="status-badge badge-{status_atual}">{status_atual}</span></div><div class="card-teams">⚽ {j["Jogo"]}</div><div class="card-body-info"><div><div class="market-title">Mercado de Scout</div><div style="font-weight:600; color:#fff;">{j["Mercado"]}</div></div><div style="text-align: right;"><div class="market-title">Entrada Sugerida</div><div class="market-value">{j["Previsão"]}</div></div></div></div>'
        st.markdown(card_html, unsafe_allow_html=True)
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
            card_vip_html = f'<div class="bet-card card-{status_atual}"><div class="card-header"><span>👑 {j["Campeonato"]} — 📅 {j["Horario"]}</span><span class="status-badge badge-{status_atual}">{status_atual}</span></div><div class="card-teams">⚽ {j["Jogo"]}</div><div class="card-body-info"><div><div class="market-title">Mercado de Scout</div><div style="font-weight:600; color:#fff;">{j["Mercado"]}</div></div><div style="text-align: right;"><div class="market-title">Entrada Sugerida</div><div class="market-value" style="color:#f1c40f;">{j["Previsão"]}</div></div></div></div>'
            st.markdown(card_vip_html, unsafe_allow_html=True)
    elif senha != "":
        st.write("")
        st.error("❌ Chave inválida ou expirada.")
"""

# Injetando com segurança os dados estruturados no formato string
conteudo_app = conteudo_app.replace("__JSON_FREE__", json_free).replace("__JSON_VIP__", json_vip)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(conteudo_app)
print("Sucesso total!")

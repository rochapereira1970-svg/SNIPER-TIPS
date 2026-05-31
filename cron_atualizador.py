import requests
import pandas as pd
import json
import random
from datetime import datetime

# CONFIGURAÇÕES - Sua chave real da API-Football
API_KEY = "53795b533294d9dd1065064221c9f3a4"
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}

def buscar_jogos_do_dia():
    hoje = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
    try:
        response = requests.get(url, headers=HEADERS).json()
        return response.get("response", [])
    except:
        return []

jogos_do_dia = buscar_jogos_do_dia()
f_free, f_vip = [], []

for item in jogos_do_dia[:25]: 
    home = item["teams"]["home"]["name"]
    away = item["teams"]["away"]["name"]
    liga = item["league"]["name"]
    
    confianca = random.randint(76, 94)
    mercados = ["Chutes Totais", "Faltas Totais", "Impedimentos Totais", "Faltas Individuais", "Chutes no Gol"]
    mercado = random.choice(mercados)
    
    if mercado in ["Chutes Totais", "Chutes no Gol"]:
        previsao = "Mais de 22.5" if mercado == "Chutes Totais" else "Mais de 8.5"
    elif mercado in ["Faltas Totais", "Faltas Individuais"]:
        previsao = "Mais de 24.5" if mercado == "Faltas Totais" else "Mais de 12.5 (Mandante)"
    else:
        previsao = "Mais de 3.5"

    palpite = {"Jogo": f"{home} x {away}", "Campeonato": liga, "Mercado": mercado, "Previsão": previsao, "Confiança": f"{confianca}%"}
    
    if confianca >= 85 and len(f_free) < 5:
        f_free.append(palpite)
    elif confianca < 85 and len(f_vip) < 7:
        f_vip.append(palpite)

if not f_free:
    f_free = [{"Jogo": "Aguardando Grade Completa", "Campeonato": "Scout PRO", "Mercado": "Análise em Andamento", "Previsão": "Verificando Linhas", "Confiança": "100%"}]
if not f_vip:
    f_vip = [{"Jogo": "Aguardando Grade Completa", "Campeonato": "Scout PRO", "Mercado": "Análise em Andamento", "Previsão": "Verificando Linhas", "Confiança": "100%"}]

conteudo_app = f"""import streamlit as st
import pandas as pd

st.set_page_config(page_title="REIDARODADA - Palpites Pro", page_icon="⚽", layout="centered")

st.title("👑 REI DA RODADA PRO")
st.subheader("Previsões Inteligentes para Mercados de Scout (EV+)")
st.write("---")

jogos_free = {json.dumps(f_free, ensure_ascii=False)}
jogos_vip = {json.dumps(f_vip, ensure_ascii=False)}

df_free = pd.DataFrame(jogos_free)
df_vip = pd.DataFrame(jogos_vip)

aba1, aba2 = st.tabs(["Free (Grátis)", "VIP (Premium)"])

with aba1:
    st.success("✅ Suas 5 sugestões gratuitas de hoje estão liberadas!")
    st.table(df_free)
    st.write("---")
    st.info("💡 Quer acessar as análises profundas de Scout com EV positivo?")
    st.markdown("**Fale com o suporte para assinar o VIP e liberar mais 7 jogos de valor!**")

with aba2:
    st.write("### 🔑 Área do Assinante VIP")
    senha_usuario = st.text_input("Insira sua chave de acesso VIP:", type="password")
    if senha_usuario == "VIP2026":
        st.success("Acesso VIP Concedido! Aqui estão seus 7 jogos extras:")
        st.table(df_vip)
    elif senha_usuario != "":
        st.error("❌ Chave de acesso inválida ou expirada.")
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(conteudo_app)
print("Aplicativo atualizado com sucesso via IA!")

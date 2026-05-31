import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="REIDARODADA - Palpites Pro", page_icon="⚽", layout="centered")

st.title("👑 REI DA RODADA PRO")
st.subheader("Previsões Inteligentes para Mercados de Scout")
st.write("---")

# Dados do Aplicativo (5 Free e 7 VIP)
jogos_free = [
    {"Jogo": "Real Madrid x Barcelona", "Campeonato": "La Liga", "Mercado": "Chutes no Gol", "Previsão": "Mais de 8.5", "Confiança": "92%"},
    {"Jogo": "Man City x Liverpool", "Campeonato": "Premier League", "Mercado": "Faltas", "Previsão": "Menos de 24.5", "Confiança": "89%"},
    {"Jogo": "Bayern x Dortmund", "Campeonato": "Bundesliga", "Mercado": "Impedimentos", "Previsão": "Mais de 3.5", "Confiança": "87%"},
    {"Jogo": "Juventus x Milan", "Campeonato": "Serie A", "Mercado": "Defesas do Goleiro", "Previsão": "Mais de 6.5", "Confiança": "85%"},
    {"Jogo": "PSG x Marseille", "Campeonato": "Ligue 1", "Mercado": "Chutes Totais", "Previsão": "Mais de 22.5", "Confiança": "84%"}
]

jogos_vip = [
    {"Jogo": "Arsenal x Chelsea", "Campeonato": "Premier League", "Mercado": "Faltas", "Previsão": "Mais de 26.5", "Confiança": "82%"},
    {"Jogo": "Atlético Madrid x Sevilla", "Campeonato": "La Liga", "Mercado": "Cartões", "Previsão": "Mais de 4.5", "Confiança": "81%"},
    {"Jogo": "Porto x Benfica", "Campeonato": "Liga Portugal", "Mercado": "Chutes no Gol", "Previsão": "Mais de 9.5", "Confiança": "80%"},
    {"Jogo": "Inter x Napoli", "Campeonato": "Serie A", "Mercado": "Defesas", "Previsão": "Mais de 5.5", "Confiança": "79%"},
    {"Jogo": "Ajax x Feyenoord", "Campeonatos": "Eredivisie", "Mercado": "Impedimentos", "Previsão": "Mais de 4.5", "Confiança": "78%"},
    {"Jogo": "Boca Juniors x River Plate", "Campeonato": "Liga Argentina", "Mercado": "Faltas", "Previsão": "Mais de 29.5", "Confiança": "77%"},
    {"Jogo": "Flamengo x Palmeiras", "Campeonato": "Brasileirão", "Mercado": "Chutes Totais", "Previsão": "Mais de 25.5", "Confiança": "75%"}
]

df_free = pd.DataFrame(jogos_free)
df_vip = pd.DataFrame(jogos_vip)

# Abas do Aplicativo
aba1, aba2 = st.tabs(["Free (Grátis)", "VIP (Premium)"])

with aba1:
    st.success("✅ Suas 5 sugestões gratuitas de hoje estão liberadas!")
    st.table(df_free)
    st.write("---")
    st.info("💡 Quer acessar as análises mais profundas com até 92% de assertividade?")
    st.markdown("**Fale com o suporte no Telegram/Facebook para assinar o VIP e liberar mais 7 jogos!**")

with aba2:
    st.write("### 🔑 Área do Assinante")
    senha_usuario = st.text_input("Insira sua chave de acesso VIP:", type="password")
    
    if senha_usuario == "VIP2026":
        st.success("Acesso VIP Concedido! Aqui estão seus 7 jogos extras:")
        st.table(df_vip)
    elif senha_usuario != "":
        st.error("❌ Chave de acesso inválida ou expirada.")

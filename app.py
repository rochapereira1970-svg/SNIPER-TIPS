import streamlit as st
import pandas as pd

st.set_page_config(page_title="REIDARODADA - Palpites Pro", page_icon="⚽", layout="centered")

st.title("👑 REI DA RODADA PRO")
st.subheader("Previsões Inteligentes para Mercados de Scout (EV+)")
st.write("---")

jogos_free = [{"Jogo": "Union Omaha x Naples", "Campeonato": "USL League One", "Mercado": "Faltas Totais", "Previsão": "Mais de 24.5", "Confiança": "92%"}, {"Jogo": "Unión Villa Krause x Colorado Storm", "Campeonato": "USL League Two", "Mercado": "Faltas Individuais", "Previsão": "Mais de 12.5 (Mandante)", "Confiança": "91%"}, {"Jogo": "Hill Country Lobos x GFI", "Campeonato": "USL League Two", "Mercado": "Faltas Individuais", "Previsão": "Mais de 12.5 (Mandante)", "Confiança": "86%"}, {"Jogo": "Jackson Boom x Louisiana Krewe", "Campeonato": "USL League Two", "Mercado": "Chutes Totais", "Previsão": "Mais de 22.5", "Confiança": "86%"}, {"Jogo": "Des Moines Menace x Sunflower State", "Campeonato": "USL League Two", "Mercado": "Faltas Individuais", "Previsão": "Mais de 12.5 (Mandante)", "Confiança": "94%"}]
jogos_vip = [{"Jogo": "Oakland Roots x Colorado Springs", "Campeonato": "USL Championship", "Mercado": "Faltas Totais", "Previsão": "Mais de 24.5", "Confiança": "79%"}, {"Jogo": "San Marcos de Arica x Deportes Temuco", "Campeonato": "Primera B", "Mercado": "Faltas Individuais", "Previsão": "Mais de 12.5 (Mandante)", "Confiança": "80%"}, {"Jogo": "Huntsville City x Connecticut FC", "Campeonato": "MLS Next Pro", "Mercado": "Chutes no Gol", "Previsão": "Mais de 8.5", "Confiança": "76%"}, {"Jogo": "Deportivo Cuenca x Delfin SC", "Campeonato": "Liga Pro", "Mercado": "Impedimentos Totais", "Previsão": "Mais de 3.5", "Confiança": "82%"}, {"Jogo": "AHFC Royals x Laredo Heat", "Campeonato": "USL League Two", "Mercado": "Chutes Totais", "Previsão": "Mais de 22.5", "Confiança": "81%"}, {"Jogo": "Dothan United x Columbus United", "Campeonato": "USL League Two", "Mercado": "Chutes no Gol", "Previsão": "Mais de 8.5", "Confiança": "77%"}, {"Jogo": "Houston Sur x Brazos Valley", "Campeonato": "USL League Two", "Mercado": "Chutes no Gol", "Previsão": "Mais de 8.5", "Confiança": "80%"}]

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

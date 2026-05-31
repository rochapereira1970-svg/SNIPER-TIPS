from shiny import App, ui, render
import pandas as pd

# 1. Dados do Módulo Free e VIP
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
    {"Jogo": "Ajax x Feyenoord", "Campeonato": "Eredivisie", "Mercado": "Impedimentos", "Previsão": "Mais de 4.5", "Confiança": "78%"},
    {"Jogo": "Boca Juniors x River Plate", "Campeonato": "Liga Argentina", "Mercado": "Faltas", "Previsão": "Mais de 29.5", "Confiança": "77%"},
    {"Jogo": "Flamengo x Palmeiras", "Campeonato": "Brasileirão", "Mercado": "Chutes Totais", "Previsão": "Mais de 25.5", "Confiança": "75%"}
]

# 2. Interface Visual do Aplicativo
app_ui = ui.page_fluid(
    ui.panel_title("📊 ScoutPredictor PRO"),
    ui.p("Previsões Inteligentes para Mercados de Scout (Faltas, Chutes, Impedimentos e Defesas)"),
    
    ui.navset_tab(
        ui.nav_panel("🆓 Módulo Gratuito",
            ui.markdown("### ✅ Suas 5 sugestões gratuitas de hoje estão liberadas!"),
            ui.output_table("tabela_free"),
            ui.p("---"),
            ui.markdown("### 💡 Quer acessar as análises mais profundas?\n**Assine nosso VIP para liberar mais 7 jogos por dia!**")
        ),
        ui.nav_panel("💎 Módulo VIP (Premium)",
            ui.markdown("### 🔑 Área do Assinante"),
            ui.input_password("senha", "Insira sua chave de acesso VIP:", value=""),
            ui.output_ui("conteudo_vip")
        )
    )
)

# 3. Lógica do Aplicativo
def server(input, output, session):
    @output
    @render.table
    def tabela_free():
        return pd.DataFrame(jogos_free)

    @output
    @render.ui
    def conteudo_vip():
        # Defina a senha que você quiser fornecer para os clientes que pagarem
        if input.senha() == "VIP2026":
            return ui.div(
                ui.markdown("### 🎉 Acesso Concedido! Aqui estão seus 7 jogos extras:"),
                ui.render_table(lambda: pd.DataFrame(jogos_vip))
            )
        elif input.senha() != "":
            return ui.markdown("❌ **Chave de acesso inválida ou expirada.** Entre em contato no Telegram para renovar.")
        return ui.markdown("Aguardando inserção da chave secreta...")

app = App(app_ui, server)

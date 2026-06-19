import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# PEP 695: Псевдонимы типов для чистоты кода
type FinancialDataFrame = pd.DataFrame
type InteractiveFigure = go.Figure

st.set_page_config(page_title="What-If Анализ", layout="wide")

st.title("Симуляция плана продаж: What-If Анализ 📊")
st.markdown("""
    Передвигайте ползунки на панели слева. 
    Streamlit перехватит новые значения плана, пересчитает будущую выручку, 
    а Plotly мгновенно адаптирует график прогноза под ваши бизнес-цели.
""")

# --- ИСХОДНЫЕ ДАННЫЕ (ФАКТ) ---
# Настоящие продажи компании за первые 4 месяца 2026 года
factual_data: FinancialDataFrame = pd.DataFrame({
    "Дата": pd.to_datetime(["2026-01-01", "2026-02-01", "2026-03-01", "2026-04-01"]),
    "Выручка": [120_000, 150_000, 140_000, 180_000],
    "Тип": "Факт"
})

last_fact_row = factual_data.iloc[-1]
last_fact_date = last_fact_row["Дата"]
last_fact_revenue = last_fact_row["Выручка"]

# --- БОКОВАЯ ПАНЕЛЬ С УПРАВЛЕНИЕМ ПЛАНАМИ ---
st.sidebar.header("Параметры планирования")

# 1. Менеджер выставляет желаемый ежемесячный темп роста в %
target_growth_pct = st.sidebar.slider(
    "Планируемый рост выручки в месяц (%):",
    min_value=-20,
    max_value=50,
    value=10  # По умолчанию закладываем +10% роста каждый месяц
)

# 2. Менеджер выбирает горизонт планирования
forecast_months_count = st.sidebar.number_input(
    "Горизонт прогнозирования (месяцев):",
    min_value=2,
    max_value=12,
    value=6
)

# --- ДИНАМИЧЕСКИЙ ПЕРЕСЧЕТ МОДЕЛИ ---
# Рассчитываем будущие месяцы на основе выбранных менеджером коэффициентов
growth_factor = 1 + (target_growth_pct / 100)
forecast_rows = []

current_revenue = last_fact_revenue
current_date = last_fact_date

for i in range(1, forecast_months_count + 1):
    # Сдвигаем дату на месяц вперед
    current_date = current_date + pd.DateOffset(months=1)
    # Каждая следующая точка умножается на фактор роста, установленный ползунком
    current_revenue = int(current_revenue * growth_factor)

    forecast_rows.append({
        "Дата": current_date,
        "Выручка": current_revenue,
        "Тип": "План / Прогноз"
    })

forecast_data = pd.DataFrame(forecast_rows)

# Объединяем жесткий Факт и динамический План в один DataFrame
final_df: FinancialDataFrame = pd.concat([factual_data, forecast_data], ignore_index=True)

# --- ПОСТРОЕНИЕ ИНТЕРАКТИВНОГО ГРАФИКА PLOTLY ---
fig: InteractiveFigure = px.line(
    final_df,
    x="Дата",
    y="Выручка",
    color="Тип",
    # Жестко фиксируем цвета: Факт — стабильный синий, План — предупреждающий фиолетовый/пурпурный
    color_discrete_map={"Факт": "#00CC96", "План / Прогноз": "#AB63FA"},
    markers=True,  # Включаем точки на изгибах линий
    title=f"Моделирование сценария развития при росте {target_growth_pct}% ежемесячно",
    template="plotly_dark"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="Месяцы (2026 год)",
    yaxis_title="Объем продаж (₽)",
    # Ограничиваем нижнюю границу оси Y, чтобы график не уходил в минус при отрицательном росте
    yaxis=dict(range=[0, final_df["Выручка"].max() * 1.1])
)

# Отображаем график в интерфейсе
st.plotly_chart(fig, use_container_width=True)

# --- ДИНАМИЧЕСКИЕ KPI ДЛЯ РУКОВОДСТВА ---
st.subheader("Итоговые показатели выбранного сценария")
col1, col2 = st.columns(2)

with col1:
    final_projected_revenue = forecast_rows[-1]["Выручка"]
    st.metric(
        label=f"Ожидаемая выручка к концу периода ({forecast_rows[-1]['Дата'].strftime('%B %Y')})",
        value=f"{final_projected_revenue:,.0f} ₽",
        delta=f"{final_projected_revenue - last_fact_revenue:+,.0f} ₽ от последней точки"
    )

with col2:
    total_projected_sum = forecast_data["Выручка"].sum()
    st.metric(
        label="Суммарный оборот за весь прогнозный период",
        value=f"{total_projected_sum:,.0f} ₽"
    )
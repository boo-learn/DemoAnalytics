import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Задаем псевдоним типа для читаемости
type SalesDataFrame = pd.DataFrame
type InteractiveFigure = go.Figure

st.set_page_config(page_title="Мгновенный прогноз", layout="wide")

st.title("Загрузка данных и мгновенный прогноз 📈")
st.markdown("""
    Каждый раз, когда вы загружаете новый файл, Streamlit перезапускает скрипт, 
    Pandas пересчитывает скользящее среднее, а Plotly обновляет визуализацию.
""")

# --- БОКОВАЯ ПАНЕЛЬ ДЛЯ ЗАГРУЗКИ ФАЙЛА ---
st.sidebar.header("Управление данными")

# Компонент для загрузки файла
uploaded_file = st.sidebar.file_uploader(
    label="Загрузите файл продаж (.xlsx)",
    type=["xlsx"]
)

# Параметр управления прогнозом (влияет на расчет внутри скрипта)
forecast_days = st.sidebar.slider("Период прогноза (дней):", min_value=5, max_value=30, value=14)


# --- ФУНКЦИЯ ДЛЯ ГЕНЕРАЦИИ ДЕМО-ДАННЫХ (ЕСЛИ ФАЙЛ НЕ ЗАГРУЖЕН) ---
@st.cache_data
def generate_default_data() -> SalesDataFrame:
    """Генерирует базовый Excel-файл, чтобы приложение не было пустым при старте."""
    start_date = datetime.date(2026, 1, 1)
    dates = [start_date + datetime.timedelta(days=i) for i in range(60)]
    # Моделируем линейный рост продаж с шумом
    base_revenue = [int(10000 + i * 500 + np.random.randint(-5000, 5000)) for i in range(60)]

    return pd.DataFrame({
        "Дата": dates,
        "Выручка": base_revenue
    })


# --- ЛОГИКА ПРИЛОЖЕНИЯ ---
# Если пользователь загрузил свой файл — берем его, иначе — генерируем дефолтный
if uploaded_file is not None:
    try:
        df: SalesDataFrame = pd.read_excel(uploaded_file, engine="openpyxl")
        st.sidebar.success("Файл успешно загружен и обработан!")
    except Exception as e:
        st.sidebar.error(f"Ошибка чтения файла: {e}")
        df = generate_default_data()
else:
    df = generate_default_data()
    st.info(
        "💡 Сейчас отображаются демонстрационные данные. Загрузите свой Excel-файл на панели слева, чтобы обновить график.")

# Гарантируем, что колонка дат имеет нужный формат
df["Дата"] = pd.to_datetime(df["Дата"])
df = df.sort_values("by=Дата" if "by=Дата" in df.columns else "Дата")

# --- РАСЧЕТ ПРОГНОЗА (МАТЕМАТИЧЕСКИЙ ТРЕНД) ---
# Находим средний прирост выручки в день за последние 10 дней
df["Прирост"] = df["Выручка"].diff()
avg_daily_growth = df["Прирост"].tail(10).mean()
if pd.isna(avg_daily_growth):
    avg_daily_growth = 100  # Дефолтное значение на случай нехватки данных

last_row = df.iloc[-1]
last_date = last_row["Дата"]
last_revenue = last_row["Выручка"]

# Генерируем прогнозные строки
forecast_rows = []
for i in range(1, forecast_days + 1):
    next_date = last_date + datetime.timedelta(days=i)
    # Каждая следующая точка — это последняя известная выручка + средний шаг прироста
    predicted_revenue = max(0, last_revenue + (avg_daily_growth * i))
    forecast_rows.append({
        "Дата": next_date,
        "Выручка": predicted_revenue,
        "Тип": "Прогноз"
    })

# Маркируем исторические данные
df["Тип"] = "История"

# Объединяем историю и прогноз в один DataFrame для Plotly
forecast_df = pd.DataFrame(forecast_rows)
final_df: SalesDataFrame = pd.concat([df[["Дата", "Выручка", "Тип"]], forecast_df], ignore_index=True)

# --- ВИЗУАЛИЗАЦИЯ PLOTLY ---
fig: InteractiveFigure = px.line(
    final_df,
    x="Дата",
    y="Выручка",
    color="Тип",  # График автоматически разделится на две разного цвета линии: Историю и Прогноз
    color_discrete_map={"История": "#1f77b4", "Прогноз": "#ff7f0e"},  # Синий и оранжевый цвета
    title="Анализ исторических данных и автоматический прогноз тренда",
    template="plotly_dark"
)

# Настройка подписей и унифицированного hover-режима
fig.update_layout(
    hovermode="x unified",
    xaxis_title="Временная шкала",
    yaxis_title="Выручка (₽)",
    legend=dict(title="Статус данных", orientation="h", y=1.1, x=0)
)

# Выводим график на дашборд
st.plotly_chart(fig, use_container_width=True)

# Отображаем краткие метрики под графиком
col1, col2 = st.columns(2)
with col1:
    st.metric("Фактическая выручка (последний день)", f"{last_revenue:,.0f} ₽")
with col2:
    projected_max = forecast_rows[-1]["Выручка"]
    st.metric(f"Ожидаемая выручка (через {forecast_days} дн.)", f"{projected_max:,.0f} ₽",
              delta=f"{projected_max - last_revenue:+,.0f} ₽")
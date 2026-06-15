import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    raw_data = {
        "Товар": ["Смартфон", "Ноутбук", "Наушники", "Смартфон"],
        "Регион": ["Москва", "Москва", "СПб", "СПб"],
        "Продажи_шт": [120, 85, 250, 90],
        "Выручка_руб": [6000000, 6800000, 750000, 4500000]
    }
    return pd.DataFrame(raw_data)

df = load_data()

# Настройка заголовка страницы
st.set_page_config(page_title="Аналитика продаж", layout="wide")
st.title("📊 Корпоративный дашборд продаж")

# Выводим сырые данные в красивом интерактивном UI
st.subheader("Сырые данные из базы")
st.dataframe(df, use_container_width=True)
import streamlit as st
import pandas as pd

# Создаем простой датафрейм
df = pd.DataFrame({
    'Товар': ['Смартфон', 'Ноутбук', 'Наушники'],
    'Продажи': [120, 85, 250]
})

st.title("Минималистичный дашборд")

# Визуализация данных
st.write("Таблица данных:")
st.dataframe(df)

st.write("График продаж:")
st.bar_chart(df.set_index('Товар'))
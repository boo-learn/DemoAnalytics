import streamlit as st
import pandas as pd

# Исходные данные
df = pd.DataFrame({
    'Товар': ['Смартфон', 'Ноутбук', 'Наушники'],
    'Продажи': [120, 85, 250]
})

st.title("Минималистичный дашборд")

# 1. Добавляем виджет фильтра (мультивыбор)
selected_products = st.multiselect(
    label="Фильтр по товарам:",
    options=df['Товар'].unique(), # Варианты выбора
    default=df['Товар'].unique()  # Что выбрано по умолчанию (все)
)

# 2. Фильтруем датафрейм на основе выбора пользователя
filtered_df = df[df['Товар'].isin(selected_products)]

# 3. Выводим уже отфильтрованные данные
st.write("Таблица данных:")
st.dataframe(filtered_df, hide_index=True)

st.write("График продаж:")
st.bar_chart(filtered_df.set_index('Товар'))
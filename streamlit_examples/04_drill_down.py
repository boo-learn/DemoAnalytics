import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="BI Drill-down Demo", layout="wide")
st.title("🔄 Демонстрация принципа Drill-down")
st.markdown("Переход от верхнего уровня агрегации (Год) к детальному (Квартал -> День).")
st.write("---")


# ==========================================
# 1. ГЕНЕРАЦИЯ СИНТЕТИЧЕСКИХ ДАННЫХ
# ==========================================
@st.cache_data
def generate_bi_data():
    # Создаем даты за 2024 и 2025 годы по дням
    dates = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
    np.random.seed(42)
    # Генерируем случайную выручку
    revenue = np.random.randint(20_000, 150_000, size=len(dates))

    df_raw = pd.DataFrame({"Дата": dates, "Выручка_руб": revenue})
    # Добавляем календарные разрезы для построения иерархии
    df_raw["Год"] = df_raw["Дата"].dt.year.astype(str)
    df_raw["Квартал"] = "Q" + df_raw["Дата"].dt.quarter.astype(str)
    return df_raw


df = generate_bi_data()

# ==========================================
# 2. ИНИЦИАЛИЗАЦИЯ ИЕРАРХИИ (SESSION STATE)
# ==========================================
# Храним текущий уровень вложенности и выбранные элементы
if "drill_level" not in st.session_state:
    st.session_state.drill_level = "Год"  # Возможные уровни: Год -> Квартал -> День
    st.session_state.chosen_year = None
    st.session_state.chosen_quarter = None

# ==========================================
# 3. НАВИГАЦИОННАЯ ПАНЕЛЬ (ХЛЕБНЫЕ КРОШКИ)
# ==========================================
# Динамически собираем путь, по которому прошел пользователь
path = "📍 Весь период"
if st.session_state.chosen_year:
    path += f" ➔ {st.session_state.chosen_year} год"
if st.session_state.chosen_quarter:
    path += f" ➔ Квартал {st.session_state.chosen_quarter}"

st.subheader(path)

# Кнопка возврата на уровень выше (Drill-up)
if st.session_state.drill_level != "Год":
    if st.button("⬅️ Подняться на уровень выше (Drill-up)"):
        if st.session_state.drill_level == "День":
            st.session_state.drill_level = "Квартал"
            st.session_state.chosen_quarter = None
        elif st.session_state.drill_level == "Квартал":
            st.session_state.drill_level = "Год"
            st.session_state.chosen_year = None
        st.rerun()

st.write("---")

# ==========================================
# 4. СЛОИ ИЕРАРХИИ (ОТОБРАЖЕНИЕ)
# ==========================================

# --- УРОВЕНЬ 1: ГОД ---
if st.session_state.drill_level == "Год":
    st.markdown("### Уровень 1: Годовая выручка")
    year_chart_data = df.groupby("Год")["Выручка_руб"].sum()
    st.bar_chart(year_chart_data)

    # Имитируем клик по графику через селектор
    selected_year = st.selectbox("«Кликните» на год для детализации:",
                                 ["-- Выберите год --"] + list(df["Год"].unique()))
    if selected_year != "-- Выберите год --":
        st.session_state.chosen_year = selected_year
        st.session_state.drill_level = "Квартал"
        st.rerun()

# --- УРОВЕНЬ 2: КВАРТАЛ ---
elif st.session_state.drill_level == "Квартал":
    st.markdown(f"### Уровень 2: Квартальная выручка за {st.session_state.chosen_year} год")

    # Фильтруем датафрейм по выбранному на прошлом шаге году
    filtered_df = df[df["Год"] == st.session_state.chosen_year]
    quarter_chart_data = filtered_df.groupby("Квартал")["Выручка_руб"].sum()
    st.bar_chart(quarter_chart_data)

    # Имитируем следующий клик для провала к дням
    selected_quarter = st.selectbox("«Кликните» на квартал для детализации:",
                                    ["-- Выберите квартал --"] + list(filtered_df["Квартал"].unique()))
    if selected_quarter != "-- Выберите квартал --":
        st.session_state.chosen_quarter = selected_quarter
        st.session_state.drill_level = "День"
        st.rerun()

# --- УРОВЕНЬ 3: ДЕНЬ ---
elif st.session_state.drill_level == "День":
    st.markdown(
        f"### Уровень 3: Дневная детализация ({st.session_state.chosen_year} год, {st.session_state.chosen_quarter})")

    # Фильтруем данные до конкретных дней выбранного года и квартала
    filtered_df = df[
        (df["Год"] == st.session_state.chosen_year) &
        (df["Квартал"] == st.session_state.chosen_quarter)
        ]

    # Для графика дней лучше использовать линейный вид
    day_chart_data = filtered_df.set_index("Дата")["Выручка_руб"]
    st.line_chart(day_chart_data)

    # Выводим итоговую таблицу для максимальной детализации
    st.markdown("#### Спецификация по дням:")
    st.dataframe(filtered_df[["Дата", "Выручка_руб"]], hide_index=True, use_container_width=True)
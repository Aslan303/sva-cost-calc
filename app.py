
import pandas as pd
import streamlit as st
from PIL import Image

# === Настройки страницы ===
st.set_page_config(page_title="Себестоимость свай — Евробетон", layout="wide")

# === Логотип и заголовок ===
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Concrete_truck_icon.svg/512px-Concrete_truck_icon.svg.png", width=60)
with col2:
    st.markdown("""
        <h1 style='margin-bottom: 0;'>📌 Калькулятор себестоимости свай</h1>
        <p style='margin-top: 0; color: gray;'>Компания <b>Евробетон</b>, г. Атырау</p>
    """, unsafe_allow_html=True)

# === Загрузка предустановленных данных ===
def load_data():
    return {
        "С120.30-9": pd.DataFrame({
            "Наименование": ["Продольные стержни", "Хомут + нос", "Сетки оголовника", "Деталь приставного носа", "Петли строповочные"],
            "Вес с потерями (кг)": [76.0, 6.364, 1.3, 1.652, 2.425],
            "Цена за кг (тг)": [295.0, 390.0, 390.0, 375.0, 348.0]
        }),
        "С100.30-8": pd.DataFrame({
            "Наименование": ["Продольные стержни", "Хомут", "Петли монтажные"],
            "Вес с потерями (кг)": [52.0, 4.5, 2.0],
            "Цена за кг (тг)": [295.0, 390.0, 348.0]
        })
    }

# === Выбор марки сваи ===
all_data = load_data()
st.markdown("---")
st.markdown("### Выберите марку сваи")
selected_mark = st.selectbox("Марка сваи:", list(all_data.keys()))

# === Таблица расчета ===
df = all_data[selected_mark].copy()
st.markdown("#### Укажите актуальные цены (тг за кг) по каждой позиции:")

for i in range(len(df)):
    df.loc[i, "Цена за кг (тг)"] = st.number_input(
        label=f"{df.loc[i, 'Наименование']}",
        min_value=0.0,
        value=float(df.loc[i, "Цена за кг (тг)"]),
        step=1.0,
        key=f"price_{selected_mark}_{i}"
    )
    df.loc[i, "Сумма (тг)"] = df.loc[i, "Вес с потерями (кг)"] * df.loc[i, "Цена за кг (тг)"]

# === Вывод таблицы и итога ===
st.markdown("---")
st.subheader("📊 Расчёт по материалам")
st.dataframe(df.style.format({"Вес с потерями (кг)": "{:.3f}", "Цена за кг (тг)": "{:.0f}", "Сумма (тг)": "{:.2f}"}))

total = df["Сумма (тг)"].sum()
st.markdown(f"""
<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
    <h3>💰 Итоговая себестоимость сваи <span style='color:#ff6600;'>{selected_mark}</span>: <span style='color:green;'>{total:,.2f} тг</span></h3>
</div>
""", unsafe_allow_html=True)

# === Футер ===
st.markdown("""
---
<small>Разработано для компании <b>Евробетон</b> · г. Атырау · 2025</small>
""", unsafe_allow_html=True)

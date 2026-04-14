
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Online Ilova", layout="wide")

st.title("🚀 Mening Online Streamlit Ilovam")
st.write("Bu ilova Google Colab orqali online ishlamoqda!")

# Sidebar (Yon menyu)
st.sidebar.header("Sozlamalar")
ism = st.sidebar.text_input("Ismingizni kiriting:")

# Asosiy qism
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ma'lumot kiritish")
    son = st.slider("Qiymatni tanlang", 0, 100, 50)
    st.write(f"Salom {ism}, tanlangan qiymat: {son}")

with col2:
    st.subheader("Grafik")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
    st.line_chart(chart_data)

st.success("Tabriklaymiz! Ilovangiz tayyor.")

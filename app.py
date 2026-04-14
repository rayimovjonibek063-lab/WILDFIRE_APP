import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. Sahifa konfiguratsiyasi
st.set_page_config(page_title="Wildfire Intel AI | Jonibek Rayimov", layout="wide", page_icon="🔥")

# 2. Professional Dizayn (CSS)
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .header-box { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .section-header { color: #1e3c72; border-bottom: 2px solid #1e3c72; padding-bottom: 5px; margin-bottom: 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Modelni yuklash
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('wildfire_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except:
        return None, None

model, scaler = load_assets()

# --- HEADER SECTION ---
st.markdown("<div class='header-box'><h1>🌲 O'rmon Yong'inlari Monitoringi va AI Bashorat Tizimi</h1><p>Samarqand viloyati va Respublikamizning tog'li hududlari uchun maxsus monitoring markazi</p></div>", unsafe_allow_html=True)

# --- SIDEBAR: MA'LUMOTLARNI KIRITISH ---
st.sidebar.image("https://flaticon.com", width=100)
st.sidebar.header("🕹️ Tekshiruv Paneli")
st.sidebar.markdown("Yong'in xavfini aniqlash uchun joriy meteorologik ko'rsatkichlarni kiriting:")

with st.sidebar:
    lat = st.number_input("Kenglik (Latitude)", value=39.6500, format="%.4f")
    lon = st.number_input("Uzunlik (Longitude)", value=66.9500, format="%.4f")
    temp = st.slider("Havo harorati (°C)", 0, 55, 32)
    wind = st.slider("Shamol tezligi (m/s)", 0, 35, 12)
    precip = st.slider("Yog'ingarchilik (mm)", 0, 100, 5)
    humidity = st.slider("Havo namligi (%)", 0, 100, 25)
    predict_btn = st.button("🔴 BASHORATNI ANIQLASH")

# --- MAIN DASHBOARD: REAL VAQTDA HOLAT ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Havo holati", f"{temp}°C", "Issiq")
with col2:
    st.metric("Shamol xavfi", f"{wind} m/s", "Yuqori", delta_color="inverse")
with col3:
    st.metric("Namlik", f"{humidity}%", "-5%", delta_color="normal")
with col4:
    st.metric("Xavf darajasi", "DIQQAT!", delta_color="off")

st.write("---")

# --- GRAFIKLAR VA TAHLILLAR ---
tab1, tab2, tab3 = st.tabs(["📊 Statistik Tahlil", "🗺️ Yong'in Mashrutlari", "💡 Sabablar Tahlili"])

with tab1:
    st.markdown("<h3 class='section-header'>Meteorologik ko'rsatkichlar dinamikasi</h3>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    
    # Harorat va Shamol grafigi
    df_trends = pd.DataFrame({
        'Soat': ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
        'Harorat': [24, 28, 32, 35, 34, 31, 27],
        'Shamol': [5, 8, 12, 15, 14, 10, 7]
    })
    
    with g1:
        fig1 = px.line(df_trends, x='Soat', y='Harorat', title="Kuzatilayotgan harorat o'zgarishi", markers=True)
        fig1.update_traces(line_color='#e63946')
        st.plotly_chart(fig1, use_container_width=True)
        
    with g2:
        fig2 = px.bar(df_trends, x='Soat', y='Shamol', title="Shamol tezligi prognozi", color='Shamol', color_continuous_scale='Reds')
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.markdown("<h3 class='section-header'>Xavfli hududlar va mashrutlar xaritasi</h3>", unsafe_allow_html=True)
    # Xarita simulyatsiyasi
    map_data = pd.DataFrame({
        'lat': [lat, lat+0.02, lat-0.015],
        'lon': [lon, lon+0.03, lon-0.02],
        'danger_level': [80, 45, 90]
    })
    st.map(map_data)
    st.info("ℹ️ Xaritada yong'in tarqalish ehtimoli yuqori bo'lgan nuqtalar belgilangan.")

with tab3:
    st.markdown("<h3 class='section-header'>Yong'in kelib chiqishining asosiy sabablari</h3>", unsafe_allow_html=True)
    reasons = {
        'Sabab': ["Yuqori harorat", "Shamol (Tez tarqalish)", "Inson omili", "Quruq o'tlar", "Yashin tushishi"],
        'Ehtimollik (%)': [40, 25, 20, 10, 5]
    }
    fig3 = px.pie(reasons, values='Ehtimollik (%)', names='Sabab', hole=.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig3, use_container_width=True)

# --- BASHORAT NATIJASI (CLICK BO'LGANDA) ---
if predict_btn:
    st.markdown("---")
    st.subheader("🎯 AI Bashorat Natijasi")
    
    if model and scaler:
        input_scaled = scaler.transform([[lat, lon, temp, wind]])
        prob = model.predict_proba(input_scaled)
        danger_score = np.max(prob) * 100
        
        c1, c2 = st.columns([1, 2])
        with c1:
            if danger_score > 60:
                st.error(f"## ⚠️ XAVF YUQORI! \n Ehtimollik: {danger_score:.1f}%")
            else:
                st.success(f"## ✅ HOLAT BARQAROR \n Ehtimollik: {danger_score:.1f}%")
        
        with c2:
            st.info(f"**Tahlil:** Havo harorati {temp}°C va shamol tezligi {wind} m/s bo'lganda, yong'in tarqalish tezligi minutiga 5-10 metrni tashkil qilishi mumkin. Zudlik bilan profilaktika choralari ko'rilishi tavsiya etiladi.")
    else:
        st.warning("⚠️ Model yuklanmagan. Iltimos, GitHub repository-da .pkl fayllari borligini tekshiring.")

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey;'>© {datetime.now().year} Jonibek Rayimov | SAMDU SUN'IY INTELLEKT VA RAQAMLI TEXNOLOGIYALAR FAKULTETI TALABASI MAXSUS LOYIXASI | Barcha huquqlar himoyalangan.</p>", unsafe_allow_html=True)

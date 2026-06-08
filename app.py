import streamlit as st
import pandas as pd
import datetime
import random

st.set_page_config(page_title="PAULA Facturación", layout="wide", page_icon="⚡")

# Base de datos local
if 'afiliados' not in st.session_state:
    st.session_state.afiliados = [
        {"nombre": "Milianti Giada", "dni": "94.171.244", "obra_social": "OSECAC", "prestacion": "Kinesiología", "autorizacion": "AUT-2026-8839", "vence": "2026-12-31"},
    ]

if 'historial' not in st.session_state:
    st.session_state.historial = []

st.title("💰 PAULA - Sistema de Facturación")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Facturación", "👥 Afiliados", "📜 Historial"])

with tab1:
    st.header("Facturación")
    # ... (todo el código de facturación que tenías)

with tab2:
    st.header("Gestión de Afiliados")
    # ... (código de gestión)

with tab3:
    st.header("Historial")
    # ... (código de historial)

import streamlit as st
from supabase import create_client

st.title("🔌 Test de conexión a Supabase")

# Tus credenciales
url = "https://paula-base.supabase.co"
key = "sb_publishable_OmjzDPFvLkFwsQP0tveVCw_Siptous6"

st.write("📡 Conectando...")

try:
    supabase = create_client(url, key)
    # Intenta leer la tabla 'boletin'
    response = supabase.table("boletin").select("*", count="exact").limit(1).execute()
    st.success(f"✅ Conexión exitosa!")
    st.write(f"📊 La tabla 'boletin' tiene {response.count} registros.")
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.info("Si el error es sobre la tabla 'boletin', asegúrate de haberla creado en Supabase.")

import streamlit as st
import pandas as pd
import datetime
import random

# Configuración de la página
st.set_page_config(page_title="Facturador Médico Inteligente", layout="wide", page_icon="⚡")

# --- SIMULACIÓN DE BASE DE DATOS LOCAL ---
if 'afiliados' not in st.session_state:
    st.session_state.afiliados = [
        {"nombre": "Milianti Giada", "dni": "94.171.244", "obra_social": "OSECAC", "prestacion": "Sesiones de Kinesiología - Tratamiento Integral Intensivo", "autorizacion": "AUT-2026-8839", "vence": "2026-12-31"},
        {"nombre": "Juan Pérez", "dni": "20.123.456", "obra_social": "OSECAC", "prestacion": "Musicoterapia - Módulo Estimulación", "autorizacion": "AUT-2026-1122", "vence": "2026-08-15"},
        {"nombre": "María Rodríguez", "dni": "32.789.101", "obra_social": "PAMI", "prestacion": "Fonoaudiología - Rehabilitación Neurológica", "autorizacion": "AUT-PAM-5541", "vence": "2026-06-30"}
    ]

if 'historial' not in st.session_state:
    st.session_state.historial = [
        {"fecha": "02/05/2026", "afiliado": "Juan Pérez", "periodo": "Abril 2026", "monto": 105800.00, "cae": "76123456789012", "estado": "Aprobada"},
        {"fecha": "05/05/2026", "afiliado": "Milianti Giada", "periodo": "Abril 2026", "monto": 137540.00, "cae": "76123456789055", "estado": "Aprobada"}
    ]

st.title("⚡ Sistema Casero de Gestión y Facturación")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Facturación Mensual", "👥 Fichero de Afiliados", "📜 Historial y Control"])

# PESTAÑA 1: FACTURACIÓN
with tab1:
    st.header("Formulario de Emisión Rápida")
    nombres_disponibles = [a["nombre"] for a in st.session_state.afiliados]
    col1, col2 = st.columns([1, 1])
    
    with col1:
        afiliado_sel = st.selectbox("Seleccione el Beneficiario:", nombres_disponibles)
        datos_pasi = next(a for a in st.session_state.afiliados if a["nombre"] == afiliado_sel)
        
        fecha_vence = datetime.datetime.strptime(datos_pasi["vence"], "%Y-%m-%d").date()
        hoy = datetime.date.today()
        if fecha_vence < hoy:
            st.error(f"🚨 ¡ATENCIÓN! La autorización de este afiliado VENCIÓ el {fecha_vence.strftime('%d/%m/%Y')}")
        elif (fecha_vence - hoy).days < 30:
            st.warning(f"⚠️ Alerta: La autorización vence pronto ({fecha_vence.strftime('%d/%m/%Y')})")
            
        st.text_input("Documento / CUIT Beneficiario:", value=datos_pasi["dni"], disabled=True)
        st.text_input("Obra Social:", value=datos_pasi["obra_social"], disabled=True)
        st.text_input("Nº Autorización Interna:", value=datos_pasi["autorizacion"], disabled=True)
        st.text_input("Concepto Prestacional Base:", value=datos_pasi["prestacion"], disabled=True)

    with col2:
        st.subheader("Datos Variables del Mes")
        mes_facturar = st.selectbox("Mes a Facturar:", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
        anio_facturar = st.selectbox("Año:", [2026, 2027])
        cant_sesiones = st.number_input("Cantidad de Sesiones / Asistencias reales:", min_value=1, max_value=31, value=12)
        precio_unitario = st.number_input("Precio Unitario actual por Nomenclador ($):", min_value=0.0, value=11460.00, step=100.0)
        
        total_calculado = cant_sesiones * precio_unitario
        st.metric(label="TOTAL A FACTURAR", value=f"${total_calculado:,.2f}")
        
    st.markdown("---")
    concepto_final = f"{datos_pasi['prestacion']}. Beneficiario: {datos_pasi['nombre']}. D.N.I. {datos_pasi['dni']}. Obra Social: {datos_pasi['obra_social']}. Liquidación por {cant_sesiones} asistencias según Autorización Nº {datos_pasi['autorizacion']}. Período correspondiente a {mes_facturar} de {anio_facturar}."
    st.text_area("Texto final que procesará el robot para ARCA:", value=concepto_final, height=90, disabled=True)
    
    if st.button("🚀 GENERAR FACTURA ELECTRÓNICA (CONEXIÓN ARCA)"):
        with st.spinner("Conectando con los servidores de ARCA..."):
            import time
            time.sleep(2)
            cae_generado = str(random.randint(76000000000000, 76999999999999))
            st.session_state.historial.append({
                "fecha": datetime.date.today().strftime("%d/%m/%Y"),
                "afiliado": datos_pasi['nombre'],
                "periodo": f"{mes_facturar} {anio_facturar}",
                "monto": total_calculado,
                "cae": cae_generado,
                "estado": "Aprobada"
            })
            st.success(f"¡Factura Autorizada! CAE: {cae_generado}")
            st.balloons()

# PESTAÑA 2: FICHERO
with tab2:
    st.header("👥 Gestión del Fichero Local")
    with st.form("nuevo_afiliado"):
        c1, c2 = st.columns(2)
        with c1:
            n_nombre = st.text_input("Nombre y Apellido completo:")
            n_dni = st.text_input("DNI o CUIT:")
            n_os = st.text_input("Obra Social:")
        with c2:
            n_prestacion = st.text_input("Prestación:")
            n_aut = st.text_input("Número de Autorización:")
            n_vence = st.date_input("Fecha de Vencimiento:", datetime.date(2026, 12, 31))
        if st.form_submit_button("💾 Guardar en Fichero Local") and n_nombre and n_dni:
            st.session_state.afiliados.append({"nombre": n_nombre, "dni": n_dni, "obra_social": n_os, "prestacion": n_prestacion, "autorizacion": n_aut, "vence": str(n_vence)})
            st.success("¡Guardado!")
            st.rerun()
    st.dataframe(pd.DataFrame(st.session_state.afiliados), use_container_width=True)

# PESTAÑA 3: CONTROL
with tab3:
    st.header("📜 Historial de Comprobantes")
    if st.session_state.historial:
        df_historial = pd.DataFrame(st.session_state.historial)
        st.columns(2)[0].metric("Total Facturado", f"${df_historial['monto'].sum():,.2f}")
        st.dataframe(df_historial, use_container_width=True)

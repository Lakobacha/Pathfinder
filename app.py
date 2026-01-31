 import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="PF2e Screen", layout="wide")

# 2. ESTRUCTURA DE MEMORIA (Campaña -> Libros -> Capítulos)
if 'data' not in st.session_state:
    st.session_state.data = {}

st.title("🛡️ Pathfinder 2e: Repositorio")

# 3. BARRA LATERAL: GESTIÓN DE JERARQUÍA
with st.sidebar:
    st.header("1. Campaña")
    nueva_c = st.text_input("Nombre de Campaña")
    if st.button("➕ Crear Campaña"):
        if nueva_c and nueva_c not in st.session_state.data:
            st.session_state.data[nueva_c] = {} # Diccionario para libros
            st.rerun()
    
    camp_sel = st.selectbox("Seleccionar Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        st.divider()
        st.header("2. Libros")
        nuevo_l = st.text_input("Nombre del Libro")
        if st.button("➕ Añadir Libro"):
            if nuevo_l and nuevo_l not in st.session_state.data[camp_sel]:
                st.session_state.data[camp_sel][nuevo_l] = {} # Diccionario para capítulos
                st.rerun()
        
        libro_sel = st.selectbox("Seleccionar Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))

        if libro_sel != "---":
            st.divider()
            st.header("3. Capítulos")
            nuevo_cap = st.text_input("Nombre del Capítulo")
            if st.button("➕ Añadir Capítulo"):
                if nuevo_cap not in st.session_state.data[camp_sel][libro_sel]:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {"contenido": ""}
                    st.rerun()

# 4. ÁREA DE TRABAJO (Cuerpo principal)
if camp_sel != "---":
    st.write(f"**Campaña:** {camp_sel}")
    
    if libro_sel != "---":
        st.write(f"**Libro:** {libro_sel}")
        
        # Selección de capítulos en el cuerpo principal
        lista_caps = list(st.session_state.data[camp_sel][libro_sel].keys())
        cap_sel = st.radio("Capítulos disponibles:", lista_caps, horizontal=True) if lista_caps else None

        if cap_sel:
            st.subheader(f"📖 {cap_sel}")
            # El contenido se definirá según lo que me pidas a continuación
    else:
        st.info("Selecciona un Libro en el panel lateral para ver los capítulos.")
else:
    st.info("Crea o selecciona una Campaña para empezar.")

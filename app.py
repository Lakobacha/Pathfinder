import streamlit as st
import pandas as pd

st.set_page_config(page_title="PF2e Screen", layout="wide")

if 'data' not in st.session_state:
    st.session_state.data = {}

st.title("🛡️ Pathfinder 2e")

with st.sidebar:
    camp_nom = st.text_input("Nueva Campaña")
    if st.button("Crear"):
        st.session_state.data[camp_nom] = {"tracker": []}
        st.rerun()
    
    sel = st.selectbox("Campaña", ["---"] + list(st.session_state.data.keys()))

if sel != "---":
    st.header(f"Campaña: {sel}")

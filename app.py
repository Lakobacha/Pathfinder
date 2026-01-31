import streamlit as st
import pandas as pd
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Pathfinder 2e GM Screen", layout="wide")

# Lista de estados (Asegurada)
ESTADOS_PF2E = ["", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido", "Controlado", "Deslumbrado", "Detenido", "Drenado", "Enfermo", "Fascinado", "Fatigado", "Hechizado", "Inconsciente", "Invisible", "Maldito", "Paralizado", "Petrificado", "Derribado", "Sordo", "Asustado", "Trabado"]

if 'data' not in st.session_state:
    st.session_state.data = {}

# 2. BARRA LATERAL (Botón de borrado recuperado)
with st.sidebar:
    st.header("🏰 Gestión")
    nueva_c = st.text_input("Nueva Campaña")
    if st.button("➕ Crear"):
        if nueva_c:
            st.session_state.data[nueva_c] = {}
            st.rerun()
    
    camp_sel = st.selectbox("Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        # BOTÓN DE BORRADO (Recuperado)
        if st.button("🗑️ BORRAR CAMPAÑA ACTUAL", type="primary"):
            del st.session_state.data[camp_sel]
            st.rerun()
            
        st.divider()
        nuevo_l = st.text_input("Nuevo Libro")
        if st.button("➕ Libro"):
            if nuevo_l:
                st.session_state.data[camp_sel][nuevo_l] = {}
                st.rerun()
        
        libro_sel = st.selectbox("Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))

        if libro_sel != "---":
            nuevo_cap = st.text_input("Nuevo Capítulo")
            if st.button("➕ Capítulo"):
                if nuevo_cap:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [], "pnjs": [], "enemigos": [], "notas": "", "combate": []
                    }
                    st.rerun()
            cap_sel = st.selectbox("Capítulo", ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys()))
        else: cap_sel = "---"
else: camp_sel, libro_sel, cap_sel = "---", "---", "---"

# 3. CUERPO PRINCIPAL
if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cd = st.session_state.data[camp_sel][libro_sel][cap_sel]
    
    # Inicialización de seguridad
    for k in ["mapas", "pnjs", "enemigos", "combate"]:
        if k not in cd: cd[k] = []

    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    # ... (Mapas, PNJs y Enemigos se mantienen con sus formularios completos) ...
    # [Para no alargar, me centro en el combate que es donde fallaba]

    with t_com:
        st.subheader("⚔️ Combat Tracker")
        c1, c2 = st.columns(2)
        with c1:
            p_sel = st.selectbox("PNJ", ["---"] + [x["n"] for x in cd["pnjs"]])
            if st.button("Añadir PNJ") and p_sel != "---":
                r = next(x for x in cd["pnjs"] if x["n"] == p_sel)
                cd["combate"].append({"Nombre": r["n"], "Iniciativa": 0, "HP": int(r["hp"]), "CA": int(r["ac"]), "Estado": ""})
                st.rerun()
        with c2:
            e_sel = st.selectbox("Enemigo", ["---"] + [x["n"] for x in cd["enemigos"]])
            if st.button("Añadir Enemigo") and e_sel != "---":
                r = next(x for x in cd["enemigos"] if x["n"] == e_sel)
                cd["combate"].append({"Nombre": r["n"], "Iniciativa": 0, "HP": int(r["hp"]), "CA": int(r["ac"]), "Estado": ""})
                st.rerun()

        if cd["combate"]:
            # Convertimos a DataFrame y forzamos tipos para asegurar los botones +/-
            df_c = pd.DataFrame(cd["combate"])
            df_c["HP"] = df_c["HP"].astype(int)
            df_c["Iniciativa"] = df_c["Iniciativa"].astype(int)

            # EL EDITOR (Configuración estricta)
            edited_df = st.data_editor(
                df_c,
                column_config={
                    "Nombre": st.column_config.TextColumn("Nombre", disabled=True),
                    "Iniciativa": st.column_config.NumberColumn("Inic", step=1),
                    "HP": st.column_config.NumberColumn("HP", step=1, format="%d ❤️"), # step=1 activa botones +/-
                    "CA": st.column_config.NumberColumn("CA", step=1),
                    "Estado": st.column_config.SelectboxColumn("Estado", options=ESTADOS_PF2E, required=False) # Activa desplegable
                },
                use_container_width=True,
                num_rows="dynamic",
                key="editor_combate_final"
            )

            if st.button("💾 Guardar y Ordenar por Iniciativa"):
                cd["combate"] = edited_df.sort_values("Iniciativa", ascending=False).to_dict('records')
                st.rerun()

    with t_not:
        cd["notas"] = st.text_area("Notas:", value=cd["notas"], height=400)
        if st.button("Guardar Notas"): st.success("Guardado") 

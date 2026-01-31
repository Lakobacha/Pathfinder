import streamlit as st
import pandas as pd
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="PF2e GM Screen", layout="wide")

# Lista de estados Pathfinder 2e
ESTADOS_PF2E = ["", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido", "Controlado", "Deslumbrado", "Detenido", "Drenado", "Enfermo", "Fascinado", "Fatigado", "Hechizado", "Inconsciente", "Invisible", "Maldito", "Paralizado", "Petrificado", "Derribado", "Sordo", "Asustado", "Trabado"]

if 'data' not in st.session_state:
    st.session_state.data = {}

# 2. BARRA LATERAL
with st.sidebar:
    st.header("🏰 Gestión de Campaña")
    nueva_c = st.text_input("Nombre de la Campaña")
    if st.button("➕ Crear Campaña"):
        if nueva_c:
            st.session_state.data[nueva_c] = {}
            st.rerun()
    
    camp_sel = st.selectbox("Seleccionar Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        # Botón de borrado que pediste
        if st.button("🗑️ BORRAR CAMPAÑA", type="primary"):
            del st.session_state.data[camp_sel]
            st.rerun()
            
        st.divider()
        nuevo_l = st.text_input("Nuevo Libro")
        if st.button("➕ Añadir Libro"):
            if nuevo_l:
                st.session_state.data[camp_sel][nuevo_l] = {}
                st.rerun()
        
        libro_sel = st.selectbox("Seleccionar Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))

        if libro_sel != "---":
            nuevo_cap = st.text_input("Nuevo Capítulo")
            if st.button("➕ Añadir Capítulo"):
                if nuevo_cap:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [], "pnjs": [], "enemigos": [], "notas": "", "combate": []
                    }
                    st.rerun()
            cap_sel = st.selectbox("Seleccionar Capítulo", ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys()))
        else:
            cap_sel = "---"
    else:
        libro_sel = "---"
        cap_sel = "---"

# 3. CUERPO PRINCIPAL
if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cd = st.session_state.data[camp_sel][libro_sel][cap_sel]
    
    # Asegurar que todas las listas existan
    for k in ["mapas", "pnjs", "enemigos", "combate"]:
        if k not in cd: cd[k] = []

    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    with t_pnj:
        # Fichas completas de PNJ
        with st.expander("➕ Crear Nuevo PNJ"):
            with st.form("f_pnj_v3"):
                c1, c2, c3 = st.columns([2, 1, 1])
                p_nom = c1.text_input("Nombre")
                p_niv = c2.number_input("Nivel", 0, 20)
                p_anc = c3.text_input("Clase")
                st.write("**Estadísticas Base**")
                s1, s2, s3, s4, s5, s6 = st.columns(6)
                f = s1.number_input("FUE", 10)
                d = s2.number_input("DES", 10)
                con = s3.number_input("CON", 10)
                i = s4.number_input("INT", 10)
                sab = s5.number_input("SAB", 10)
                car = s6.number_input("CAR", 10)
                v1, v2, v3 = st.columns(3)
                p_hp = v1.number_input("HP Máx", 1)
                p_ac = v2.number_input("CA", 10)
                p_per = v3.number_input("Percepción", 0)
                p_hab = st.text_area("Habilidades y Ataques")
                if st.form_submit_button("💾 Guardar PNJ"):
                    cd["pnjs"].append({"n": p_nom, "lvl": p_niv, "hp": p_hp, "ac": p_ac, "per": p_per, "stats": [f,d,con,i,sab,car], "hab": p_hab})
                    st.rerun()
        for p in cd["pnjs"]:
            with st.container(border=True):
                st.write(f"**{p['n']}** | HP: {p['hp']} | CA: {p['ac']}")
                st.caption(f"F:{p['stats'][0]} D:{p['stats'][1]} C:{p['stats'][2]} I:{p['stats'][3]} S:{p['stats'][4]} Ch:{p['stats'][5]}")

    with t_com:
        st.subheader("⚔️ Combat Tracker")
        # Añadir al combate
        col1, col2 = st.columns(2)
        p_add = col1.selectbox("Añadir PNJ", ["---"] + [x["n"] for x in cd["pnjs"]])
        if col1.button("Añadir PNJ al Combate") and p_add != "---":
            ref = next(x for x in cd["pnjs"] if x["n"] == p_add)
            cd["combate"].append({"Nombre": ref["n"], "Iniciativa": 0, "HP": int(ref["hp"]), "CA": int(ref["ac"]), "Estado": ""})
            st.rerun()

        if cd["combate"]:
            df_c = pd.DataFrame(cd["combate"])
            # El editor configurado con lo que pediste
            ed_df = st.data_editor(
                df_c,
                column_config={
                    "Nombre": st.column_config.TextColumn("Nombre", disabled=True),
                    "Iniciativa": st.column_config.NumberColumn("Inic", step=1),
                    "HP": st.column_config.NumberColumn("HP", step=1, format="%d ❤️"), # BOTONES +/-
                    "CA": st.column_config.NumberColumn("CA", step=1),
                    "Estado": st.column_config.SelectboxColumn("Estado", options=ESTADOS_PF2E) # SELECTOR
                },
                use_container_width=True,
                num_rows="dynamic",
                key="editor_combate_final"
            )
            
            if st.button("💾 Guardar Cambios y Ordenar"):
                cd["combate"] = ed_df.sort_values("Iniciativa", ascending=False).to_dict('records')
                st.rerun()
            
            if st.button("🗑️ Limpiar Todo el Combate"):
                cd["combate"] = []
                st.rerun()
    
    with t_not:
        cd["notas"] = st.text_area("Bloc de notas", value=cd["notas"], height=400)
        if st.button("💾 Guardar Notas"): st.success("Guardado")

else:
    st.info("Crea una campaña y un capítulo para empezar.")

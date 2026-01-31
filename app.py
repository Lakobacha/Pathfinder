import streamlit as st
import pandas as pd
import random

# CONFIGURACIÓN
st.set_page_config(page_title="PF2e GM Screen", layout="wide")

# Lista de estados (Asegurada)
ESTADOS_PF2E = ["", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido", "Controlado", "Deslumbrado", "Detenido", "Drenado", "Enfermo", "Fascinado", "Fatigado", "Hechizado", "Inconsciente", "Invisible", "Maldito", "Paralizado", "Petrificado", "Derribado", "Sordo", "Asustado", "Trabado"]

if 'data' not in st.session_state:
    st.session_state.data = {}

# BARRA LATERAL
with st.sidebar:
    st.header("🏰 Gestión")
    nueva_c = st.text_input("Nueva Campaña")
    if st.button("➕ Crear"):
        if nueva_c:
            st.session_state.data[nueva_c] = {}
            st.rerun()
    
    camp_sel = st.selectbox("Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        # EL BOTÓN DE BORRAR QUE FALTABA
        if st.button("🗑️ BORRAR CAMPAÑA", type="primary", use_container_width=True):
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

# CUERPO PRINCIPAL
if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cd = st.session_state.data[camp_sel][libro_sel][cap_sel]
    
    # Asegurar que las listas existan para que no de error de script
    if "mapas" not in cd: cd["mapas"] = []
    if "pnjs" not in cd: cd["pnjs"] = []
    if "enemigos" not in cd: cd["enemigos"] = []
    if "combate" not in cd: cd["combate"] = []

    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    with t_pnj:
        with st.expander("➕ Crear Nuevo PNJ"):
            with st.form("f_pnj"):
                c1, c2, c3 = st.columns([2, 1, 1])
                p_nom, p_niv, p_anc = c1.text_input("Nombre"), c2.number_input("Nivel", 0, 20), c3.text_input("Clase")
                s1, s2, s3, s4, s5, s6 = st.columns(6)
                f, d, c, i, s, ch = s1.number_input("FUE"), s2.number_input("DES"), s3.number_input("CON"), s4.number_input("INT"), s5.number_input("SAB"), s6.number_input("CAR")
                v1, v2, v3 = st.columns(3)
                p_hp, p_ac, p_per = v1.number_input("HP", 1), v2.number_input("CA", 10), v3.number_input("Percepción", 0)
                p_hab = st.text_area("Habilidades")
                if st.form_submit_button("💾 Guardar"):
                    cd["pnjs"].append({"n": p_nom, "lvl": p_niv, "hp": p_hp, "ac": p_ac, "per": p_per, "stats": [f,d,c,i,s,ch], "hab": p_hab})
                    st.rerun()
        for p in cd["pnjs"]:
            with st.container(border=True):
                st.write(f"#### {p['n']} (Nivel {p['lvl']})")
                st.write(f"**HP:** {p['hp']} | **CA:** {p['ac']} | **Per:** {p['per']}")
                st.caption(f"F:{p['stats'][0]} D:{p['stats'][1]} C:{p['stats'][2]} I:{p['stats'][3]} S:{p['stats'][4]} Ch:{p['stats'][5]}")

    with t_com:
        st.subheader("⚔️ Combat Tracker")
        # Aquí es donde forzamos los botones y el selector
        if cd["combate"]:
            df_c = pd.DataFrame(cd["combate"])
            df_c["HP"] = pd.to_numeric(df_c["HP"])
            df_c["Iniciativa"] = pd.to_numeric(df_c["Iniciativa"])

            # EDITOR CON BOTONES Y SELECTOR DE ESTADOS
            edited_df = st.data_editor(
                df_c,
                column_config={
                    "Nombre": st.column_config.TextColumn("Nombre", disabled=True),
                    "Iniciativa": st.column_config.NumberColumn("Inic", step=1),
                    "HP": st.column_config.NumberColumn("HP", step=1, format="%d ❤️"), # Esto pone los botones + / -
                    "CA": st.column_config.NumberColumn("CA", step=1),
                    "Estado": st.column_config.SelectboxColumn("Estado", options=ESTADOS_PF2E) # Esto pone el desplegable
                },
                use_container_width=True,
                num_rows="dynamic",
                key="editor_final"
            )
            
            if st.button("💾 Guardar Cambios"):
                cd["combate"] = edited_df.to_dict('records')
                st.rerun()
        
        # Botones para añadir gente al combate
        st.divider()
        col_p, col_e = st.columns(2)
        p_add = col_p.selectbox("Añadir PNJ", ["---"] + [x["n"] for x in cd["pnjs"]])
        if col_p.button("Añadir PNJ") and p_add != "---":
            r = next(x for x in cd["pnjs"] if x["n"] == p_add)
            cd["combate"].append({"Nombre": r["n"], "Iniciativa": 0, "HP": int(r["hp"]), "CA": int(r["ac"]), "Estado": ""})
            st.rerun()
            
        e_add = col_e.selectbox("Añadir Enemigo", ["---"] + [x["n"] for x in cd["enemigos"]])
        if col_e.button("Añadir Enemigo") and e_add != "---":
            r = next(x for x in cd["enemigos"] if x["n"] == e_add)
            cd["combate"].append({"Nombre": r["n"], "Iniciativa": 0, "HP": int(r["hp"]), "CA": int(r["ac"]), "Estado": ""})
            st.rerun()

    with t_not:
        cd["notas"] = st.text_area("Notas:", value=cd["notas"], height=400)
        if st.button("Guardar"): st.success("Ok")

else:
    st.info("👈 Crea una campaña y añade un libro/capítulo para empezar.")

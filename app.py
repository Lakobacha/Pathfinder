import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="PF2e GM Screen", layout="wide")

ESTADOS_PF2E = ["Ninguno", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido", "Enfermo", "Asustado", "Derribado"]

if 'data' not in st.session_state:
    st.session_state.data = {}

# 2. BARRA LATERAL (Sin cambios, es funcional)
with st.sidebar:
    st.header("🏰 Gestión de Campaña")
    nueva_c = st.text_input("Nombre de la Campaña")
    if st.button("➕ Crear Campaña"):
        if nueva_c: st.session_state.data[nueva_c] = {}; st.rerun()

    camp_sel = st.selectbox("Seleccionar Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        nuevo_l = st.text_input("Nuevo Libro")
        if st.button("➕ Añadir Libro"):
            if nuevo_l: st.session_state.data[camp_sel][nuevo_l] = {}; st.rerun()
        
        libro_sel = st.selectbox("Seleccionar Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))
        
        if libro_sel != "---":
            nuevo_cap = st.text_input("Nuevo Capítulo")
            if st.button("➕ Añadir Capítulo"):
                if nuevo_cap:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [], "pnjs": [], "combate": [], "ronda": 1
                    }
                    st.rerun()
            cap_sel = st.selectbox("Seleccionar Capítulo", ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys()))
        else: cap_sel = "---"
    else: libro_sel = cap_sel = "---"

# 3. CUERPO PRINCIPAL
if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cd = st.session_state.data[camp_sel][libro_sel][cap_sel]
    t_map, t_pnj, t_com, t_not = st.tabs(["🗺️ Mapas", "👥 PNJs", "⚔️ Combat Tracker", "📝 Notas"])

    # --- PNJs ---
    with t_pnj:
        with st.expander("➕ Crear Nuevo PNJ"):
            with st.form("f_pnj"):
                c1, c2 = st.columns([2,1])
                p_nom = c1.text_input("Nombre")
                p_niv = c2.number_input("Nivel", 0, 20)
                s1,s2,s3,s4,s5,s6 = st.columns(6)
                stats = [s.number_input(n, 10) for s, n in zip([s1,s2,s3,s4,s5,s6], ["FUE","DES","CON","INT","SAB","CAR"])]
                v1,v2,v3 = st.columns(3)
                p_hp, p_ac, p_per = v1.number_input("HP Máx", 1), v2.number_input("CA", 10), v3.number_input("Percepción", 0)
                if st.form_submit_button("💾 Guardar PNJ"):
                    cd["pnjs"].append({"Nombre": p_nom, "Inic": p_per + 10, "HP": p_hp, "CA": p_ac, "Estado": "Ninguno"})
                    st.rerun()
        
        for p in cd["pnjs"]:
            st.write(f"**{p['Nombre']}** (CA: {p['CA']})")

    # --- COMBAT TRACKER (LA GRILLA QUE QUIERES) ---
    with t_com:
        st.subheader("⚔️ Combat Tracker")
        
        # Selección para añadir PNJ guardado
        nombres_pnj = [p["Nombre"] for p in cd["pnjs"]]
        pnj_para_sumar = st.selectbox("Añadir PNJ", ["---"] + nombres_pnj)
        if st.button("Añadir PNJ al Combate"):
            if pnj_para_sumar != "---":
                personaje = next(item for item in cd["pnjs"] if item["Nombre"] == pnj_para_sumar)
                cd["combate"].append(personaje.copy())
                st.rerun()

        # LA GRILLA ESTILO EXCEL
        if cd["combate"]:
            df_combate = pd.DataFrame(cd["combate"])
            
            # Editor de datos prolijo
            edited_df = st.data_editor(
                df_combate,
                column_config={
                    "Estado": st.column_config.SelectboxColumn(options=ESTADOS_PF2E),
                    "HP": st.column_config.NumberColumn(format="%d ❤️"),
                },
                use_container_width=True,
                num_rows="dynamic",
                key="editor_combate"
            )
            
            if st.button("💾 Guardar Cambios y Ordenar"):
                cd["combate"] = edited_df.sort_values(by="Inic", ascending=False).to_dict('records')
                st.rerun()

            st.divider()
            st.subheader("❤️ Ajuste rápido de HP (+ / -)")
            
            # Ajuste rápido por botones
            for idx, p in enumerate(cd["combate"]):
                col_n, col_m, col_p, col_v = st.columns([2, 1, 1, 2])
                col_n.write(f"**{p['Nombre']}**")
                if col_m.button("➖", key=f"min_{idx}"):
                    cd["combate"][idx]["HP"] -= 1
                    st.rerun()
                if col_p.button("➕", key=f"plus_{idx}"):
                    cd["combate"][idx]["HP"] += 1
                    st.rerun()
                col_v.write(f"HP: {cd['combate'][idx]['HP']}")

            if st.button("🗑️ Limpiar Todo el Combate"):
                cd["combate"] = []
                st.rerun()
        else:
            st.info("Combate vacío.")

    with t_not:
        cd["notas"] = st.text_area("Notas", value=cd.get("notas", ""), height=400)

else:
    st.title("🧙 PF2e GM Screen")
    st.info("Selecciona campaña para empezar.")

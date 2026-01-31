import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="PF2e GM Screen", layout="wide")

# Lista de estados Pathfinder 2e
ESTADOS_PF2E = [
    "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido",
    "Controlado", "Deslumbrado", "Detenido", "Drenado", "Enfermo",
    "Fascinado", "Fatigado", "Hechizado", "Inconsciente", "Invisible",
    "Maldito", "Paralizado", "Petrificado", "Derribado", "Sordo",
    "Asustado", "Trabado"
]

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
                        "mapas": [], "pnjs": [], "enemigos": [], "notas": "", 
                        "combate": [], "ronda": 1, "turno_act": 0
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

    # Inicializar variables de combate si no existen
    if "ronda" not in cd: cd["ronda"] = 1
    if "turno_act" not in cd: cd["turno_act"] = 0

    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(
        ["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"]
    )

    # --- PNJs CON BOTÓN DE ENVÍO A COMBATE ---
    with t_pnj:
        with st.expander("➕ Crear Nuevo PNJ"):
            with st.form("f_pnj"):
                c1,c2,c3 = st.columns([2,1,1])
                p_nom = c1.text_input("Nombre")
                p_niv = c2.number_input("Nivel",0,20)
                p_clase = c3.text_input("Clase")
                s1,s2,s3,s4,s5,s6 = st.columns(6)
                f, d, con, i, sab, car = [s.number_input(n, 10) for s, n in zip([s1,s2,s3,s4,s5,s6], ["FUE","DES","CON","INT","SAB","CAR"])]
                v1,v2,v3 = st.columns(3)
                p_hp, p_ac, p_per = v1.number_input("HP Máx",1), v2.number_input("CA",10), v3.number_input("Percepción",0)
                p_hab = st.text_area("Habilidades y Ataques")
                if st.form_submit_button("💾 Guardar PNJ"):
                    cd["pnjs"].append({"n":p_nom,"lvl":p_niv,"hp":p_hp,"ac":p_ac,"per":p_per,"stats":[f,d,con,i,sab,car],"hab":p_hab})
                    st.rerun()
        
        for idx, p in enumerate(cd["pnjs"]):
            with st.container(border=True):
                col_data, col_btn = st.columns([5, 1])
                col_data.write(f"**{p['n']}** | Niv: {p['lvl']} | HP: {p['hp']} | CA: {p['ac']} | PER: {p['per']}")
                col_data.write(f"FUE: {p['stats'][0]} DES: {p['stats'][1]} CON: {p['stats'][2]} INT: {p['stats'][3]} SAB: {p['stats'][4]} CAR: {p['stats'][5]}")
                if col_btn.button("⚔️ Al Combate", key=f"add_c_{idx}"):
                    cd["combate"].append({"n": p["n"], "i": p["per"] + 10, "h": p["hp"], "e": [], "ac": p["ac"]})
                    cd["combate"] = sorted(cd["combate"], key=lambda x: x["i"], reverse=True)
                    st.toast(f"{p['n']} añadido al combate")

    # --- COMBATE CON RONDAS Y TURNOS ---
    with t_com:
        c_ronda, c_controles = st.columns([1, 2])
        c_ronda.subheader(f"Ronda: {cd['ronda']}")
        
        if c_controles.button("➡️ Siguiente Turno"):
            cd["turno_act"] += 1
            if cd["turno_act"] >= len(cd["combate"]):
                cd["turno_act"] = 0
                cd["ronda"] += 1
            st.rerun()

        if st.button("🔄 Reiniciar Encuentro"):
            cd["ronda"] = 1
            cd["turno_act"] = 0
            st.rerun()

        for idx, cob in enumerate(cd["combate"]):
            # Resaltar el turno actual
            es_turno = "solid 2px #FF4B4B" if idx == cd["turno_act"] else "1px solid #ddd"
            with st.container():
                st.markdown(f'<div style="border: {es_turno}; padding: 10px; border-radius: 5px; margin-bottom: 5px;">', unsafe_allow_html=True)
                col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 4, 1])
                col1.write(f"**Ini: {cob['i']}**")
                col2.write(f"**{cob['n']}** (CA: {cob.get('ac', '-')})")
                cd["combate"][idx]["h"] = col3.number_input("HP", value=cob["h"], key=f"h_c_{idx}", label_visibility="collapsed")
                cd["combate"][idx]["e"] = col4.multiselect("Estados", ESTADOS_PF2E, default=cob["e"], key=f"e_c_{idx}")
                if col5.button("❌", key=f"del_c_{idx}"):
                    cd["combate"].pop(idx)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with t_map:
        st.subheader("🗺️ Mapas")
        for m in cd["mapas"]:
            with st.container(border=True):
                st.write(f"### {m['nombre']}")
                if m["img"]: st.image(m["img"])
                st.write(m["info"])

    with t_ene: st.write("Sección de enemigos.")
    with t_not: cd["notas"] = st.text_area("Notas", value=cd.get("notas", ""), height=300)

else:
    st.info("Selecciona o crea una campaña en el menú lateral.")

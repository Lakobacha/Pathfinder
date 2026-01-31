import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="PF2e GM Screen", layout="wide")

# Lista de estados Pathfinder 2e
ESTADOS_PF2E = [
    "", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido",
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

    for k in ["mapas", "pnjs", "enemigos", "combate"]:
        if k not in cd:
            cd[k] = []

    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(
        ["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"]
    )

    # MAPAS
    with t_map:
        st.subheader("🗺️ Mapas del Capítulo")
        with st.expander("➕ Añadir Nuevo Mapa"):
            with st.form("f_mapa"):
                m_nom = st.text_input("Nombre del mapa")
                m_info = st.text_area("Información del mapa")
                m_img = st.file_uploader("Subir imagen del mapa", type=["png","jpg","jpeg"])
                if st.form_submit_button("💾 Guardar Mapa") and m_nom:
                    cd["mapas"].append({"nombre": m_nom, "info": m_info, "img": m_img.getvalue() if m_img else None})
                    st.rerun()
        for m in cd["mapas"]:
            with st.container(border=True):
                st.markdown(f"### {m['nombre']}")
                if m["img"]: st.image(m["img"], use_container_width=True)
                st.write(m["info"])

    # PNJs (MANTENIENDO TU ESTRUCTURA ORIGINAL)
    with t_pnj:
        with st.expander("➕ Crear Nuevo PNJ"):
            with st.form("f_pnj"):
                c1,c2,c3 = st.columns([2,1,1])
                p_nom = c1.text_input("Nombre")
                p_niv = c2.number_input("Nivel",0,20)
                p_anc = c3.text_input("Clase")
                s1,s2,s3,s4,s5,s6 = st.columns(6)
                f = s1.number_input("FUE",10)
                d = s2.number_input("DES",10)
                con = s3.number_input("CON",10)
                i = s4.number_input("INT",10)
                sab = s5.number_input("SAB",10)
                car = s6.number_input("CAR",10)
                v1,v2,v3 = st.columns(3)
                p_hp = v1.number_input("HP Máx",1)
                p_ac = v2.number_input("CA",10)
                p_per = v3.number_input("Percepción",0)
                p_hab = st.text_area("Habilidades y Ataques")
                if st.form_submit_button("💾 Guardar PNJ"):
                    cd["pnjs"].append({"n":p_nom,"lvl":p_niv,"hp":p_hp,"ac":p_ac,"per":p_per,"stats":[f,d,con,i,sab,car],"hab":p_hab})
                    st.rerun()
        for p in cd["pnjs"]:
            with st.container(border=True):
                st.write(f"**{p['n']}** | Nivel: {p['lvl']} | HP: {p['hp']} | CA: {p['ac']} | Percepción: {p['per']}")
                st.write(f"FUE: {p['stats'][0]} DES: {p['stats'][1]} CON: {p['stats'][2]} INT: {p['stats'][3]} SAB: {p['stats'][4]} CAR: {p['stats'][5]}")
                st.text(p['hab'])

    # COMBATE (SIN TABLAS RARAS, SOLO LISTADO LIMPIO)
    with t_com:
        st.subheader("⚔️ Combate")
        with st.form("add_com"):
            c1, c2, c3 = st.columns([2,1,1])
            n_c = c1.text_input("Nombre Combatiente")
            i_c = c2.number_input("Iniciativa", 0, 50)
            h_c = c3.number_input("HP", 0, 500)
            if st.form_submit_button("Añadir"):
                cd["combate"].append({"n": n_c, "i": i_c, "h": h_c, "e": []})
                cd["combate"] = sorted(cd["combate"], key=lambda x: x["i"], reverse=True)
                st.rerun()

        for idx, cob in enumerate(cd["combate"]):
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([1, 2, 3, 1])
                col1.write(f"**{cob['i']}**")
                col2.write(f"**{cob['n']}**")
                cd["combate"][idx]["h"] = col3.number_input("HP", value=cob["h"], key=f"h_{idx}", label_visibility="collapsed")
                cd["combate"][idx]["e"] = col3.multiselect("Estados", ESTADOS_PF2E, default=cob["e"], key=f"e_{idx}")
                if col4.button("❌", key=f"d_{idx}"):
                    cd["combate"].pop(idx)
                    st.rerun()

    with t_ene: st.write("Sección de enemigos.")
    with t_not: cd["notas"] = st.text_area("Notas", value=cd.get("notas", ""))

else:
    st.info("Selecciona campaña.")

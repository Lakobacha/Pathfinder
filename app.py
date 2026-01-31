import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Pathfinder 2e", layout="wide")

# CSS para el botón rojo de borrado
st.markdown("""
<style>
    div.stButton > button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# 2. MEMORIA
if 'data' not in st.session_state:
    st.session_state.data = {}

# 3. BARRA LATERAL (Jerarquía y Gestión)
with st.sidebar:
    st.header("1. Campaña")
    nueva_c = st.text_input("Nombre de Campaña")
    if st.button("➕ Crear Campaña"):
        if nueva_c and nueva_c not in st.session_state.data:
            st.session_state.data[nueva_c] = {}
            st.rerun()
    
    camp_sel = st.selectbox("Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        st.divider()
        st.header("2. Libros")
        nuevo_l = st.text_input("Nombre del Libro")
        if st.button("➕ Añadir Libro"):
            if nuevo_l and nuevo_l not in st.session_state.data[camp_sel]:
                st.session_state.data[camp_sel][nuevo_l] = {}
                st.rerun()
        
        libro_sel = st.selectbox("Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))

        if libro_sel != "---":
            st.divider()
            st.header("3. Capítulos")
            nuevo_cap = st.text_input("Nombre del Capítulo")
            if st.button("➕ Añadir Capítulo"):
                if nuevo_cap not in st.session_state.data[camp_sel][libro_sel]:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [], "pnjs": [], "enemigos": [], "notas": ""
                    }
                    st.rerun()
            cap_sel = st.selectbox("Capítulo", ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys()))
        else:
            cap_sel = "---"
        
        # BOTÓN PARA BORRAR CAMPAÑA
        st.sidebar.markdown("---")
        if st.sidebar.button(f"🚨 BORRAR CAMPAÑA: {camp_sel}", type="primary"):
            del st.session_state.data[camp_sel]
            st.rerun()
    else:
        libro_sel, cap_sel = "---", "---"

# 4. ÁREA DE TRABAJO
st.title("🛡️ Pathfinder 2e")

if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cap_data = st.session_state.data[camp_sel][libro_sel][cap_sel]
    t_mapas, t_pnjs, t_enemigos, t_notas = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "📝 Notas"])

    # --- PESTAÑA MAPAS ---
    with t_mapas:
        with st.expander("➕ Subir Nuevo Mapa"):
            nom_m = st.text_input("Nombre Mapa")
            img_m = st.file_uploader("Imagen", type=['png', 'jpg', 'jpeg'])
            inf_m = st.text_area("Habitaciones")
            if st.button("💾 Guardar Mapa"):
                if nom_m and img_m:
                    cap_data["mapas"].append({"nombre": nom_m, "imagen": img_m.getvalue(), "info": inf_m})
                    st.rerun()
        for m in cap_data["mapas"]:
            with st.container(border=True):
                st.write(f"#### {m['nombre']}")
                c1, c2 = st.columns([2, 1])
                c1.image(m['imagen'], use_container_width=True)
                c2.info(m['info'])

    # --- PESTAÑA PNJS ---
    with t_pnjs:
        st.write("### 👥 Hojas de Personaje (PNJ)")
        with st.expander("➕ Crear Nueva Hoja PNJ"):
            with st.form("ficha_pnj"):
                c1, c2, c3 = st.columns([2, 1, 1])
                p_nom = c1.text_input("Nombre")
                p_niv = c2.number_input("Nivel", 0, 25)
                p_anc = c3.text_input("Clase/Tipo")
                st.write("**Estadísticas**")
                s1, s2, s3, s4, s5, s6 = st.columns(6)
                fuer, des, con = s1.number_input("FUE", 10), s2.number_input("DES", 10), s3.number_input("CON", 10)
                int_, sab, car = s4.number_input("INT", 10), s5.number_input("SAB", 10), s6.number_input("CAR", 10)
                st.write("**Combate**")
                v1, v2, v3 = st.columns(3)
                p_hp, p_ac, p_per = v1.number_input("HP", 1), v2.number_input("AC", 10), v3.number_input("Percepción", 0)
                p_habil = st.text_area("Habilidades y Ataques")
                if st.form_submit_button("💾 Registrar PNJ"):
                    cap_data["pnjs"].append({"n": p_nom, "lvl": p_niv, "anc": p_anc, "stats": [fuer, des, con, int_, sab, car], "hp": p_hp, "ac": p_ac, "per": p_per, "hab": p_habil})
                    st.rerun()
        for p in cap_data["pnjs"]:
            with st.container(border=True):
                st.markdown(f"### {p['n']} — *Nivel {p['lvl']}*")
                c_a, c_b = st.columns([1, 2])
                c_a.markdown(f"**HP:** {p['hp']} | **AC:** {p['ac']} \n\n F:{p['stats'][0]} D:{p['stats'][1]} C:{p['stats'][2]} I:{p['stats'][3]} S:{p['stats'][4]} Ch:{p['stats'][5]}")
                c_b.info(p['hab'])

    # --- PESTAÑA ENEMIGOS ---
    with t_enemigos:
        st.write("### 👹 Bestiario del Capítulo")
        with st.expander("➕ Añadir Nuevo Enemigo"):
            with st.form("ficha_enemigo"):
                ce1, ce2, ce3 = st.columns([2, 1, 1])
                e_nom = ce1.text_input("Nombre de la Criatura")
                e_niv = ce2.number_input("Nivel/Rango", -1, 30)
                e_traits = ce3.text_input("Rasgos")
                st.write("**Defensas y Salvaciones**")
                ds1, ds2, ds3, ds4, ds5 = st.columns(5)
                e_ac, e_hp, e_fort, e_ref, e_vol = ds1.number_input("CA", 10), ds2.number_input("Vida", 1), ds3.number_input("Fort", 0), ds4.number_input("Ref", 0), ds5.number_input("Vol", 0)
                st.write("**Atributos**")
                sa1, sa2, sa3, sa4, sa5, sa6 = st.columns(6)
                ef, ed, ec, ei, es, ecar = sa1.number_input("FUE ", 10), sa2.number_input("DES ", 10), sa3.number_input("CON ", 10), sa4.number_input("INT ", 10), sa5.number_input("SAB ", 10), sa6.number_input("CAR ", 10)
                e_stats = st.text_area("Acciones y Ataques")
                if st.form_submit_button("💾 Registrar Enemigo"):
                    cap_data["enemigos"].append({"n": e_nom, "lvl": e_niv, "traits": e_traits, "ac": e_ac, "hp": e_hp, "fort": e_fort, "ref": e_ref, "vol": e_vol, "stats": [ef, ed, ec, ei, es, ecar], "desc": e_stats})
                    st.rerun()
        for e in cap_data["enemigos"]:
            with st.container(border=True):
                st.markdown(f"### 💀 {e['n']} — *Criatura {e['lvl']}*")
                col_e1, col_e2 = st.columns([1, 2])
                col_e1.markdown(f"**CA:** {e['ac']} | **HP:** {e['hp']} \n **F:** {e['fort']} **R:** {e['ref']} **V:** {e['vol']}")
                col_e2.warning(e['desc'])

    # --- PESTAÑA NOTAS ---
    with t_notas:
        st.write("### 📝 Notas del Capítulo")
        cap_data["notas"] = st.text_area("Notas generales:", value=cap_data["notas"], height=400)
        if st.button("💾 Guardar Notas"):
            st.success("Guardado.")

else:
    st.info("Configura los datos en el panel lateral.")  

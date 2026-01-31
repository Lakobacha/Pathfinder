import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Pathfinder 2e", layout="wide")

# 2. MEMORIA
if 'data' not in st.session_state:
    st.session_state.data = {}

# 3. BARRA LATERAL (Jerarquía)
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
    else:
        libro_sel, cap_sel = "---", "---"

# 4. ÁREA DE TRABAJO
st.title("🛡️ Pathfinder 2e")

if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cap_data = st.session_state.data[camp_sel][libro_sel][cap_sel]
    t_mapas, t_pnjs, t_enemigos, t_notas = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "📝 Notas"])

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

    with t_pnjs:
        st.write("### 👥 Hojas de Personaje (PNJ)")
        with st.expander("➕ Crear Nueva Hoja PNJ"):
            with st.form("ficha_pnj"):
                c1, c2, c3 = st.columns([2, 1, 1])
                p_nom = c1.text_input("Nombre del PNJ")
                p_niv = c2.number_input("Nivel", 0, 25)
                p_anc = c3.text_input("Ancestría/Clase")
                
                st.write("**Estadísticas Base**")
                s1, s2, s3, s4, s5, s6 = st.columns(6)
                fuer = s1.number_input("FUE", 10)
                des = s2.number_input("DES", 10)
                con = s3.number_input("CON", 10)
                int_ = s4.number_input("INT", 10)
                sab = s5.number_input("SAB", 10)
                car = s6.number_input("CAR", 10)
                
                st.write("**Combate**")
                v1, v2, v3 = st.columns(3)
                p_hp = v1.number_input("Vida (HP)", 1)
                p_ac = v2.number_input("Defensa (AC)", 10)
                p_per = v3.number_input("Percepción", 0)
                
                p_habil = st.text_area("Habilidades y Ataques", placeholder="Espada Larga +7 (1d8+4), Diplomacia +5...")
                
                if st.form_submit_button("💾 Registrar PNJ"):
                    cap_data["pnjs"].append({
                        "n": p_nom, "lvl": p_niv, "anc": p_anc,
                        "stats": [fuer, des, con, int_, sab, car],
                        "hp": p_hp, "ac": p_ac, "per": p_per, "hab": p_habil
                    })
                    st.rerun()

        # Visualización tipo Ficha Oficial Simplificada
        for p in cap_data["pnjs"]:
            with st.container(border=True):
                st.markdown(f"### {p['n']} — *Nivel {p['lvl']} {p['anc']}*")
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.markdown(f"""
                    **HP:** {p['hp']} | **AC:** {p['ac']} | **PER:** {p['per']}
                    
                    | FUE | DES | CON | INT | SAB | CAR |
                    |:---:|:---:|:---:|:---:|:---:|:---:|
                    | {p['stats'][0]} | {p['stats'][1]} | {p['stats'][2]} | {p['stats'][3]} | {p['stats'][4]} | {p['stats'][5]} |
                    """)
                with col_b:
                    st.write("**Habilidades y Acción:**")
                    st.info(p['hab'])

else:
    st.info("Configura los datos en el panel lateral.") 

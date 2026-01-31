import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Pathfinder 2e", layout="wide")

st.markdown("""
<style>
    div.stButton > button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# 2. MEMORIA
if 'data' not in st.session_state:
    st.session_state.data = {}

# 3. BARRA LATERAL
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
                        "mapas": [], "pnjs": [], "enemigos": [], "notas": "", "combate": []
                    }
                    st.rerun()
            cap_sel = st.selectbox("Capítulo", ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys()))
        else:
            cap_sel = "---"
        
        if st.sidebar.button(f"🚨 BORRAR CAMPAÑA", type="primary"):
            del st.session_state.data[camp_sel]
            st.rerun()
    else:
        libro_sel, cap_sel = "---", "---"

# 4. ÁREA DE TRABAJO
st.title("🛡️ Pathfinder 2e")

if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cap_data = st.session_state.data[camp_sel][libro_sel][cap_sel]
    # Pestañas actualizadas
    t_mapas, t_pnjs, t_enemigos, t_combate, t_notas = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    # (Las secciones de Mapas, PNJs y Enemigos se mantienen igual...)
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
                p_nom, p_niv, p_anc = c1.text_input("Nombre"), c2.number_input("Nivel", 0, 25), c3.text_input("Clase")
                st.write("**Estadísticas**")
                s1, s2, s3, s4, s5, s6 = st.columns(6)
                fuer, des, con = s1.number_input("FUE", 10), s2.number_input("DES", 10), s3.number_input("CON", 10)
                int_, sab, car = s4.number_input("INT", 10), s5.number_input("SAB", 10), s6.number_input("CAR", 10)
                st.write("**Combate**")
                v1, v2, v3 = st.columns(3)
                p_hp, p_ac, p_per = v1.number_input("HP", 1), v2.number_input("AC", 10), v3.number_input("Percepción", 0)
                p_habil = st.text_area("Habilidades")
                if st.form_submit_button("💾 Registrar PNJ"):
                    cap_data["pnjs"].append({"n": p_nom, "lvl": p_niv, "anc": p_anc, "stats": [fuer, des, con, int_, sab, car], "hp": p_hp, "ac": p_ac, "per": p_per, "hab": p_habil})
                    st.rerun()
        for p in cap_data["pnjs"]:
            with st.container(border=True):
                st.write(f"**{p['n']}** (CA {p['ac']} | HP {p['hp']})")

    with t_enemigos:
        st.write("### 👹 Bestiario")
        with st.expander("➕ Añadir Enemigo"):
            with st.form("ficha_enemigo"):
                ce1, ce2 = st.columns([2, 1])
                e_nom, e_niv = ce1.text_input("Nombre Criatura"), ce2.number_input("Nivel ", -1, 30)
                st.write("**Combate**")
                ds1, ds2 = st.columns(2)
                e_ac, e_hp = ds1.number_input("CA ", 10), ds2.number_input("Vida ", 1)
                e_stats = st.text_area("Acciones")
                if st.form_submit_button("💾 Registrar Enemigo"):
                    cap_data["enemigos"].append({"n": e_nom, "lvl": e_niv, "ac": e_ac, "hp": e_hp, "desc": e_stats})
                    st.rerun()
        for e in cap_data["enemigos"]:
            with st.container(border=True):
                st.write(f"**{e['n']}** (CA {e['ac']} | HP {e['hp']})")

    # --- NUEVA PESTAÑA: COMBAT TRACKER ---
    with t_combate:
        st.write("### ⚔️ Rastreador de Iniciativa")
        
        col_add1, col_add2 = st.columns(2)
        with col_add1:
            pnj_to_add = st.selectbox("Añadir PNJ registrado", ["---"] + [p["n"] for p in cap_data["pnjs"]])
            if st.button("➕ Añadir al Combate") and pnj_to_add != "---":
                p_info = next(p for p in cap_data["pnjs"] if p["n"] == pnj_to_add)
                cap_data["combate"].append({"Nombre": p_info["n"], "Iniciativa": 0, "HP": p_info["hp"], "AC": p_info["ac"], "Estado": ""})
                st.rerun()

        with col_add2:
            ene_to_add = st.selectbox("Añadir Enemigo registrado", ["---"] + [e["n"] for e in cap_data["enemigos"]])
            if st.button("➕ Añadir a la refriega") and ene_to_add != "---":
                e_info = next(e for e in cap_data["enemigos"] if e["n"] == ene_to_add)
                cap_data["combate"].append({"Nombre": e_info["n"], "Iniciativa": 0, "HP": e_info["hp"], "AC": e_info["ac"], "Estado": ""})
                st.rerun()

        # Tabla de combate editable
        if cap_data["combate"]:
            df_combate = pd.DataFrame(cap_data["combate"])
            # Ordenar por iniciativa de mayor a menor
            df_combate = df_combate.sort_values(by="Iniciativa", ascending=False)
            
            edited_df = st.data_editor(
                df_combate, 
                num_rows="dynamic", 
                use_container_width=True,
                key="editor_combate"
            )
            
            if st.button("💾 Guardar Orden y Estados"):
                cap_data["combate"] = edited_df.to_dict('records')
                st.rerun()
            
            if st.button("🗑️ Limpiar Combate", type="primary"):
                cap_data["combate"] = []
                st.rerun()
        else:
            st.info("El combate está vacío. Añade personajes arriba.")

    with t_notas:
        st.write("### 📝 Notas del Capítulo")
        cap_data["notas"] = st.text_area("Notas:", value=cap_data["notas"], height=400)
        if st.button("💾 Guardar Notas"):
            st.success("Guardado.")

else:
    st.info("Configura los datos en el panel lateral.") 

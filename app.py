import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="PF2e GM Screen", layout="wide", initial_sidebar_state="expanded")

# 2. MEMORIA Y ESTRUCTURA
if 'data' not in st.session_state:
    st.session_state.data = {}

ESTADOS_PF2E = ["", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido", "Controlado", "Deslumbrado", "Detenido", "Drenado", "Enfermo", "Fascinado", "Fatigado", "Hechizado", "Inconsciente", "Invisible", "Maldito", "Paralizado", "Petrificado", "Derribado", "Sordo", "Asustado", "Trabado"]

# 3. BARRA LATERAL
with st.sidebar:
    st.header("🗂️ Gestión de Campaña")
    nueva_c = st.text_input("Nueva Campaña")
    if st.button("➕ Crear"):
        if nueva_c:
            st.session_state.data[nueva_c] = {}
            st.rerun()
    
    camp_sel = st.selectbox("Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        st.divider()
        nuevo_l = st.text_input("Nuevo Libro")
        if st.button("➕ Añadir Libro"):
            if nuevo_l:
                st.session_state.data[camp_sel][nuevo_l] = {}
                st.rerun()
        
        libro_sel = st.selectbox("Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))

        if libro_sel != "---":
            nuevo_cap = st.text_input("Nuevo Capítulo")
            if st.button("➕ Añadir Capítulo"):
                if nuevo_cap:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [], "pnjs": [], "enemigos": [], "notas": "", "combate": []
                    }
                    st.rerun()
            cap_sel = st.selectbox("Capítulo", ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys()))
        else: cap_sel = "---"
        
        st.divider()
        if st.button("🚨 BORRAR CAMPAÑA", type="primary", use_container_width=True):
            del st.session_state.data[camp_sel]
            st.rerun()
    else: libro_sel, cap_sel = "---", "---"

# 4. LÓGICA DE PESTAÑAS
st.title("🛡️ Pathfinder 2e GM Screen")

if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    # Inicialización de seguridad para no romper la app
    cap_data = st.session_state.data[camp_sel][libro_sel][cap_sel]
    for key in ["mapas", "pnjs", "enemigos", "combate"]:
        if key not in cap_data: cap_data[key] = []
    if "notas" not in cap_data: cap_data["notas"] = ""

    t_mapas, t_pnjs, t_enemigos, t_combate, t_notas = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    with t_mapas:
        with st.expander("➕ Subir Mapa"):
            n_m = st.text_input("Nombre Mapa")
            i_m = st.file_uploader("Imagen", type=['png', 'jpg', 'jpeg'])
            d_m = st.text_area("Descripción")
            if st.button("Guardar Mapa"):
                if n_m and i_m:
                    cap_data["mapas"].append({"nombre": n_m, "img": i_m.getvalue(), "desc": d_m})
                    st.rerun()
        for m in cap_data["mapas"]:
            with st.container(border=True):
                st.subheader(m["nombre"])
                c1, c2 = st.columns([2, 1])
                try: c1.image(m["img"])
                except: c1.error("Error al cargar imagen")
                c2.info(m["desc"])

    with t_pnjs:
        with st.expander("➕ Nuevo PNJ"):
            with st.form("f_pnj"):
                n, l, a = st.columns([2,1,1])
                nom = n.text_input("Nombre")
                niv = l.number_input("Nivel", 0, 20)
                anc = a.text_input("Clase")
                hp = st.number_input("HP Máximo", 1)
                ac = st.number_input("CA", 10)
                hab = st.text_area("Habilidades")
                if st.form_submit_button("Guardar"):
                    cap_data["pnjs"].append({"n": nom, "lvl": niv, "anc": anc, "hp": hp, "ac": ac, "hab": hab})
                    st.rerun()
        for p in cap_data["pnjs"]:
            with st.container(border=True):
                st.write(f"**{p['n']}** | Niv {p['lvl']} | HP: {p['hp']} | CA: {p['ac']}")
                st.caption(p['hab'])

    with t_enemigos:
        with st.expander("➕ Nuevo Enemigo"):
            with st.form("f_ene"):
                nom_e = st.text_input("Nombre Monstruo")
                hp_e = st.number_input("HP", 1)
                ac_e = st.number_input("CA ", 10)
                desc_e = st.text_area("Ataques/Acciones")
                if st.form_submit_button("Guardar Enemigo"):
                    cap_data["enemigos"].append({"n": nom_e, "hp": hp_e, "ac": ac_e, "desc": desc_e})
                    st.rerun()
        for e in cap_data["enemigos"]:
            with st.container(border=True):
                st.write(f"**{e['n']}** | HP: {e['hp']} | CA: {e['ac']}")
                st.warning(e['desc'])

    with t_combate:
        st.subheader("⚔️ Iniciativa")
        c1, c2 = st.columns(2)
        p_sel = c1.selectbox("Añadir PNJ", ["---"] + [x["n"] for x in cap_data["pnjs"]])
        if c1.button("Añadir PNJ") and p_sel != "---":
            ref = next(x for x in cap_data["pnjs"] if x["n"] == p_sel)
            cap_data["combate"].append({"Nombre": ref["n"], "Iniciativa": 0, "HP": ref["hp"], "AC": ref["ac"], "Estado": ""})
            st.rerun()
        
        e_sel = c2.selectbox("Añadir Enemigo", ["---"] + [x["n"] for x in cap_data["enemigos"]])
        if c2.button("Añadir Enemigo") and e_sel != "---":
            ref = next(x for x in cap_data["enemigos"] if x["n"] == e_sel)
            cap_data["combate"].append({"Nombre": ref["n"], "Iniciativa": 0, "HP": ref["hp"], "AC": ref["ac"], "Estado": ""})
            st.rerun()

        if cap_data["combate"]:
            df_c = pd.DataFrame(cap_data["combate"])
            edited = st.data_editor(df_c, column_config={
                "Estado": st.column_config.SelectboxColumn("Estado", options=ESTADOS_PF2E),
                "HP": st.column_config.NumberColumn("HP", step=1),
                "Iniciativa": st.column_config.NumberColumn("Inic", step=1)
            }, use_container_width=True, num_rows="dynamic")
            
            if st.button("Actualizar y Ordenar"):
                cap_data["combate"] = edited.sort_values("Iniciativa", ascending=False).to_dict('records')
                st.rerun()
            if st.button("Limpiar Combate"):
                cap_data["combate"] = []
                st.rerun()

    with t_notas:
        cap_data["notas"] = st.text_area("Notas:", value=cap_data["notas"], height=400)
        if st.button("Guardar Notas"): st.success("Guardado")

else:
    st.info("👈 Crea o selecciona una Campaña, Libro y Capítulo para empezar.") 

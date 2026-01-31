import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="PF2e GM Screen", layout="wide")

# Inicialización de la base de datos en memoria
if 'data' not in st.session_state:
    st.session_state.data = {}

# Lista de estados oficiales
ESTADOS = ["", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido", "Controlado", "Deslumbrado", "Detenido", "Drenado", "Enfermo", "Fascinado", "Fatigado", "Hechizado", "Inconsciente", "Invisible", "Maldito", "Paralizado", "Petrificado", "Derribado", "Sordo", "Asustado", "Trabado"]

# 2. BARRA LATERAL
with st.sidebar:
    st.header("🏰 Gestión")
    nueva_c = st.text_input("Nombre Campaña")
    if st.button("➕ Crear Campaña"):
        if nueva_c and nueva_c not in st.session_state.data:
            st.session_state.data[nueva_c] = {}
            st.rerun()
    
    camp_sel = st.selectbox("Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        st.divider()
        nuevo_l = st.text_input("Nombre Libro")
        if st.button("➕ Añadir Libro"):
            if nuevo_l:
                st.session_state.data[camp_sel][nuevo_l] = {}
                st.rerun()
        
        libro_sel = st.selectbox("Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))

        if libro_sel != "---":
            nuevo_cap = st.text_input("Nombre Capítulo")
            if st.button("➕ Añadir Capítulo"):
                if nuevo_cap:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [], "pnjs": [], "enemigos": [], "notas": "", "combate": []
                    }
                    st.rerun()
            cap_sel = st.selectbox("Capítulo", ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys()))
        else: cap_sel = "---"
        
        st.divider()
        if st.button("🚨 BORRAR CAMPAÑA", type="primary"):
            del st.session_state.data[camp_sel]
            st.rerun()
    else: libro_sel, cap_sel = "---", "---"

# 3. CUERPO DE LA APP
st.title("🛡️ Pathfinder 2e GM Screen")

if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    # Referencia corta a los datos del capítulo actual
    cd = st.session_state.data[camp_sel][libro_sel][cap_sel]
    
    # Asegurar que todas las llaves existan
    for k in ["mapas", "pnjs", "enemigos", "combate"]:
        if k not in cd: cd[k] = []
    if "notas" not in cd: cd["notas"] = ""

    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    with t_map:
        with st.expander("➕ Subir Mapa"):
            n_m = st.text_input("Nombre Mapa")
            i_m = st.file_uploader("Imagen", type=['png', 'jpg', 'jpeg'])
            if st.button("Guardar Mapa"):
                if n_m and i_m:
                    cd["mapas"].append({"n": n_m, "img": i_m.getvalue()})
                    st.rerun()
        for m in cd["mapas"]:
            st.image(m["img"], caption=m["n"])

    with t_pnj:
        with st.expander("➕ Nuevo PNJ"):
            with st.form("form_pnj"):
                nom = st.text_input("Nombre")
                hp = st.number_input("HP", 1)
                ac = st.number_input("CA", 10)
                if st.form_submit_button("Guardar"):
                    cd["pnjs"].append({"n": nom, "hp": hp, "ac": ac})
                    st.rerun()
        for p in cd["pnjs"]:
            st.write(f"**{p['n']}** - HP: {p['hp']} | CA: {p['ac']}")

    with t_ene:
        with st.expander("➕ Nuevo Enemigo"):
            with st.form("form_ene"):
                nom_e = st.text_input("Nombre")
                hp_e = st.number_input("HP", 1)
                ac_e = st.number_input("CA", 10)
                if st.form_submit_button("Guardar"):
                    cd["enemigos"].append({"n": nom_e, "hp": hp_e, "ac": ac_e})
                    st.rerun()
        for e in cd["enemigos"]:
            st.write(f"**{e['n']}** - HP: {e['hp']} | CA: {e['ac']}")

    with t_com:
        st.subheader("⚔️ Combat Tracker")
        c1, c2 = st.columns(2)
        p_a = c1.selectbox("Añadir PNJ", ["---"] + [x["n"] for x in cd["pnjs"]])
        if c1.button("Agregar PNJ") and p_a != "---":
            f = next(x for x in cd["pnjs"] if x["n"] == p_a)
            cd["combate"].append({"Nombre": f["n"], "Iniciativa": 0, "HP": int(f["hp"]), "CA": int(f["ac"]), "Estado": ""})
            st.rerun()
        
        e_a = c2.selectbox("Añadir Enemigo", ["---"] + [x["n"] for x in cd["enemigos"]])
        if c2.button("Agregar Enemigo") and e_a != "---":
            f = next(x for x in cd["enemigos"] if x["n"] == e_a)
            cd["combate"].append({"Nombre": f["n"], "Iniciativa": 0, "HP": int(f["hp"]), "CA": int(f["ac"]), "Estado": ""})
            st.rerun()

        if cd["combate"]:
            df = pd.DataFrame(cd["combate"])
            # Forzar tipos para que aparezcan los botones +/-
            df["HP"] = df["HP"].astype(int)
            df["Iniciativa"] = df["Iniciativa"].astype(int)

            ed = st.data_editor(
                df,
                column_config={
                    "HP": st.column_config.NumberColumn("HP", step=1, format="%d ❤️"),
                    "Iniciativa": st.column_config.NumberColumn("Inic", step=1),
                    "Estado": st.column_config.SelectboxColumn("Estado", options=ESTADOS),
                    "Nombre": st.column_config.TextColumn("Nombre", disabled=True)
                },
                use_container_width=True,
                num_rows="dynamic",
                key="combat_editor_v5"
            )
            
            if st.button("💾 Guardar y Ordenar"):
                cd["combate"] = ed.sort_values("Iniciativa", ascending=False).to_dict('records')
                st.rerun()
            
            if st.button("🗑️ Limpiar Combate"):
                cd["combate"] = []
                st.rerun()

    with t_not:
        cd["notas"] = st.text_area("Notas:", value=cd["notas"], height=300)
        if st.button("Guardar Notas"): st.success("Guardado")
else:
    st.info("Crea o selecciona una campaña en el panel izquierdo.") 

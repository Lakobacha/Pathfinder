import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Pathfinder 2e GM Screen", layout="wide")

# Lista completa de estados para el desplegable
ESTADOS_PF2E = [
    "", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido", "Controlado", 
    "Deslumbrado", "Detenido", "Drenado", "Enfermo", "Fascinado", "Fatigado", 
    "Hechizado", "Inconsciente", "Invisible", "Maldito", "Paralizado", 
    "Petrificado", "Derribado", "Sordo", "Asustado", "Trabado"
]

if 'data' not in st.session_state:
    st.session_state.data = {}

# 2. BARRA LATERAL
with st.sidebar:
    st.header("🏰 Menú de Campaña")
    nueva_c = st.text_input("Nueva Campaña")
    if st.button("➕ Crear Campaña"):
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

# 3. CUERPO PRINCIPAL
st.title("🛡️ Pathfinder 2e GM Screen")

if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cd = st.session_state.data[camp_sel][libro_sel][cap_sel]
    
    # Asegurar llaves
    for k in ["mapas", "pnjs", "enemigos", "combate"]:
        if k not in cd: cd[k] = []

    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    with t_map:
        with st.expander("➕ Subir Mapa"):
            n_m = st.text_input("Nombre Mapa")
            i_m = st.file_uploader("Imagen", type=['png', 'jpg', 'jpeg'])
            d_m = st.text_area("Descripción/Habitaciones")
            if st.button("💾 Guardar Mapa"):
                if n_m and i_m:
                    cd["mapas"].append({"nombre": n_m, "img": i_m.getvalue(), "desc": d_m})
                    st.rerun()
        for m in cd["mapas"]:
            with st.container(border=True):
                st.subheader(m["nombre"])
                c1, c2 = st.columns([2, 1])
                c1.image(m["img"])
                c2.info(m["desc"])

    with t_pnj:
        st.write("### 👥 Fichas de PNJs")
        with st.expander("➕ Crear Nuevo PNJ"):
            with st.form("f_pnj_full"):
                c1, c2, c3 = st.columns([2, 1, 1])
                p_nom = c1.text_input("Nombre")
                p_niv = c2.number_input("Nivel", 0, 20)
                p_anc = c3.text_input("Ancestría/Clase")
                st.write("**Estadísticas**")
                s1, s2, s3, s4, s5, s6 = st.columns(6)
                fuer = s1.number_input("FUE", 10)
                des = s2.number_input("DES", 10)
                con = s3.number_input("CON", 10)
                int_ = s4.number_input("INT", 10)
                sab = s5.number_input("SAB", 10)
                car = s6.number_input("CAR", 10)
                st.write("**Defensas y Percepción**")
                v1, v2, v3 = st.columns(3)
                p_hp = v1.number_input("HP Máx", 1)
                p_ac = v2.number_input("CA", 10)
                p_per = v3.number_input("Percepción", 0)
                p_hab = st.text_area("Habilidades y Ataques")
                if st.form_submit_button("💾 Registrar PNJ"):
                    cd["pnjs"].append({"n": p_nom, "lvl": p_niv, "anc": p_anc, "hp": p_hp, "ac": p_ac, "per": p_per, "stats": [fuer, des, con, int_, sab, car], "hab": p_hab})
                    st.rerun()
        for p in cd["pnjs"]:
            with st.container(border=True):
                st.markdown(f"#### {p['n']} (Nivel {p['lvl']} {p['anc']})")
                st.write(f"**CA:** {p['ac']} | **HP:** {p['hp']} | **Per:** {p['per']}")
                st.caption(f"F:{p['stats'][0]} D:{p['stats'][1]} C:{p['stats'][2]} I:{p['stats'][3]} S:{p['stats'][4]} C:{p['stats'][5]}")
                st.info(p['hab'])

    with t_ene:
        st.write("### 👹 Bestiario")
        with st.expander("➕ Nuevo Enemigo"):
            with st.form("f_ene_full"):
                ce1, ce2 = st.columns([2, 1])
                e_nom = ce1.text_input("Nombre Criatura")
                e_niv = ce2.number_input("Nivel ", -1, 30)
                st.write("**Combate**")
                de1, de2, de3, de4, de5 = st.columns(5)
                e_hp = de1.number_input("Vida", 1)
                e_ac = de2.number_input("CA ", 10)
                e_f = de3.number_input("Fort", 0)
                e_r = de4.number_input("Ref", 0)
                e_v = de5.number_input("Vol", 0)
                e_desc = st.text_area("Habilidades/Ataques")
                if st.form_submit_button("💾 Registrar Enemigo"):
                    cd["enemigos"].append({"n": e_nom, "lvl": e_niv, "hp": e_hp, "ac": e_ac, "fort": e_f, "ref": e_r, "vol": e_v, "desc": e_desc})
                    st.rerun()
        for e in cd["enemigos"]:
            with st.container(border=True):
                st.markdown(f"#### {e['n']} (Nivel {e['lvl']})")
                st.write(f"**HP:** {e['hp']} | **CA:** {e['ac']} | **F/R/V:** {e['fort']}/{e['ref']}/{e['vol']}")
                st.warning(e['desc'])

    with t_com:
        st.subheader("⚔️ Combat Tracker")
        c1, c2 = st.columns(2)
        p_add = c1.selectbox("Añadir PNJ", ["---"] + [x["n"] for x in cd["pnjs"]])
        if c1.button("Añadir PNJ") and p_add != "---":
            ref = next(x for x in cd["pnjs"] if x["n"] == p_add)
            cd["combate"].append({"Nombre": ref["n"], "Iniciativa": 0, "HP": int(ref["hp"]), "CA": int(ref["ac"]), "Estado": ""})
            st.rerun()
        
        e_add = c2.selectbox("Añadir Enemigo", ["---"] + [x["n"] for x in cd["enemigos"]])
        if c2.button("Añadir Enemigo") and e_add != "---":
            ref = next(x for x in cd["enemigos"] if x["n"] == e_add)
            cd["combate"].append({"Nombre": ref["n"], "Iniciativa": 0, "HP": int(ref["hp"]), "CA": int(ref["ac"]), "Estado": ""})
            st.rerun()

        if cd["combate"]:
            df_com = pd.DataFrame(cd["combate"])
            # Configuración forzada del editor
            df_editado = st.data_editor(
                df_com,
                column_config={
                    "Nombre": st.column_config.TextColumn("Nombre", disabled=True),
                    "Iniciativa": st.column_config.NumberColumn("Inic", step=1, format="%d"),
                    "HP": st.column_config.NumberColumn("HP", step=1, format="%d ❤️"),
                    "AC": st.column_config.NumberColumn("CA", step=1),
                    "Estado": st.column_config.SelectboxColumn("Estado", options=ESTADOS_PF2E, width="medium")
                },
                use_container_width=True,
                num_rows="dynamic",
                key="combat_final"
            )
            
            if st.button("💾 Guardar y Ordenar"):
                cd["combate"] = df_editado.sort_values("Iniciativa", ascending=False).to_dict('records')
                st.rerun()
            if st.button("🗑️ Reset Combate", type="primary"):
                cd["combate"] = []
                st.rerun()

    with t_not:
        cd["notas"] = st.text_area("Notas:", value=cd["notas"], height=400)
        if st.button("💾 Guardar"): st.success("Guardado")
else:
    st.info("👈 Selecciona o crea una campaña en el panel lateral.") 

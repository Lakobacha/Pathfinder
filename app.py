import streamlit as st
import pandas as pd

# ==============================
# CONFIGURACIÓN
# ==============================
st.set_page_config(page_title="PF2e GM Screen", layout="wide")

ESTADOS_PF2E = [
    "", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido",
    "Controlado", "Deslumbrado", "Detenido", "Drenado", "Enfermo",
    "Fascinado", "Fatigado", "Hechizado", "Inconsciente", "Invisible",
    "Maldito", "Paralizado", "Petrificado", "Derribado", "Sordo",
    "Asustado", "Trabado"
]

if "data" not in st.session_state:
    st.session_state.data = {}

# ==============================
# BARRA LATERAL
# ==============================
with st.sidebar:
    st.header("🏰 Gestión de Campaña")

    nueva_c = st.text_input("Nombre de la Campaña")
    if st.button("➕ Crear Campaña"):
        if nueva_c:
            st.session_state.data[nueva_c] = {}
            st.rerun()

    camp_sel = st.selectbox(
        "Seleccionar Campaña",
        ["---"] + list(st.session_state.data.keys())
    )

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

        libro_sel = st.selectbox(
            "Seleccionar Libro",
            ["---"] + list(st.session_state.data[camp_sel].keys())
        )

        if libro_sel != "---":
            nuevo_cap = st.text_input("Nuevo Capítulo")
            if st.button("➕ Añadir Capítulo"):
                if nuevo_cap:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [],
                        "pnjs": [],
                        "enemigos": [],
                        "notas": "",
                        "combate": []
                    }
                    st.rerun()

            cap_sel = st.selectbox(
                "Seleccionar Capítulo",
                ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys())
            )
        else:
            cap_sel = "---"
    else:
        libro_sel = "---"
        cap_sel = "---"

# ==============================
# CUERPO PRINCIPAL
# ==============================
if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":

    cd = st.session_state.data[camp_sel][libro_sel][cap_sel]

    # Tabs principales
    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(
        ["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"]
    )

    # ==============================
    # MAPAS
    # ==============================
    with t_map:
        st.subheader("🗺️ Mapas del Capítulo")

        with st.expander("➕ Añadir Nuevo Mapa"):
            with st.form("form_mapa"):
                m_nombre = st.text_input("Nombre del mapa")
                m_desc = st.text_area("Información del mapa")
                m_img = st.file_uploader("Subir imagen", type=["png", "jpg", "jpeg"])

                if st.form_submit_button("💾 Guardar Mapa"):
                    if m_nombre:
                        cd["mapas"].append({
                            "nombre": m_nombre,
                            "desc": m_desc,
                            "img": m_img.getvalue() if m_img else None
                        })
                        st.rerun()

        # Mostrar mapas
        for mapa in cd["mapas"]:
            with st.container(border=True):
                st.markdown(f"### {mapa['nombre']}")
                if mapa["img"]:
                    st.image(mapa["img"], use_container_width=True)
                st.write(mapa["desc"])

    # ==============================
    # PNJs
    # ==============================
    with t_pnj:
        st.subheader("👥 PNJs")

        with st.expander("➕ Crear Nuevo PNJ"):
            with st.form("f_pnj"):
                p_nom = st.text_input("Nombre")
                p_niv = st.number_input("Nivel", 0, 20)
                p_hp = st.number_input("HP Máx", 1)
                p_ac = st.number_input("CA", 10)

                if st.form_submit_button("💾 Guardar PNJ"):
                    cd["pnjs"].append({
                        "n": p_nom,
                        "lvl": p_niv,
                        "hp": p_hp,
                        "ac": p_ac
                    })
                    st.rerun()

        for p in cd["pnjs"]:
            st.write(f"✅ {p['n']} (HP {p['hp']}, CA {p['ac']})")

    # ==============================
    # ENEMIGOS
    # ==============================
    with t_ene:
        st.subheader("👹 Enemigos")

        with st.expander("➕ Crear Nuevo Enemigo"):
            with st.form("f_enemigo"):
                e_nom = st.text_input("Nombre del enemigo")
                e_niv = st.number_input("Nivel", 0, 25)
                e_hp = st.number_input("HP Máx", 1)
                e_ac = st.number_input("CA", 10)

                if st.form_submit_button("💾 Guardar Enemigo"):
                    cd["enemigos"].append({
                        "n": e_nom,
                        "lvl": e_niv,
                        "hp": e_hp,
                        "ac": e_ac
                    })
                    st.rerun()

        for e in cd["enemigos"]:
            st.write(f"⚔️ {e['n']} (HP {e['hp']}, CA {e['ac']})")

    # ==============================
    # COMBATE
    # ==============================
    with t_com:
        st.subheader("⚔️ Combat Tracker")

        col1, col2 = st.columns(2)

        # Añadir PNJ
        p_add = col1.selectbox(
            "Añadir PNJ",
            ["---"] + [x["n"] for x in cd["pnjs"]]
        )
        if col1.button("➕ Añadir PNJ al Combate") and p_add != "---":
            ref = next(x for x in cd["pnjs"] if x["n"] == p_add)
            cd["combate"].append({
                "Nombre": ref["n"],
                "Iniciativa": 0,
                "HP": int(ref["hp"]),
                "CA": int(ref["ac"]),
                "Estado": ""
            })
            st.rerun()

        # Añadir Enemigo
        e_add = col2.selectbox(
            "Añadir Enemigo",
            ["---"] + [x["n"] for x in cd["enemigos"]]
        )
        if col2.button("➕ Añadir Enemigo al Combate") and e_add != "---":
            ref = next(x for x in cd["enemigos"] if x["n"] == e_add)
            cd["combate"].append({
                "Nombre": ref["n"],
                "Iniciativa": 0,
                "HP": int(ref["hp"]),
                "CA": int(ref["ac"]),
                "Estado": ""
            })
            st.rerun()

        # Tabla editable
        if cd["combate"]:
            df_c = pd.DataFrame(cd["combate"])

            ed_df = st.data_editor(
                df_c,
                column_config={
                    "Estado": st.column_config.SelectboxColumn(
                        "Estado",
                        options=ESTADOS_PF2E
                    )
                },
                use_container_width=True,
                num_rows="dynamic"
            )

            if st.button("💾 Guardar Cambios"):
                cd["combate"] = ed_df.to_dict("records")
                st.rerun()

            # HP rápido con botones
            st.divider()
            st.subheader("❤️ Ajuste rápido de HP")

            for i, combatiente in enumerate(cd["combate"]):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 2])

                c1.write(f"**{combatiente['Nombre']}**")

                if c2.button("➖ -5", key=f"menos{i}"):
                    combatiente["HP"] -= 5
                    st.rerun()

                if c3.button("➕ +5", key=f"mas{i}"):
                    combatiente["HP"] += 5
                    st.rerun()

                c4.write(f"HP actual: {combatiente['HP']}")

            if st.button("🗑️ Limpiar Combate"):
                cd["combate"] = []
                st.rerun()

    # ==============================
    # NOTAS
    # ==============================
    with t_not:
        cd["notas"] = st.text_area(
            "Bloc de notas",
            value=cd["notas"],
            height=400
        )
        if st.button("💾 Guardar Notas"):
            st.success("Notas guardadas")

else:
    st.info("Crea una campaña y un capítulo para empezar.")
 

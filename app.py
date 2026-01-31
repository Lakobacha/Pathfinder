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

    t_map, t_pnj, t_ene, t_com, t_not = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    # ======================================================
    # MAPAS
    # ======================================================
    with t_map:
        st.subheader("🗺️ Mapas del Capítulo")
        with st.expander("➕ Añadir Nuevo Mapa"):
            with st.form("f_mapa"):
                m_nom = st.text_input("Nombre del mapa")
                m_info = st.text_area("Información del mapa")
                m_img = st.file_uploader("Subir imagen del mapa", type=["png","jpg","jpeg"])
                if st.form_submit_button("💾 Guardar Mapa") and m_nom:
                    cd["mapas"].append({
                        "nombre": m_nom,
                        "info": m_info,
                        "img": m_img.getvalue() if m_img else None
                    })
                    st.rerun()
        for m in cd["mapas"]:
            with st.container(border=True):
                st.markdown(f"### {m['nombre']}")
                if m["img"]:
                    st.image(m["img"], use_container_width=True)
                st.write(m["info"])

    # ======================================================
    # PNJs
    # ======================================================
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
                st.write(f"**{p['n']}** | HP: {p['hp']} | CA: {p['ac']}")
                st.caption(f"F:{p['stats'][0]} D:{p['stats'][1]} C:{p['stats'][2]} I:{p['stats'][3]} S:{p['stats'][4]} Ch:{p['stats'][5]}")

    # ======================================================
    # ENEMIGOS
    # ======================================================
    with t_ene:
        with st.expander("➕ Crear Nuevo Enemigo"):
            with st.form("f_ene"):
                c1,c2,c3 = st.columns([2,1,1])
                e_nom = c1.text_input("Nombre")
                e_niv = c2.number_input("Nivel",0,25)
                e_tipo = c3.text_input("Tipo")
                s1,s2,s3,s4,s5,s6 = st.columns(6)
                f = s1.number_input("FUE",10,key="e_f")
                d = s2.number_input("DES",10,key="e_d")
                con = s3.number_input("CON",10,key="e_c")
                i = s4.number_input("INT",10,key="e_i")
                sab = s5.number_input("SAB",10,key="e_s")
                car = s6.number_input("CAR",10,key="e_ch")
                v1,v2,v3 = st.columns(3)
                e_hp = v1.number_input("HP Máx",1,key="e_hp")
                e_ac = v2.number_input("CA",10,key="e_ca")
                e_per = v3.number_input("Percepción",0,key="e_per")
                e_hab = st.text_area("Habilidades y Ataques",key="e_hab")
                if st.form_submit_button("💾 Guardar Enemigo"):
                    cd["enemigos"].append({"n":e_nom,"lvl":e_niv,"hp":e_hp,"ac":e_ac,"per":e_per,"stats":[f,d,con,i,sab,car],"hab":e_hab})
                    st.rerun()
        for e in cd["enemigos"]:
            with st.container(border=True):
                st.write(f"**{e['n']}** | HP: {e['hp']} | CA: {e['ac']}")
                st.caption(f"F:{e['stats'][0]} D:{e['stats'][1]} C:{e['stats'][2]} I:{e['stats'][3]} S:{e['stats'][4]} Ch:{e['stats'][5]}")

    # ======================================================
    # COMBAT TRACKER INTERACTIVO
    # ======================================================
    with t_com:
        st.subheader("⚔️ Combat Tracker")

        col1, col2 = st.columns(2)
        sel = col1.selectbox("Añadir PNJ al combate", ["---"] + [x["n"] for x in cd["pnjs"]])
        if col1.button("Añadir") and sel != "---":
            ref = next(x for x in cd["pnjs"] if x["n"]==sel)
            cd["combate"].append({"Nombre":ref["n"], "Iniciativa":0, "HP":int(ref["hp"]), "CA":int(ref["ac"]), "Estado":""})
            st.rerun()

        # Mostrar combatientes
        for idx,c in enumerate(cd["combate"]):
            cols = st.columns([2,1,0.5,0.5,1,2])
            cols[0].write(f"**{c['Nombre']}**")
            c["Iniciativa"] = cols[1].number_input("Iniciativa", value=c["Iniciativa"], step=1, key=f"ini_{idx}")
            if cols[2].button("➖", key=f"hp_minus_{idx}"): c["HP"]-=1
            if cols[3].button("➕", key=f"hp_plus_{idx}"): c["HP"]+=1
            cols[4].write(f"HP: {c['HP']}")
            cols[5].selectbox("Estado", ESTADOS_PF2E, index=ESTADOS_PF2E.index(c['Estado']) if c['Estado'] in ESTADOS_PF2E else 0, key=f"estado_{idx}")

        if st.button("Ordenar por iniciativa"):
            cd["combate"] = sorted(cd["combate"], key=lambda x:x["Iniciativa"], reverse=True)
            st.rerun()
        if st.button("🗑️ Limpiar combate"):
            cd["combate"]=[]
            st.rerun()

    # ======================================================
    # NOTAS
    # ======================================================
    with t_not:
        cd["notas"] = st.text_area("Bloc de notas", value=cd["notas"], height=400)
        if st.button("💾 Guardar Notas"):
            st.success("Guardado")

else:
    st.info("Crea una campaña y un capítulo para empezar.")
 

import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Pathfinder 2e", layout="wide")

# CSS para botones y estética
st.markdown("""
<style>
    div.stButton > button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
    .stDataEditor { border: 1px solid #4a4a4a; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# Lista de estados oficiales PF2e en español
ESTADOS_PF2E = [
    "", "Agarrado", "Apresado", "Aturdido", "Cegado", "Confundido", "Controlado", 
    "Deslumbrado", "Detenido", "Drenado", "Enfermo", "Fascinado", "Fatigado", 
    "Hechizado", "Inconsciente", "Invisible", "Maldito", "Paralizado", 
    "Petrificado", "Prone (Derribado)", "Sordo", "Sustado", "Trabado"
]

# 2. MEMORIA
if 'data' not in st.session_state:
    st.session_state.data = {}

# 3. BARRA LATERAL (Simplificada para brevedad, mantiene tu lógica)
with st.sidebar:
    st.header("1. Campaña")
    nueva_c = st.text_input("Nueva Campaña")
    if st.button("➕ Crear"):
        if nueva_c: st.session_state.data[nueva_c] = {}; st.rerun()
    
    camp_sel = st.selectbox("Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        st.divider()
        st.header("2. Libros")
        nuevo_l = st.text_input("Nuevo Libro")
        if st.button("➕ Añadir"):
            if nuevo_l: st.session_state.data[camp_sel][nuevo_l] = {}; st.rerun()
        
        libro_sel = st.selectbox("Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))

        if libro_sel != "---":
            st.divider()
            st.header("3. Capítulos")
            nuevo_cap = st.text_input("Nuevo Capítulo")
            if st.button("➕"):
                if nuevo_cap:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [], "pnjs": [], "enemigos": [], "notas": "", "combate": []
                    }
                    st.rerun()
            cap_sel = st.selectbox("Capítulo", ["---"] + list(st.session_state.data[camp_sel][libro_sel].keys()))
        else: cap_sel = "---"
        
        if st.sidebar.button(f"🚨 BORRAR CAMPAÑA", type="primary"):
            del st.session_state.data[camp_sel]; st.rerun()
    else: libro_sel, cap_sel = "---", "---"

# 4. ÁREA DE TRABAJO
st.title("🛡️ Pathfinder 2e")

if camp_sel != "---" and libro_sel != "---" and cap_sel != "---":
    cap_data = st.session_state.data[camp_sel][libro_sel][cap_sel]
    t_mapas, t_pnjs, t_enemigos, t_combate, t_notas = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "⚔️ Combate", "📝 Notas"])

    # (Las pestañas de Mapas, PNJs y Enemigos consumen los datos creados antes)
    # ... (Se omite el código repetido de creación para ir al grano con el combate) ...

    with t_combate:
        st.write("### ⚔️ Control de Iniciativa y Estados")
        
        c_add1, c_add2 = st.columns(2)
        with c_add1:
            pnj_n = st.selectbox("Importar PNJ", ["---"] + [p["n"] for p in cap_data.get("pnjs", [])])
            if st.button("Añadir PNJ") and pnj_n != "---":
                p = next(x for x in cap_data["pnjs"] if x["n"] == pnj_n)
                cap_data["combate"].append({"Nombre": p["n"], "Iniciativa": 0, "HP": p["hp"], "CA": p["ac"], "Estado": ""})
                st.rerun()

        with c_add2:
            ene_n = st.selectbox("Importar Enemigo", ["---"] + [e["n"] for e in cap_data.get("enemigos", [])])
            if st.button("Añadir Enemigo") and ene_n != "---":
                e = next(x for x in cap_data["enemigos"] if x["n"] == ene_n)
                cap_data["combate"].append({"Nombre": e["n"], "Iniciativa": 0, "HP": e["hp"], "CA": e["ac"], "Estado": ""})
                st.rerun()

        if cap_data["combate"]:
            df = pd.DataFrame(cap_data["combate"])
            
            # CONFIGURACIÓN DE COLUMNAS DEL EDITOR
            # st.data_editor permite subir/bajar números con flechas y menús desplegables
            df_editado = st.data_editor(
                df,
                column_config={
                    "Iniciativa": st.column_config.NumberColumn("Inic.", format="%d 🎲", step=1),
                    "HP": st.column_config.NumberColumn("Vida (HP)", step=1, format="%d ❤️"),
                    "CA": st.column_config.NumberColumn("CA", format="%d 🛡️"),
                    "Estado": st.column_config.SelectboxColumn(
                        "Estado Condición",
                        options=ESTADOS_PF2E,
                        width="medium"
                    ),
                    "Nombre": st.column_config.TextColumn("Nombre", disabled=True)
                },
                num_rows="dynamic",
                use_container_width=True,
                key="combat_editor"
            )

            col_b1, col_b2 = st.columns([1, 5])
            if col_b1.button("💾 Guardar y Ordenar"):
                # Ordenar por iniciativa antes de guardar
                cap_data["combate"] = df_editado.sort_values(by="Iniciativa", ascending=False).to_dict('records')
                st.rerun()
            
            if col_b2.button("🗑️ Resetear Combate", type="primary"):
                cap_data["combate"] = []
                st.rerun()
            
            st.caption("💡 Puedes usar las flechas en la celda de HP para subir/bajar la vida rápidamente.")
        else:
            st.info("No hay combatientes activos.")

    # (Pestañas de Notas, Mapas etc siguen funcionando igual)
    with t_notas:
        cap_data["notas"] = st.text_area("Notas:", value=cap_data.get("notas", ""), height=300)
        if st.button("Guardar"): st.success("Ok")

else:
    st.info("Configura la campaña en el lateral.") 

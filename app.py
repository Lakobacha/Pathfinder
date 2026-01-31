import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Pathfinder 2e", layout="wide")

# 2. ESTRUCTURA DE MEMORIA
if 'data' not in st.session_state:
    st.session_state.data = {}

# 3. BARRA LATERAL: JERARQUÍA (Campaña > Libro > Capítulo)
with st.sidebar:
    st.header("1. Campaña")
    nueva_c = st.text_input("Nombre de Campaña")
    if st.button("➕ Crear Campaña"):
        if nueva_c and nueva_c not in st.session_state.data:
            st.session_state.data[nueva_c] = {}
            st.rerun()
    
    camp_sel = st.selectbox("Seleccionar Campaña", ["---"] + list(st.session_state.data.keys()))

    if camp_sel != "---":
        st.divider()
        st.header("2. Libros")
        nuevo_l = st.text_input("Nombre del Libro")
        if st.button("➕ Añadir Libro"):
            if nuevo_l and nuevo_l not in st.session_state.data[camp_sel]:
                st.session_state.data[camp_sel][nuevo_l] = {}
                st.rerun()
        
        libro_sel = st.selectbox("Seleccionar Libro", ["---"] + list(st.session_state.data[camp_sel].keys()))

        if libro_sel != "---":
            st.divider()
            st.header("3. Capítulos")
            nuevo_cap = st.text_input("Nombre del Capítulo")
            if st.button("➕ Añadir Capítulo"):
                if nuevo_cap not in st.session_state.data[camp_sel][libro_sel]:
                    st.session_state.data[camp_sel][libro_sel][nuevo_cap] = {
                        "mapas": [],
                        "pnjs": [],
                        "enemigos": [],
                        "notas": ""
                    }
                    st.rerun()

# 4. ÁREA DE TRABAJO (Solo el Sistema y Pestañas)
if camp_sel != "---" and libro_sel != "---":
    # Título limpio del sistema
    st.title("🛡️ Pathfinder 2e")
    
    lista_caps = list(st.session_state.data[camp_sel][libro_sel].keys())
    
    if lista_caps:
        cap_sel = st.radio("Capítulos:", lista_caps, horizontal=True)
        cap_data = st.session_state.data[camp_sel][libro_sel][cap_sel]

        # PESTAÑAS INDEPENDIENTES
        t_mapas, t_pnjs, t_enemigos, t_notas = st.tabs(["🗺️ Mapas", "👥 PNJs", "👹 Enemigos", "📝 Notas"])

        with t_mapas:
            # Sección de Mapas
            with st.expander("➕ Subir Nuevo Mapa"):
                nombre_mapa = st.text_input("Nombre del Mapa/Zona")
                img_file = st.file_uploader("Imagen del Mapa", type=['png', 'jpg', 'jpeg'])
                info_hab = st.text_area("Información de Habitaciones")
                
                if st.button("💾 Guardar Mapa"):
                    if nombre_mapa and img_file:
                        cap_data["mapas"].append({
                            "nombre": nombre_mapa,
                            "imagen": img_file.getvalue(),
                            "info": info_hab
                        })
                        st.rerun()

            for m in cap_data["mapas"]:
                with st.container(border=True):
                    st.write(f"#### {m['nombre']}")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.image(m['imagen'], use_container_width=True)
                    with col2:
                        st.info(m['info'])
    else:
        st.info("Crea un capítulo para comenzar.")
else:
    st.title("🛡️ Pathfinder 2e")
    st.info("Configura la campaña y el libro en el panel izquierdo.") 

# ======================================================
    # ⚔️ COMBATE (TRACKER DE INICIATIVA)
    # ======================================================
    with t_com:
        st.subheader("⚔️ Rastreador de Iniciativa")
        
        # Formulario para añadir combatientes
        with st.expander("➕ Añadir Combatiente"):
            with st.form("f_combate"):
                c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                nombre_c = c1.text_input("Nombre")
                ini_c = c2.number_input("Iniciativa", 0, 50, value=10)
                hp_c = c3.number_input("HP actual", 0, 500, value=20)
                tipo_c = c4.selectbox("Tipo", ["PJ", "Enemigo", "PNJ"])
                
                if st.form_submit_button("Añadir al Turno"):
                    if nombre_c:
                        cd["combate"].append({
                            "nombre": nombre_c,
                            "iniciativa": ini_c,
                            "hp": hp_c,
                            "tipo": tipo_c,
                            "estados": []
                        })
                        # Ordenar automáticamente por iniciativa
                        cd["combate"] = sorted(cd["combate"], key=lambda x: x["iniciativa"], reverse=True)
                        st.rerun()

        if cd["combate"]:
            # Botón para limpiar combate
            if st.button("🗑️ Limpiar Todo el Combate"):
                cd["combate"] = []
                st.rerun()

            st.divider()
            
            # Encabezados de la tabla
            h1, h2, h3, h4, h5 = st.columns([1, 2, 2, 3, 1])
            h1.write("**Ini**")
            h2.write("**Nombre**")
            h3.write("**HP**")
            h4.write("**Estados**")
            h5.write("**Acción**")

            # Lista de combatientes
            for idx, p en enumerate(cd["combate"]):
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 3, 1])
                    
                    # Iniciativa y Nombre
                    col1.write(f"`{p['iniciativa']}`")
                    color = "blue" if p["tipo"] == "PJ" else "red"
                    col2.markdown(f":{color}[**{p['nombre']}**]")
                    
                    # Gestión de HP
                    new_hp = col3.number_input(f"HP de {p['nombre']}", 0, 1000, value=p["hp"], key=f"hp_{idx}", label_visibility="collapsed")
                    cd["combate"][idx]["hp"] = new_hp
                    
                    # Gestión de Estados (Multi-select)
                    estados_activos = col4.multiselect(
                        f"Estados {p['nombre']}", 
                        ESTADOS_PF2E, 
                        default=p["estados"], 
                        key=f"est_{idx}",
                        label_visibility="collapsed"
                    )
                    cd["combate"][idx]["estados"] = estados_activos
                    
                    # Eliminar combatiente
                    if col5.button("❌", key=f"del_{idx}"):
                        cd["combate"].pop(idx)
                        st.rerun()
                st.divider()
        else:
            st.info("No hay combatientes en el turno. ¡Añade algunos arriba!")

    # --- ENEMY PLACEHOLDER (Para no borrarlo) ---
    with t_ene:
        st.info("👹 Aquí podrás gestionar el bestiario de este capítulo.") 

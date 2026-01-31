# --- PESTAÑA COMBATE (Configuración Robusta) ---
    with t_combate:
        st.subheader("⚔️ Control de Iniciativa y Estados")
        
        # Selectores para añadir personajes
        c1, c2 = st.columns(2)
        with c1:
            p_sel = st.selectbox("Importar PNJ", ["---"] + [x["n"] for x in cap_data.get("pnjs", [])])
            if st.button("Añadir PNJ") and p_sel != "---":
                ref = next(x for x in cap_data["pnjs"] if x["n"] == p_sel)
                cap_data["combate"].append({"Nombre": ref["n"], "Iniciativa": 0, "HP": int(ref["hp"]), "AC": int(ref["ac"]), "Estado": ""})
                st.rerun()
        
        with c2:
            e_sel = st.selectbox("Importar Enemigo", ["---"] + [x["n"] for x in cap_data.get("enemigos", [])])
            if st.button("Añadir Enemigo") and e_sel != "---":
                ref = next(x for x in cap_data["enemigos"] if x["n"] == e_sel)
                cap_data["combate"].append({"Nombre": ref["n"], "Iniciativa": 0, "HP": int(ref["hp"]), "AC": int(ref["ac"]), "Estado": ""})
                st.rerun()

        if cap_data["combate"]:
            # Convertimos a DataFrame asegurando tipos numéricos para que aparezcan los controles + / -
            df_c = pd.DataFrame(cap_data["combate"])
            df_c["HP"] = pd.to_numeric(df_c["HP"])
            df_c["Iniciativa"] = pd.to_numeric(df_c["Iniciativa"])

            # El Editor con configuración explícita
            edited = st.data_editor(
                df_c,
                column_config={
                    "Nombre": st.column_config.TextColumn("Nombre", disabled=True),
                    "Iniciativa": st.column_config.NumberColumn(
                        "Iniciativa", 
                        help="Tira 1d20 + Percepción",
                        step=1,
                        format="%d"
                    ),
                    "HP": st.column_config.NumberColumn(
                        "Vida (HP)", 
                        help="Usa + / - para ajustar la vida",
                        step=1, # Esto habilita los controles de incremento
                        format="%d ❤️"
                    ),
                    "AC": st.column_config.NumberColumn("CA", step=1, format="%d 🛡️"),
                    "Estado": st.column_config.SelectboxColumn(
                        "Estado / Condición",
                        help="Selecciona un estado de Pathfinder 2e",
                        options=ESTADOS_PF2E, # Aquí forzamos el menú desplegable
                        width="large",
                        required=False
                    )
                },
                use_container_width=True,
                num_rows="dynamic",
                key="editor_final_pf2e"
            )
            
            col_save, col_clear = st.columns([1, 4])
            if col_save.button("💾 Guardar y Ordenar"):
                # Ordenamos de mayor a menor iniciativa
                cap_data["combate"] = edited.sort_values("Iniciativa", ascending=False).to_dict('records')
                st.rerun()
            
            if col_clear.button("🗑️ Limpiar Combate", type="primary"):
                cap_data["combate"] = []
                st.rerun()
        else:
            st.info("El combate está vacío. Añade PNJs o Enemigos arriba.") 

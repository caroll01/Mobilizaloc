import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="MobilizaLoc", page_icon="🚀", layout="wide")

# ==================== DADOS INICIAIS ====================
if "locations" not in st.session_state:
    st.session_state.locations = {
        "qualificado": {"lat": 38.7223, "lon": -9.1393, "status": "Em espera", "last_update": datetime.now().strftime("%H:%M")},
        "membro1": {"lat": 41.1579, "lon": -8.6291, "status": "Em espera", "last_update": datetime.now().strftime("%H:%M")},
        "membro2": {"lat": 37.0194, "lon": -8.0573, "status": "Em espera", "last_update": datetime.now().strftime("%H:%M")},
        "membro3": {"lat": 40.2033, "lon": -8.4103, "status": "Em espera", "last_update": datetime.now().strftime("%H:%M")},
    }

if "qualified_users" not in st.session_state:
    st.session_state.qualified_users = ["qualificado"]

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "full_access" not in st.session_state:
    st.session_state.full_access = False

# ==================== LOGIN ====================
if st.session_state.current_user is None:
    st.title("🚀 MobilizaLoc")
    st.subheader("Sistema de Localização e Mobilização de Equipa")
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Nome de utilizador", placeholder="qualificado, membro1, membro2 ou membro3")
    with col2:
        password = st.text_input("Password", type="password")
    
    if st.button("Entrar", type="primary"):
        if password == "1234" and username in ["qualificado", "membro1", "membro2", "membro3"]:
            st.session_state.current_user = username
            st.success(f"Bem-vindo, {username}!")
            st.rerun()
        else:
            st.error("Credenciais erradas. Password de demonstração: 1234")

else:
    user = st.session_state.current_user
    st.title(f"Olá, {user} 👋")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.current_user = None
        st.session_state.full_access = False
        st.rerun()

    # Página pessoal
    st.subheader("📍 A tua página pessoal")
    my_loc = st.session_state.locations[user]
    
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.metric("Localização atual", f"{my_loc['lat']:.4f}, {my_loc['lon']:.4f}")
    with col2:
        st.metric("Status", my_loc["status"])
    with col3:
        st.metric("Atualizado", my_loc["last_update"])

    if st.button("📡 Mobilizar-me", type="primary", use_container_width=True):
        st.session_state.locations[user]["status"] = "Mobilizado ✅"
        st.session_state.locations[user]["last_update"] = datetime.now().strftime("%H:%M")
        st.session_state.locations[user]["lat"] += random.uniform(-0.008, 0.008)
        st.session_state.locations[user]["lon"] += random.uniform(-0.008, 0.008)
        st.success("Estás mobilizado! Localização enviada.")
        st.rerun()

    st.subheader("🗺️ Onde estás agora")
    df_personal = pd.DataFrame([{"lat": my_loc["lat"], "lon": my_loc["lon"], "name": user}])
    st.map(df_personal, use_container_width=True)

    # Acesso qualificado
    if user in st.session_state.qualified_users:
        st.divider()
        st.subheader("🔐 Acesso à localização de TODOS os elementos")
        st.info("Insere o código específico abaixo.")

        code = st.text_input("Código específico", type="password", placeholder="MOBILIZA2026")
        
        if st.button("Validar código"):
            if code == "MOBILIZA2026":
                st.session_state.full_access = True
                st.success("✅ Código validado! Acesso total concedido.")
                st.rerun()
            else:
                st.error("Código incorreto.")

        if st.session_state.full_access:
            st.subheader("🌍 Mapa Global - Todos os elementos")
            
            data = []
            for u, loc in st.session_state.locations.items():
                data.append({
                    "Elemento": u,

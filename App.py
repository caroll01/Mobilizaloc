import streamlit as st
import pandas as pd
import random
from datetime import datetime
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MobilizaLoc", page_icon="🚀", layout="wide")

# ==================== DADOS DOS MEMBROS (com foto e nome completo) ====================
if "locations" not in st.session_state:
    st.session_state.locations = {
        "qualificado": {
            "nome": "Comandante Qualificado",
            "lat": 38.7223, "lon": -9.1393,
            "status": "Em espera",
            "last_update": datetime.now().strftime("%H:%M"),
            "foto": "https://picsum.photos/id/1015/300/300"   # foto de demonstração
        },
        "membro1": {
            "nome": "João Silva",
            "lat": 41.1579, "lon": -8.6291,
            "status": "Em espera",
            "last_update": datetime.now().strftime("%H:%M"),
            "foto": "https://picsum.photos/id/64/300/300"
        },
        "membro2": {
            "nome": "Maria Santos",
            "lat": 37.0194, "lon": -8.0573,
            "status": "Em espera",
            "last_update": datetime.now().strftime("%H:%M"),
            "foto": "https://picsum.photos/id/1005/300/300"
        },
        "membro3": {
            "nome": "Pedro Costa",
            "lat": 40.2033, "lon": -8.4103,
            "status": "Em espera",
            "last_update": datetime.now().strftime("%H:%M"),
            "foto": "https://picsum.photos/id/201/300/300"
        }
    }

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "full_access" not in st.session_state:
    st.session_state.full_access = False

# ==================== LOGIN ====================
if st.session_state.current_user is None:
    st.title("🚀 MobilizaLoc")
    st.subheader("Sistema de Localização de Equipa")

    username = st.text_input("Nome de utilizador", placeholder="qualificado, membro1, membro2 ou membro3")
    password = st.text_input("Password", type="password")

    if st.button("Entrar", type="primary"):
        if password == "1234" and username in ["qualificado", "membro1", "membro2", "membro3"]:
            st.session_state.current_user = username
            st.success(f"Bem-vindo, {username}!")
            st.rerun()
        else:
            st.error("Password errada. Usa **1234**")

else:
    user = st.session_state.current_user
    st.title(f"Olá, {user} 👋")

    if st.sidebar.button("🚪 Sair"):
        st.session_state.current_user = None
        st.session_state.full_access = False
        st.rerun()

    # ==================== PÁGINA PESSOAL ====================
    loc = st.session_state.locations[user]

    st.subheader("📍 A tua localização")
    st.metric("Nome", loc["nome"])
    st.metric("Coordenadas", f"{loc['lat']:.4f}, {loc['lon']:.4f}")
    st.metric("Estado", loc["status"])

    if st.button("📡 Mobilizar-me", type="primary", use_container_width=True):
        loc["status"] = "Mobilizado ✅"
        loc["last_update"] = datetime.now().strftime("%H:%M")
        loc["lat"] += random.uniform(-0.015, 0.015)
        loc["lon"] += random.uniform(-0.015, 0.015)
        st.success("Localização atualizada!")
        st.rerun()

    st.subheader("🗺️ Onde estás agora")
    df_personal = pd.DataFrame([{"lat": loc["lat"], "lon": loc["lon"]}])
    st.map(df_personal, zoom=12, use_container_width=True)

    # ==================== MAPA GLOBAL PARA QUALIFICADOS ====================
    if user == "qualificado":
       st.divider()
        st.subheader("🔐 Mapa Global - Clique nos pontos para ver detalhes")

        code = st.text_input("Código específico", typ e="password", placeholder="MOBILIZA2026")

        if st.button("Validar código"):
            if code == "MOBILIZA2026":
                st.session_state.full_access = True
                st.success("✅ Acesso total concedido!")
                st.rerun()
            else:
                st.error("Código incorreto")

        if st.session_state.full_access:
            # Cria o mapa interativo com Folium

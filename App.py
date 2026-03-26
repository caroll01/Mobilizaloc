import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="MobilizaLoc", page_icon="🚀", layout="wide")

# Dados de localização
if "locations" not in st.session_state:
    st.session_state.locations = {
        "qualificado": {"lat": 38.7223, "lon": -9.1393, "status": "Em espera", "last_update": datetime.now().strftime("%H:%M")},
        "membro1": {"lat": 41.1579, "lon": -8.6291, "status": "Em espera", "last_update": datetime.now().strftime("%H:%M")},
        "membro2": {"lat": 37.0194, "lon": -8.0573, "status": "Em espera", "last_update": datetime.now().strftime("%H:%M")},
        "membro3": {"lat": 40.2033, "lon": -8.4103, "status": "Em espera", "last_update": datetime.now().strftime("%H:%M")}
    }

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "full_access" not in st.session_state:
    st.session_state.full_access = False

# === TELA DE LOGIN ===
if st.session_state.current_user is None:
    st.title("🚀 MobilizaLoc")
    st.subheader("Sistema de Localização de Equipa")

    username = st.text_input("Nome de utilizador", placeholder="qualificado ou membro1")
    password = st.text_input("Password", type="password")

    if st.button("Entrar"):
        if password == "1234" and username in ["qualificado", "membro1", "membro2", "membro3"]:
            st.session_state.current_user = username
            st.success(f"Bem-vindo, {username}!")
            st.rerun()
        else:
            st.error("Password errada. Tenta 1234")

else:
    user = st.session_state.current_user
    st.title(f"Olá, {user}")

    if st.sidebar.button("Sair"):
        st.session_state.current_user = None
        st.session_state.full_access = False
        st.rerun()

    # Página pessoal de cada membro
    loc = st.session_state.locations[user]

    st.subheader("📍 A tua localização")
    st.metric("Coordenadas", f"{loc['lat']:.4f}, {loc['lon']:.4f}")
    st.metric("Estado", loc["status"])

    if st.button("📡 Mobilizar-me", type="primary"):
        loc["status"] = "Mobilizado ✅"
        loc["last_update"] = datetime.now().strftime("%H:%M")
        loc["lat"] += random.uniform(-0.01, 0.01)
        loc["lon"] += random.uniform(-0.01, 0.01)
        st.success("Localização atualizada!")
        st.rerun()

    # Mapa pessoal
    st.map(pd.DataFrame([{"lat": loc["lat"], "lon": loc["lon"]}]))

    # === PARTE PARA O QUALIFICADO ===
    if user == "qualificado":
        st.divider()
        st.subheader("🔐 Mapa de Todos os Elementos")

        code = st.text_input("Código de acesso", type="password", placeholder="MOBILIZA2026")

        if st.button("Validar"):
            if code == "MOBILIZA2026":
                st.session_state.full_access = True
                st.success("Acesso concedido!")
                st.rerun()
            else:
                st.error("Código incorreto")

        if st.session_state.full_access:
            # Cria a lista para o mapa
            data = []
            for nome, info in st.session_state.locations.items():
                data.append({
                    "Elemento": nome,
                    "Latitude": info["lat"],
                    "Longitude": info["lon"],
                    "Estado": info["status"]
                })

            df = pd.DataFrame(data)
            st.map(df)
            st.dataframe(df, use_container_width=True)

st.caption("MobilizaLoc - Versão simplificada")

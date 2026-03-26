import streamlit as st
import pandas as pd
import random
from datetime import datetime
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="MobilizaLoc", page_icon="🚀", layout="wide")

# Dados dos membros (com número de identificação)
if "locations" not in st.session_state:
    st.session_state.locations = {
        "qualificado": {
            "nome": "Comandante Qualificado",
            "numero_id": "Q-001",
            "lat": 38.7223, "lon": -9.1393,
            "status": "Em espera",
            "last_update": datetime.now().strftime("%H:%M"),
            "foto": "https://picsum.photos/id/1015/300/300"
        },
        "membro1": {
            "nome": "Francisco Pereira",
            "numero_id": "M-12345",
            "lat": 41.1579, "lon": -8.6291,
            "status": "Em espera",
            "last_update": datetime.now().strftime("%H:%M"),
            "foto": "https://picsum.photos/id/64/300/300"
        },
        "membro2": {
            "nome": "Maria Santos",
            "numero_id": "M-67890",
            "lat": 37.0194, "lon": -8.0573,
            "status": "Em espera",
            "last_update": datetime.now().strftime("%H:%M"),
            "foto": "https://picsum.photos/id/1005/300/300"
        },
        "membro3": {
            "nome": "Pedro Costa",
            "numero_id": "M-11223",
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

# LOGIN
if st.session_state.current_user is None:
    st.title("🚀 MobilizaLoc")
    st.subheader("Sistema de Localização de Equipa")

    username = st.text_input("Nome de utilizador", placeholder="qualificado, membro1, membro2 ou membro3")
    password = st.text_input("Password", type="password")

    if st.button("Entrar", type="primary"):
        if password == "1234" and username in list(st.session_state.locations.keys()):
            st.session_state.current_user = username
            st.success(f"Bem-vindo, {username}!")
            st.rerun()
        else:
            st.error("Password errada. Usa 1234")
else:
    user = st.session_state.current_user
    st.title(f"Olá, {user} 👋")

    if st.sidebar.button("🚪 Sair"):
        st.session_state.current_user = None
        st.session_state.full_access = False
        st.rerun()

    loc = st.session_state.locations[user]

    # Página pessoal
    st.subheader("📍 A tua localização")
    st.metric("Nome", loc["nome"])
    st.metric("Número de Identificação", loc.get("numero_id", "—"))
    st.metric("Coordenadas", f"{loc['lat']:.4f}, {loc['lon']:.4f}")
    st.metric("Estado", loc["status"])

    # Botão para mudar foto
    nova_foto = st.text_input("URL da tua foto (opcional)", value=loc["foto"])
    if st.button("Atualizar foto"):
        loc["foto"] = nova_foto
        st.success("Foto atualizada!")
        st.rerun()

    if st.button("📡 Mobilizar-me", type="primary", use_container_width=True):
        loc["status"] = "Mobilizado ✅"
        loc["last_update"] = datetime.now().strftime("%H:%M")
        loc["lat"] += random.uniform(-0.015, 0.015)
        loc["lon"] += random.uniform(-0.015, 0.015)
        st.success("Mobilizado! O qualificado já consegue ver.")
        st.rerun()

    st.subheader("🗺️ Onde estás agora")
    st.map(pd.DataFrame([{"lat": loc["lat"], "lon": loc["lon"]}]), zoom=12, use_container_width=True)

    # ==================== ÁREA DO QUALIFICADO ====================
    if user == "qualificado":
        st.divider()
        st.subheader("🔐 Mapa Global - Clique nos pontos")

        code = st.text_input("Código específico", type="password", placeholder="MOBILIZA2026")

        if st.button("Validar código"):
            if code == "MOBILIZA2026":
                st.session_state.full_access = True
                st.success("✅ Acesso total!")
                st.rerun()
            else:
                st.error("Código incorreto")

        if st.session_state.full_access:
            # Mapa global clicável
            m = folium.Map(location=[39.5, -8.0], zoom_start=7)
            for nome_user, info in st.session_state.locations.items():
                popup_text = f"""
                <b>{info['nome']}</b><br>
                Número: {info.get('numero_id', '—')}<br>
                Estado: {info['status']}<br>
                Atualizado: {info['last_update']}<br>
                Coordenadas: {info['lat']:.4f}, {info['lon']:.4f}
                """
                folium.Marker(
                    [info["lat"], info["lon"]],
                    popup=popup_text,
                    tooltip=info["nome"],
                    icon=folium.Icon(color="red" if "Mobilizado" in info["status"] else "blue")
                ).add_to(m)
            st_folium(m, width=700, height=500, use_container_width=True)

            # Adicionar novo membro
            st.subheader("➕ Adicionar novo membro")
            with st.form("novo_membro"):
                novo_nome = st.text_input("Nome completo")
                novo_id = st.text_input("Número de Identificação")
                nova_foto_url = st.text_input("URL da foto", "https://picsum.photos/id/1005/300/300")
                if st.form_submit_button("Adicionar membro"):
                    novo_username = "membro" + str(len(st.session_state.locations))
                    st.session_state.locations[novo_username] = {
                        "nome": novo_nome,
                        "numero_id": novo_id,
                        "lat": 38.7 + random.uniform(-0.5, 0.5),
                        "lon": -9.1 + random.uniform(-0.5, 0.5),
                        "status": "Em espera",
                        "last_update": datetime.now().strftime("%H:%M"),
                        "foto": nova_foto_url
                    }
                    st.success(f"Membro {novo_nome} adicionado!")
                    st.rerun()

st.caption("MobilizaLoc • Versão com GPS, edição e adição de membros")

# **************************************************/

# Project: Design-Patterns-for-IoT-Embedded-Systems
# Data: 01/11/2024
# Version: 1.0
# Description: This code implements the platform based on Design Patterns, where the devices (Raspberry Pi and Esp8266) are integrated for reading
#              temperature and making it available on the platform through observer methods and creating objects with the Factory Method and Builder Pattern.
#              The created objects are based on reading the I/O list from an Excel file.
# License: MIT

# **************************************************/

##################### INICIO DE PROGRAMA ############################################################

import atexit
import os
import sys
from threading import Event, Thread

import streamlit as st
from streamlit_autorefresh import st_autorefresh

##################### INICIO DA PLATAFORMA BROKER ###################################################

# Configuração da página do Streamlit
st.set_page_config(layout="wide", page_title="Broker IoT", page_icon="🔧")

# Diretório atual (onde está o broker.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Diretório pai (raiz do projeto)
parent_dir = os.path.abspath(os.path.join(script_dir, ".."))

# Diretório 'src' dentro do projeto
src_dir = os.path.join(parent_dir, "src")

# Diretório 'styles' dentro do projeto
styles_dir = os.path.join(parent_dir, "styles")

# Adiciona o 'parent_dir' e 'src_dir' ao sys.path, se ainda não estiverem
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

if src_dir not in sys.path:
    sys.path.append(src_dir)

from src.devices import AIDevicePublisher

# Importações dos módulos
from src.main import ler_sensor, processar_e_criar_dispositivos
from src.observer import GenericSubscriber


# Carregar CSS personalizado
def load_css():
    css_path = os.path.join(styles_dir, "styles.css")
    if not os.path.exists(css_path):
        st.error(f"Arquivo CSS não encontrado: {css_path}")
        return

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Chamando a função para carregar o CSS
load_css()

# Carregar dispositivos criados usando a função do main.py
if "dispositivos_criados" not in st.session_state:
    try:
        dispositivos_criados = processar_e_criar_dispositivos()
        st.session_state["dispositivos_criados"] = dispositivos_criados
        if not dispositivos_criados:
            st.error("Nenhum dispositivo foi criado. Verifique o arquivo Excel.")
    except Exception as e:
        st.error(f"Erro ao processar e criar dispositivos: {e}")
else:
    dispositivos_criados = st.session_state["dispositivos_criados"]

# Verificar se dispositivos_criados está definido e não está vazio
if not dispositivos_criados:
    st.stop()  # Parar a execução do Streamlit se não houver dispositivos

# Iniciar a thread de leitura do sensor
if "sensor_thread" not in st.session_state:
    stop_event = Event()
    sensor_thread = Thread(
        target=ler_sensor, args=(dispositivos_criados, stop_event), daemon=True
    )
    sensor_thread.start()
    st.session_state["sensor_thread"] = sensor_thread
    st.session_state["stop_event"] = stop_event


# Função para parar a thread ao encerrar a aplicação
def stop_sensor_thread():
    if "stop_event" in st.session_state:
        st.session_state["stop_event"].set()
        st.session_state["sensor_thread"].join()


# Registrar a função de limpeza para ser chamada quando o programa sair
atexit.register(stop_sensor_thread)

# Atualização automática da página a cada 1000ms (1 segundo)
st_autorefresh(interval=400, key="data_refresh")

##################### MENU LATERAL ####################################################

# Sidebar
image_path = os.path.join(parent_dir, "assets", "image.png")
if os.path.exists(image_path):
    st.sidebar.image(image_path, width=300)
else:
    st.sidebar.error(f"Imagem não encontrada: {image_path}")

st.sidebar.title("MENU")
page = st.sidebar.selectbox("Selecione a página", ["Broker", "Visualização"])

##################### CABEÇALHO ####################################################

# Cabeçalho
st.markdown(
    '<div class="custom-header">BROKER - DESIGN PATTERN FOR IOT INTEGRATION</div>',
    unsafe_allow_html=True,
)

##################### PÁGINA PRINCIPAL BROKER ####################################################

if page == "Broker":
    ##################### "use state" PARA MANTER DADOS NA MEMORIA ####################################################

    if "associacoes" not in st.session_state:
        st.session_state["associacoes"] = []
    associacoes = st.session_state["associacoes"]

    ##################### PREENCHE COM OBJETOS CRIADOS E ASSOCIA ####################################################

    st.title("Gerenciador de Associações de Dispositivos")
    st.header("Criar Nova Associação")

    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        dispositivos_ai = [
            d.tag for d in dispositivos_criados if isinstance(d, AIDevicePublisher)
        ]
        dispositivo_selecionado = st.selectbox(
            "Dispositivo AI:", dispositivos_ai, key="novo_dispositivo"
        )

    with col2:
        subscriber_name = st.text_input("Associar com:", key="novo_subscriber")

    def adicionar_associacao():
        dispositivo_tag = dispositivo_selecionado
        subscriber_name_input = subscriber_name.strip()

        if not subscriber_name_input:
            st.warning("Por favor, insira o nome do objeto associado.")
            return

        if any(
            assoc["dispositivo"] == dispositivo_tag
            and assoc["subscriber"] == subscriber_name_input
            for assoc in associacoes
        ):
            st.warning("Essa associação já existe.")
            return

        dispositivo = next(
            (d for d in dispositivos_criados if d.tag == dispositivo_tag), None
        )

        if dispositivo and isinstance(dispositivo, AIDevicePublisher):
            observer = GenericSubscriber(subscriber_name_input)
            dispositivo.attach(observer)
            associacoes.append(
                {
                    "dispositivo": dispositivo_tag,
                    "subscriber": subscriber_name_input,
                    "observer": observer,
                }
            )
            st.session_state["associacoes"] = associacoes.copy()
            st.success(
                f"Associação criada entre {dispositivo_tag} e {subscriber_name_input}"
            )
        else:
            st.error("Dispositivo não encontrado ou inválido.")

    with col3:
        st.button("Criar Associação", on_click=adicionar_associacao)

    st.markdown("---")

    ##################### ATUALIZAÇÃO DA TABELA DE ASSOCIAÇÕES ####################################################

    # Exibe a lista de associações
    st.header("Associações Criadas")
    if associacoes:
        cols = st.columns([1, 3, 3, 3, 1])
        cols[0].markdown('<div class="table-header">Nº</div>', unsafe_allow_html=True)
        cols[1].markdown(
            '<div class="table-header">Dispositivo AI</div>', unsafe_allow_html=True
        )
        cols[2].markdown(
            '<div class="table-header">Objeto Associado</div>', unsafe_allow_html=True
        )
        cols[3].markdown(
            '<div class="table-header">Valor em Tempo Real</div>',
            unsafe_allow_html=True,
        )
        cols[4].markdown(
            '<div class="table-header">Ações</div>', unsafe_allow_html=True
        )

        for i, assoc in enumerate(associacoes):
            dispositivo = next(
                (d for d in dispositivos_criados if d.tag == assoc["dispositivo"]), None
            )
            current_value = (
                f"{dispositivo.value} {dispositivo.unit}"
                if dispositivo and isinstance(dispositivo, AIDevicePublisher)
                else "N/A"
            )

            cols = st.columns([1, 3, 3, 3, 1])
            cols[0].markdown(
                f'<div class="table-cell">{i+1}</div>', unsafe_allow_html=True
            )
            cols[1].markdown(
                f'<div class="table-cell">{assoc["dispositivo"]}</div>',
                unsafe_allow_html=True,
            )
            cols[2].markdown(
                f'<div class="table-cell">{assoc["subscriber"]}</div>',
                unsafe_allow_html=True,
            )
            cols[3].markdown(
                f'<div class="table-cell">{current_value}</div>', unsafe_allow_html=True
            )

            if cols[4].button("❌", key=f"remove_{i}"):
                if dispositivo:
                    dispositivo.detach(assoc["observer"])
                associacoes.pop(i)
                st.session_state["associacoes"] = associacoes.copy()
                st.experimental_rerun()
    else:
        st.info("Nenhuma associação criada ainda.")

    st.markdown("---")

    ##################### NOTIFICA OBSERVADORES ####################################################

    st.header("Notificações dos Observadores")
    if associacoes:
        for assoc in associacoes:
            observer = assoc["observer"]
            if observer.notifications:
                st.subheader(f"Objeto Associado: {observer.name}")
                for notification in observer.notifications[-5:]:
                    st.write(notification)
            else:
                st.write(
                    f"Objeto Associado: {observer.name} - Nenhuma notificação ainda."
                )
    else:
        st.info("Nenhuma notificação para exibir.")

    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Visualização":
    ##################### PÁGINA CLIENTE VIEWER ####################################################

    st.title("Visualização da Temperatura")
    st.header("Monitoramento em Tempo Real")

    # Encontrar o dispositivo A1-AI-TIT01
    dispositivo = next(
        (d for d in dispositivos_criados if d.tag == "A1-AI-TIT01"), None
    )

    if dispositivo and isinstance(dispositivo, AIDevicePublisher):
        current_value = f"{dispositivo.value} {dispositivo.unit}"

        # Exibir a temperatura usando classes CSS do styles.css
        st.markdown(
            f"""
            <div class="temperature-container">
                <div class="temperature-card">
                    <h2 class="temperature-tag">{dispositivo.tag}</h2>
                    <p class="temperature-label">Temperatura Atual:</p>
                    <h1 class="temperature-value">{current_value}</h1>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Dispositivo A1-AI-TIT01 não encontrado.")

else:
    st.error("Página não encontrada.")


if __name__ == "__main__":
    pass

##################### FIM DE PROGRAMA ####################################################

import streamlit as st

st.set_page_config(page_title="RVS PERÍCIAS", layout="centered")

# Definindo cores-base
BACKGROUND_COLOR = "#121212"
PANEL_COLOR = "#1E1E1E"
GOLD_COLOR = "#FFC600"
GOLD_GRADIENT = "linear-gradient(90deg, #FFC600, #A68000)"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT_COLOR = "#D3D3D3"

# Aplicando CSS
st.write(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        /* Configurações Globais */
        * {{
            font-family: 'Poppins', sans-serif;
        }}
        body {{
            background-color: {BACKGROUND_COLOR};
        }}

        .block-container {{
            background-color: {PANEL_COLOR};
            padding: 20px 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.4);
        }}

        /* Títulos principais */
        .title {{
            color: {GOLD_COLOR};
            font-size: 24px;
            font-weight: 700;
            text-align: center;
            margin-top: 20px;
        }}
        .subtitle {{
            color: {SECONDARY_TEXT_COLOR};
            font-size: 18px;
            text-align: center;
        }}

        /* Botões */
        .stButton>button {{
            background: {GOLD_GRADIENT};
            color: {TEXT_COLOR};
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background: #FFD465;
            color: black;
        }}

        /* Campos de Entrada */
        .stTextInput>div>div>input, .stNumberInput>div>div>input {{
            background-color: {PANEL_COLOR};
            color: {TEXT_COLOR};
            border: 1.5px solid {GOLD_COLOR}80;
            border-radius: 8px;
            padding: 8px;
        }}
        .stCheckbox>label>div:first-child {{
            border-color: {GOLD_COLOR} !important;
            background-color: {PANEL_COLOR};
        }}
        .stCheckbox>label>div:first-child:hover {{
            border-color: {GOLD_COLOR} !important;
        }}
    </style>
""", unsafe_allow_html=True)

# Layout
st.markdown("<h1 class='title'>RVS PERÍCIAS</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Verificador de Jornada de Trabalho</h2>", unsafe_allow_html=True)
st.write("---")

# Campos para entrada
st.subheader("PDF da Contagem:")
pdf_file = st.file_uploader("Procurar arquivo", type="pdf")

st.subheader("Limite de horas:")
limit_hours = st.number_input("Limite de horas:", min_value=0.0, max_value=24.0, value=17.0, step=0.25)

check_identical = st.checkbox("Verificar horários idênticos")

# Botão principal
st.write(" ")
if st.button("EXECUTAR ANÁLISE"):
    st.success("Análise concluída.")

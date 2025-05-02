import streamlit as st

st.set_page_config(page_title="RVS PERÍCIAS", layout="centered")

# Definindo cores-base
BACKGROUND_COLOR = "#121212"
PANEL_COLOR = "#1E1E1E"
GOLD_COLOR = "#FFC600"
SILVER_COLOR = "#C0C0C0"
WHITE_COLOR = "#FFFFFF"
TEXT_COLOR = "#A0A0A0"

GOLD_GRADIENT = "linear-gradient(90deg, #FFC600, #A68000)"
BUTTON_GRADIENT = f"linear-gradient(90deg, #FFC600, {SILVER_COLOR})"

# CSS personalizado
st.write(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        /* Layout principal */
        * {{
            font-family: 'Poppins', sans-serif;
        }}
        body {{
            background-color: {BACKGROUND_COLOR};
        }}
        .block-container {{
            background-color: {PANEL_COLOR};
            padding: 40px 30px; /* Aumentando o espaçamento interno */
            border-radius: 16px 16px 0 0; /* Bordas arredondadas superiores */
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.4);
        }}

        /* Logo */
        .logo-center {{
            display: flex; 
            justify-content: center; 
            align-items: center; 
            margin-top: 40px; /* Espaçamento antes do logo */
            margin-bottom: 20px; /* Espaçamento após o logo */
        }}

        /* Títulos */
        h1.title {{
            color: {WHITE_COLOR};
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            margin-top: 10px;
        }}
        h2.subtitle {{
            color: {TEXT_COLOR};
            font-size: 18px;
            text-align: center;
            margin-bottom: 24px;
        }}

        /* Subtítulos das seções */
        h4 {{
            color: {TEXT_COLOR};
        }}

        /* Botões */
        .stButton>button {{
            background: {BUTTON_GRADIENT};
            color: {WHITE_COLOR};
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        }}
        .stButton>button:hover {{
            background: linear-gradient(90deg, #FFD700, {GOLD_COLOR});
            color: black;
            box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.4);
        }}

        /* Campos de entrada */
        .stTextInput>div>div>input, .stNumberInput>div>div>input {{
            background-color: {PANEL_COLOR};
            color: {WHITE_COLOR};
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
        .stCheckbox>label {{
            color: {TEXT_COLOR};
        }}

        /* File uploader */
        [data-testid="stFileUploader"] {{
            background-color: {PANEL_COLOR};
            color: {TEXT_COLOR};
            border: 1px solid {GOLD_COLOR}80;
            border-radius: 10px;
            padding: 10px;
        }}

        /* Estilo dos títulos dos inputs */
        .stNumberInput>label, .stTextInput>label, [data-testid="stFileUploaderLabel"]>div {{
            color: {TEXT_COLOR};
            font-weight: 600;
        }}
    </style>
""", unsafe_allow_html=True)

# Logo centralizada
st.markdown("""
    <div class='logo-center'>
        <img src='https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png' 
        alt='Logo RVS' width='130'/>
    </div>
""", unsafe_allow_html=True)

# Títulos
st.markdown("<h1 class='title'>RVS PERÍCIAS</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Verificador de Jornada de Trabalho</h2>", unsafe_allow_html=True)

# Linha divisória
st.write("---")

# Campos de entrada: PDF File
st.subheader("PDF da Contagem:")
pdf_file = st.file_uploader("Procurar Arquivo", type="pdf")

# Campo de número: Limite de horas
st.subheader("Limite de horas:")
limit_hours = st.number_input("Limite de horas:", min_value=0.0, max_value=24.0, value=17.0, step=0.25)

# Checkbox
check_identical = st.checkbox("Verificar horários idênticos", value=True)

# Botão principal
st.write(" ")
if st.button("EXECUTAR ANÁLISE"):
    st.success("Análise concluída.")

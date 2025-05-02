import streamlit as st

st.set_page_config(page_title="RVS PERÍCIAS", layout="centered")
# Cores institucionais
GOLD = "#FFC600"
SILVER = "#c0c0c0"
DARK = "#121212"
SILVER_BG = "#222428"

# CSS
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        html, body, [class*="css"], .stApp {{
            font-family: 'Poppins', sans-serif !important;
            background: {DARK};
        }}
        .main .block-container {{
            background: {SILVER_BG};
            border-radius: 32px 32px 16px 16px;
            box-shadow: 0 6px 32px rgba(50,50,50,0.50);
            margin-top: 30px;
            max-width: 520px;
            min-width: 320px;
        }}

        /* Logo */
        .logo-section {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 55px;
            margin-bottom: 16px;
        }}
        .logo-section img {{
            width: 160px;
        }}

        /* Alvos visuais via círculo simples */
        .target {{
            display: inline-block;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border: 2.5px solid {SILVER};
            margin-right: 10px;
            background: rgba(255,255,255,0.03);
            box-shadow: 0 0 12px {GOLD}80, 0 0 2px {SILVER}CC;
            position: relative;
            top: 6px;
        }}
        /* Prata destacado e glow */
        .silver-label {{
            color: {SILVER};
            font-weight: 600;
            font-size: 1.16rem;
            text-shadow: 0 3px 12px #000, 0 0px 12px {SILVER}78, 0 0 8px #fff6;
            letter-spacing: 0.02em;
            margin-bottom:0.38em;
        }}
        .input-label {{
            margin-top:1.7em;
            margin-bottom:0.4em;
            display:flex;
            align-items:center;
            gap:0.18em;
        }}

        /* Checkbox custom checkmark verde */
        section[data-testid="stCheckbox"] label {{
            color: {SILVER};
            font-size:1.16rem !important;
            font-weight: 600;
            text-shadow: 0 2px 8px #000d, 0 0 10px #9ff36f55;
        }}
        section[data-testid="stCheckbox"] > div:first-child {{
            display: flex; align-items: center;
            margin-top:0.2em;
        }}
        input[type="checkbox"]:checked + div > svg {{
            stroke: #1ff96a !important;
            filter: drop-shadow(0 0 6px #1ff96aaa);
        }}

        /* Input fields */
        .stNumberInput>div>div>input, .stTextInput>div>div>input {{
            background: #232527 !important;
            color: {SILVER};
            border: 1.8px solid {GOLD}BB !important;
            border-radius: 9px !important;
            font-size: 1.13em !important;
        }}

        /* File uploader */
        [data-testid="stFileUploader"] {{
            background: #191a1bCC;
            border: 1.4px solid {SILVER}90;
            border-radius: 10px;
            color: {SILVER};
        }}

        /* Botão bonito */
        .stButton>button {{
            background: linear-gradient(93deg, {SILVER} 12%, {GOLD} 100%);
            color: #242526;
            font-weight: 700;
            letter-spacing:0.09em;
            font-size: 1.13em;
            border: none;
            border-radius: 14px;
            box-shadow: 0 4px 24px {GOLD}30, 0 2px 2px #fff3;
            padding: 0.55em 1.9em;
            margin-top: 25px;
            transition: box-shadow 0.2s,background 0.15s;
        }}
        .stButton>button:hover {{
            background: linear-gradient(85deg,#fff, {SILVER} 40%, {GOLD} 98%);
            color: #151515;
            box-shadow: 0 4px 32px {SILVER}99, 0 2px 12px {GOLD}BB;
        }}
    </style>
""", unsafe_allow_html=True)

# Logo centralizada - agora com a imagem de fundo (NOVA)
st.markdown("""
<div class='logo-section'>
    <img src='https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/fundo_rvs.png' alt='Logo RVS'/>
</div>
""", unsafe_allow_html=True)

# Label: PDF da contagem
st.markdown(
    "<div class='input-label'><span class='target'></span><span class='silver-label'>PDF da Contagem:</span></div>",
    unsafe_allow_html=True
)
pdf_file = st.file_uploader("Procurar Arquivo", type="pdf", label_visibility="collapsed")

# Label: Limite de horas
st.markdown(
    "<div class='input-label'><span class='target'></span><span class='silver-label'>Limite de horas:</span></div>",
    unsafe_allow_html=True
)
limit_hours = st.number_input("", min_value=0.0, max_value=24.0, value=17.0, step=0.25)

# Label: Checkbox verde
st.markdown(
    "<div class='input-label'><span class='target'></span><span class='silver-label'>Verificar horários idênticos</span></div>",
    unsafe_allow_html=True
)
check_identical = st.checkbox(" ", value=True)

# Botão
if st.button("EXECUTAR ANÁLISE"):
    st.success("Análise concluída.")

st.markdown("<br><br>", unsafe_allow_html=True)

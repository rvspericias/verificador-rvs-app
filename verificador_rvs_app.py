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

        /* Logo centralizada */
        .logo-section {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 55px;
            margin-bottom: 16px;
        }}
        .logo-section img {{
            width: 180px; /* Ajuste para o tamanho desejado */
        }}

        /* Alvos prateados */
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
        /* Labels prateadas com destaque */
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

        /* Checkbox customizado com check verde */
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

        /* Inputs */
        .stNumberInput>div>div>input, .stTextInput>div>div>input {{
            background: #232527 !important;
            color: {SILVER};
            border: 1.8px solid {GOLD}BB !important;
            border-radius: 9px !important;
            font-size: 1.13em !important;
        }}

        /* Botão estilizado */
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
            transition: box-shadow 0.2s, background 0.15s;
        }}
        .stButton>button:hover {{
            background: linear-gradient(85deg,#fff, {SILVER} 40%, {GOLD} 98%);
            color: #151515;
            box-shadow: 0 4px 32px {SILVER}99, 0 2px 12px {GOLD}BB;
        }}
    </style>
""", unsafe_allow_html=True)

# Adicionando a nova logo
st.markdown("""
<div class='logo-section'>
    <img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAYAAAB4snr3AAAAAXNSR0IArs4c6QAAAARzQklUCAgICHwIZIgAAAcYSURBVHic7d3dd5RFFMdxfbRCjDRQmAh5xJACklVrsKWWzrpcNWlCsppqJpQFp3oljCgoRCNiCJHAN0BQkdFLrsUKkskoBiQYYOkogJxdVxxT3bRDnuv+63s+SUMw3Ob3YPukYwzMyW/NZ5pgBAgsAAAAAAAAAYIbseddnQzPKQwPg6mOF47JXjp3IpY4XjMFc1no5XONZOXHhXF1umOV43fyoljsuXFHsno5XLrjXF09ocm4AAAAAAAAAAGCDQ38egAAAAAAAAAAQKoHhnFD89U486M8cw9443NDTh05U6MGcdOZNzRWMeekmYuMAAAAAAAAAAOAHDX/xPzs366OVT1czjtkj+dFeR73BQAAAAAAAAA2GIZxrzoWzTkiY56SZtzWGYbzrTYsnVoAAAAAAAAAYI9HjEAAAAAAAAAAGGSqvsAAAAAAAAAAGCQKwAAAAAAAAAA2FIlgAAAAAAAAAAWELbAAAAAAAAAAA2FInaAb/DA88A18wxrjGj%2BM+I53yKPRxgAAAAAAAAAAOB16PN57Y58AAAAAAAAAAA4PUwwPggAAAAAAAAAADhH3h/AgAAAAAAAAAADghYPwgAAAAAAAAAAThF3R%2FAAAAAAAAAAA4IWg%2BCEAAAAAAAAAADgFaD8IAAAAAAAAAAAOI1g/CAAAAAAAAAAE4Zd0fwAAAAAAAAAADhhaD4IQAAAAAAAAAAOAVoPwgAAAAAAAAADiNYPwgAAAAAAAAABOEXdH8AAAAAAAAAADghaD4IQAAAAAAAAAA4BWg/CAAAAAAAAAAOI1g/CAAAAAAAAAAE4Zd0fwAAAAAAAAAADhhaD4IQAAAAAAAAAA4BWg/CAAAAAAAAAAOI1g/CAAAAAAAAAAE4Zd0fwAAAAAAAAAADhhaD4IQAAAAAAAAAA4BWg/CAAAAAAAAAAOI1g/CAAAAAAAAAAE4Zd0fwAAAAAAAAAADhhaD4IQAAAAAAAAAA4BWg/CAAAAAAAAAAOI1g/CAAAAAAAAAAE4Zd12Aj+kr4dHbdCAOU/oAAAAAElFTkSuQmCC' alt='Logo RVS'/>
</div>
""", unsafe_allow_html=True)

# Campo: PDF da Contagem
st.markdown("<div class='input-label'><span class='target'></span><span class='silver-label'>PDF da Contagem:</span></div>", unsafe_allow_html=True)
pdf_file = st.file_uploader("Procurar Arquivo", type="pdf", label_visibility="collapsed")

# Campo: Limite de horas
st.markdown("<div class='input-label'><span class='target'></span><span class='silver-label'>Limite de horas:</span></div>", unsafe_allow_html=True)
limit_hours = st.number_input("", min_value=0.0, max_value=24.0, value=17.0, step=0.25)

# Checkbox - Verificar horários idênticos
st.markdown("<div class='input-label'><span class='target'></span><span class='silver-label'>Verificar horários idênticos</span></div>", unsafe_allow_html=True)
check_identical = st.checkbox("", value=True)

# Botão de análise
if st.button("EXECUTAR ANÁLISE"):
    st.success("Análise concluída.")

import streamlit as st
import pdfplumber
import re
from io import BytesIO
from datetime import datetime

# Configuração inicial
st.set_page_config(
    page_title="Verificador RVS",
    page_icon="https://raw.githubusercontent.com/carlosrvs/verificador-rvs-app/main/logo-min-flat.png",
    layout="centered"
)

st.markdown("""
<style>
    body, [class*="css"], .stApp {
        font-family: 'Roboto', sans-serif !important;
        background-color: #21242B !important;
        color: #f5f5f5 !important;
    }
    img[src*="logo-min-flat.png"] {
        border-radius: 0 !important;
    }
    .stButton>button {
        background-color: #d4af37;
        color: #21242B;
        font-weight: 700;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        font-size: 19px;
        box-shadow: 0 2px 10px #0003;
    }
    .stButton>button:hover {
        background-color: #edc84c;
    }
    section[data-testid="stCheckbox"] svg {
        stroke: #27d154 !important;
        fill: #27d154 !important;
        filter: drop-shadow(0 0 3px #27d15488);
    }
    section[data-testid="stCheckbox"]:hover svg {
        stroke: #39ef74 !important;
        fill: #39ef74 !important;
    }

    /* === Estilização para Título === */
    .header-gold {
        color: #d4af37 !important;
        font-weight: 900;
        font-size: 2.4rem !important;
        margin-top: 1em;
        margin-bottom: 0.8em;
        text-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
    }

    /* === Blocos de Resultados === */
    .result-box {
        background: #fff8dc;
        color: #333333;
        padding: 10px 18px;
        border-radius: 12px;
        border-left: 8px solid #d4af37;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        font-size: 15px;
    }
    .result-box.none {
        background: #eaf4ff;
        color: #163a67;
        border-left: 8px solid #468cfb;
    }

    /* === Estilização das Labels (NumberInput, FileUploader e Checkbox) === */
    div[data-testid="stNumberInput"] > label,
    div[data-testid="stFileUploader"] > label {
        color: #d4af37 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-shadow: 0 1px 6px rgba(0, 0, 0, 0.6);
    }

    /* Estilização Específica para o Texto do st.checkbox */
    div[data-baseweb="checkbox"] > label > span {
        color: #d4af37 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-shadow: 0 1px 6px rgba(0, 0, 0, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Elementos visuais da interface
st.image("https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png", width=110)
st.markdown("""
<h1>Verificador <span style='color:#d4af37;'>RVS</span></h1>
<p>Automatize a conferência de jornadas com base nos arquivos PDF de contagem</p>
""", unsafe_allow_html=True)

# Widgets interativos
limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25)
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos", value=True)
uploaded_file = st.file_uploader("Envie o PDF da contagem", type=["pdf"])

# Processamento do PDF (se fornecido pelo usuário)
if uploaded_file:
    dias_excedidos = []
    registros_iguais = []
    ultima_data = None

    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for page in pdf.pages:
            texto = page.extract_text() or ""
            linhas = texto.split('\n')
            datas = [datetime.strptime(data, '%d/%m/%y') for linha in linhas for data in re.findall(r'\d{2}/\d{2}/\d{2}', linha)]
            if datas:
                ultima_data = max(datas)
            for linha in linhas:
                if re.match(r'^\d{2}/\d{2}/\d{2}', linha):
                    data_str = linha[:8]
                    horarios = re.findall(r'\d{2}:\d{2}', linha)
                    if not horarios or len(horarios) < 2:
                        continue
                    valores = re.findall(r'\d+,\d+', linha)
                    try:
                        a01 = float(valores[0].replace(",", "."))
                        if a01 > limite:
                            dias_excedidos.append((data_str, a01))
                    except:
                        pass
                    if verificar_identicos:
                        pares = list(zip(horarios[::2], horarios[1::2]))
                        registros_iguais += [(data_str, f"{e} - {s}") for e, s in pares if e == s]

    # Exibir resultados
    st.markdown('<div class="header-gold">Resultado da Verificação</div>', unsafe_allow_html=True)
    if dias_excedidos:
        for d in dias_excedidos:
            st.markdown(f"<div class='result-box'><strong>{d[0]}</strong> | {d[1]}h</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='result-box none'>Nenhum dia excedeu o limite de horas.</div>", unsafe_allow_html=True)

    if verificar_identicos:
        if registros_iguais:
            for r in registros_iguais:
                st.markdown(f"<div class='result-box'><strong>{r[0]}</strong> | {r[1]}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-box none'>Nenhum registro idêntico encontrado.</div>", unsafe_allow_html=True)

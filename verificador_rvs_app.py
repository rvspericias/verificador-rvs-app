import streamlit as st
import pdfplumber
import re
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="Verificador RVS",
    page_icon="https://raw.githubusercontent.com/carlosrvs/verificador-rvs-app/main/logo-min-flat.png",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Roboto', sans-serif;
        background-color: #21242B !important; /* chumbo chic */
        color: #f5f5f5 !important;
    }
    .stApp {
        background-color: #21242B !important;
    }
    .stButton>button {
        background-color: #d4af37;
        color: #21242B;
        font-weight: 700;
        border: none;
        padding: 0.65em 1.3em;
        border-radius: 9px;
        font-size: 19px;
        transition: 0.3s;
        box-shadow: 0 2px 12px #0004;
    }
    .stButton>button:hover {
        background-color: #edc84c;
    }

    section[data-testid="stFileUploader"] {
        background: #232528 !important;
        border: 1.5px solid #353945;
        border-radius: 10px;
        color: #f3f3fa !important;
    }

    /* Inputs harmonizados */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1a1d23 !important;
        color: #e1eaf0 !important;
        border: 1.6px solid #d4af378c !important;
        border-radius: 8px !important;
        font-size: 17px !important;
        padding: 7px 11px;
    }
    .stMarkdown h1, h1 {
        color: #fafaff !important;
        font-weight: 900;
        font-size: 2.4rem !important;
        text-shadow: 0 2px 16px #000c, 0 1px 6px #d4af3785;
        letter-spacing: 0.02em;
        margin-bottom: 0.18em;
    }
    .stMarkdown h2, h2, .stSubheader {
        color: #e6e6f8 !important;
        font-weight: 800;
        font-size: 1.3rem !important;
        text-shadow: 0 1px 9px #000c, 0 1px 8px #d4af3755;
        margin-bottom: 0.16em !important;
    }
    .stMarkdown h4, h4, label, .stFileUploader label {
        color: #f6efe8 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-top: 7px !important;
    }
    .stMarkdown p, p, .stMarkdown span, .stMarkdown strong,
    .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
        color: #e2e6eb !important;
        font-size: 18px !important;
    }
    .stCheckbox label, .stCheckbox label span {
        font-size: 17px !important;
        color: #e1f7da !important;
        font-weight: 600;
        letter-spacing: 0.013em;
    }
    section[data-testid="stCheckbox"] svg {
        stroke: #27d154 !important;
        filter: drop-shadow(0 0 3px #27d15488);
    }
    /* Blocos de resultado adaptados ao fundo escuro */
    .result-block {
        background: #23283a;
        padding: 12px 13px;
        border-left: 6px solid #d4af37;
        border-radius: 7px;
        color: #fffbea;
        margin-bottom: 10px;
        font-size: 17px;
        box-shadow: 0 1px 12px #0003;
    }
    .result-block.ok {
        border-left-color: #27d154;
        background: #202e24;
        color: #c2ffd4;
    }
    .result-block.none {
        border-left-color: #468cfb;
        background: #1a2431;
        color: #e8f0fe;
    }
    .result-block.grey {
        border-left-color: #aaaaaa;
        background: #26272c;
        color: #ecf0f3;
    }
</style>
""", unsafe_allow_html=True)

st.image("https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png", width=100)

st.markdown("""
<h1>Verificador <span style='color:#d4af37;'>RVS</span></h1>
<p>Automatize a conferência de jornadas com base nos arquivos PDF de contagem</p>
""", unsafe_allow_html=True)

# Dicionário de meses em português
MESES_PT = {
    1: 'JANEIRO', 2: 'FEVEREIRO', 3: 'MARÇO', 4: 'ABRIL',
    5: 'MAIO', 6: 'JUNHO', 7: 'JULHO', 8: 'AGOSTO',
    9: 'SETEMBRO', 10: 'OUTUBRO', 11: 'NOVEMBRO', 12: 'DEZEMBRO'
}

limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25, format="%0.2f")
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos", value=True)

with st.container():
    st.markdown("""
    <h4>📎 Upload do Arquivo</h4>
    <p>Selecione o arquivo PDF da contagem de horas para verificar os registros.</p>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Envie o PDF da contagem de horas", type=["pdf"])

if uploaded_file:
    dias_excedidos = []
    registros_iguais = []

    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for i, page in enumerate(pdf.pages):
            texto = page.extract_text()
            if not texto:
                continue

            linhas = texto.split('\n')
            datas = [re.findall(r'(\d{2}/\d{2}/\d{4})', linha) for linha in linhas if re.search(r'\d{2}/\d{2}/\d{4}', linha)]
            datas = [item for sublist in datas for item in sublist]

            try:
                data_final = max(datetime.strptime(d, '%d/%m/%Y') for d in datas)
                mes_ref = f"{MESES_PT[data_final.month]}/{data_final.year}"
            except:
                mes_ref = "Mês Desconhecido"

            for linha in linhas:
                if re.match(r'^\d{2}/\d{2}/\d{2}', linha):
                    horarios = re.findall(r'\d{2}:\d{2}', linha)
                    if not horarios or len(horarios) < 2:
                        continue
                    valores = re.findall(r'\d+,\d+', linha)
                    try:
                        a01 = float(valores[0].replace(",", "."))
                        if a01 > limite:
                            dias_excedidos.append((linha[:8], a01, mes_ref, i+1))
                    except:
                        pass

                    if verificar_identicos:
                        pares = list(zip(horarios[::2], horarios[1::2]))
                        for ent, sai in pares:
                            if ent == sai:
                                registros_iguais.append((linha[:8], f"{ent} - {sai}", mes_ref, i+1))

    st.markdown("---")
    st.subheader("Resultado da Verificação")

    if dias_excedidos:
        st.write("### Dias com mais horas que o limite:")
        for d in dias_excedidos:
            st.markdown(
                f"<div class='result-block'><strong>{d[0]}</strong> | {d[1]} | {d[2]} | Página {d[3]}</div>",
                unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='result-block ok'><strong>Nenhum dia excedeu o limite de horas.</strong></div>",
            unsafe_allow_html=True)

    if verificar_identicos:
        if registros_iguais:
            st.write("### Registros com entrada/saída idênticos:")
            for r in registros_iguais:
                st.markdown(
                    f"<div class='result-block grey'><strong>{r[0]}</strong> | {r[1]} | {r[2]} | Página {r[3]}</div>",
                    unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='result-block none'>Nenhum registro idêntico encontrado.</div>",
                unsafe_allow_html=True)

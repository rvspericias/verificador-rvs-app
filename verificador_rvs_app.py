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

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background-color: #23272B !important;
        color: #f1f1f1 !important;
    }

    /* Checkbox Check verde */
    section[data-testid="stCheckbox"] svg {
        stroke: #27d154 !important;
        filter: drop-shadow(0 0 3px #27d154cc);
    }
    section[data-testid="stCheckbox"]:hover svg {
        stroke: #39ef74 !important;
        filter: drop-shadow(0 0 6px #39ef74cc);
    }

    .stButton>button {
        background-color: #d4af37;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.6em 1.15em;
        border-radius: 9px;
        font-size: 19px;
        transition: 0.3s;
        box-shadow: 0 2px 12px #0002;
    }

    .stButton>button:hover {
        background-color: #c49d2e;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', sans-serif;
        color: #f1f1f1 !important;
        font-weight: 700;
        margin-bottom: 0.4em;
    }
    h1 { font-size: 36px; }
    h2 { font-size: 27px; }
    h3 { font-size: 21px; }
    .stSubheader, .stMarkdown p, .stMarkdown strong, .stMarkdown span {
        font-size: 18px !important;
        color: #e0e0e0 !important;
        font-family: 'Roboto', sans-serif;
    }
    label, .stTextInput label, .stNumberInput label, .stFileUploader label {
        font-size: 17px !important;
        color: #d2d2d2 !important;
    }
    /* Painel dos resultados ajustado */
    .result-block {
        background: #343a40;
        padding: 12px 13px;
        border-left: 6px solid #d4af37;
        border-radius: 7px;
        color: #fffbea;
        margin-bottom: 10px;
        font-size: 17px;
    }
    .result-block.ok {
        border-left-color: #27d154;
        background: #273c2e;
        color: #e6f4ea;
    }
    .result-block.none {
        border-left-color: #468cfb;
        background: #222f3a;
        color: #e8f0fe;
    }
    .result-block.grey {
        border-left-color: #aaaaaa;
        background: #393939;
        color: #f3f3f3;
    }
</style>
""", unsafe_allow_html=True)

st.image("https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png", width=100)

st.markdown("""
<h1 style='font-family: Roboto'>Verificador <span style='color:#d4af37;'>RVS</span></h1>
<p style='font-family: Roboto; font-size: 20px; color: #cccccc; margin-top: 0;'>Automatize a conferência de jornadas com base nos arquivos PDF de contagem</p>
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
    <h4 style='font-family: Roboto; color: #ededed; font-size:19px;'>📎 Upload do Arquivo</h4>
    <p style='color: #bcbcbc; font-size:17px;'>Selecione o arquivo PDF da contagem de horas para verificar os registros.</p>
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

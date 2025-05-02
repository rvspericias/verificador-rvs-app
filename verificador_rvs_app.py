import streamlit as st
import pdfplumber
import re
from datetime import datetime
from io import BytesIO

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
    .stButton>button {
        background-color: #d4af37;
        color: #21242B;
        font-weight: bold;
        border-radius: 10px;
        font-size: 19px;
    }
    .result-box {
        padding: 10px 18px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        font-size: 15px;
        line-height: 1.4;
    }
    .exceeded {
        background: #fff8dc;
        color: #333333;
        border-left: 8px solid #d4af37;
    }
    .identical {
        background: #eaf4ff;
        color: #163a67;
        border-left: 8px solid #468cfb;
    }
    .subtitle {
        font-size: 1.2rem;
        font-weight: bold;
        color: #d4af37;
        margin-top: 1.2em;
    }
    .result-header {
        color: #d4af37 !important;
        font-size: 2rem;
        font-weight: bold;
        margin-top: 1.2em;
        margin-bottom: 0.6em;
    }
    div[data-testid="stNumberInput"] > label,
    div[data-testid="stFileUploader"] > label {
        color: #d4af37 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        text-shadow: 0 1px 6px rgba(0, 0, 0, 0.6);
    }
</style>
""", unsafe_allow_html=True)

st.image("https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png", width=110)
st.markdown("""
<h1 style='color: #ffffff;'>Verificador <span style="color: #d4af37;">RVS</span></h1>
<p>Automatize a conferência de jornadas com base nos arquivos PDF de contagem.</p>
""", unsafe_allow_html=True)

# Mapeamento de meses (inglês para português)
MES_EXTENSO = {
    "01": "JANEIRO", "02": "FEVEREIRO", "03": "MARÇO",
    "04": "ABRIL", "05": "MAIO", "06": "JUNHO",
    "07": "JULHO", "08": "AGOSTO", "09": "SETEMBRO",
    "10": "OUTUBRO", "11": "NOVEMBRO", "12": "DEZEMBRO"
}

limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25)
uploaded_file = st.file_uploader("Envie o PDF da contagem", type=["pdf"])

if uploaded_file:
    dias_excedidos = []
    registros_iguais = []

    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text() or ""
            linhas = texto.split('\n')
            for linha in linhas:
                if re.match(r'^\d{2}/\d{2}/\d{2}', linha):
                    data_str = linha[:8]
                    horarios = re.findall(r'\d{2}:\d{2}', linha)
                    if len(horarios) < 2:
                        continue
                    valores = re.findall(r'\d+,\d+', linha)
                    a01 = float(valores[0].replace(",", ".")) if valores else 0
                    if a01 > limite:
                        dias_excedidos.append((data_str, a01, page_num))
                    # Verificar registros idênticos
                    pares = list(zip(horarios[::2], horarios[1::2]))
                    for entrada, saida in pares:
                        if entrada == saida:
                            registros_iguais.append((data_str, f"{entrada} - {saida}"))

    st.markdown('<h2 class="result-header">Resultado da Verificação</h2>', unsafe_allow_html=True)

    st.markdown('<h3 class="subtitle">Dias com mais horas que o limite:</h3>', unsafe_allow_html=True)

    if dias_excedidos:
        for data, horas, pagina in dias_excedidos:
            # Extrair o mês/ano
            dia, mes, ano = data.split('/')
            mes_extenso = MES_EXTENSO[mes]
            st.markdown(
                f"<div class='result-box exceeded'><strong>{data}</strong> | {horas:.2f} horas | {mes_extenso}/{2000+int(ano)} | Página {pagina} do PDF</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='result-box exceeded'>Nenhum dia excedeu o limite de horas.</div>",
            unsafe_allow_html=True
        )

    st.markdown('<h3 class="subtitle">Registros de entrada/saída idênticos:</h3>', unsafe_allow_html=True)

    if registros_iguais:
        for data, registro in registros_iguais:
            st.markdown(
                f"<div class='result-box identical'><strong>{data}</strong> | {registro}</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='result-box identical'>Nenhum registro idêntico encontrado.</div>",
            unsafe_allow_html=True
        )

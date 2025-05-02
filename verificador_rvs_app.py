import streamlit as st
import pdfplumber
import re
from io import BytesIO
from datetime import datetime
from locale import setlocale, LC_TIME

# Define o idioma como português do Brasil
setlocale(LC_TIME, 'pt_BR.utf8')

st.set_page_config(
    page_title="Verificador RVS",
    page_icon="https://raw.githubusercontent.com/carlosrvs/verificador-rvs-app/main/logo-min-flat.png",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

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

    /* ===== Título da Verificação ===== */
    .header-gold {
        color: #d4af37 !important;
        font-weight: 900;
        font-size: 2.4rem !important;
        margin-top: 1em;
        margin-bottom: 0.8em;
        text-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
        text-align: left;
    }

    /* ===== Caixa de Resultados ===== */
    .result-box {
        background: #fff8dc;
        color: #333333;
        padding: 10px 18px;
        border-radius: 12px;
        border-left: 8px solid #d4af37;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        font-size: 15px;
        line-height: 1.5;
    }

    /* ===== Caixa para Nenhum Registro Encontrado ===== */
    .result-box.none {
        background: #eaf4ff;
        color: #163a67;
        border-left: 8px solid #468cfb;
    }

    /* Subtítulos Menores */
    .subtitle-custom {
        font-size: 1.1rem !important;
        color: #e4e4e4 !important;
        margin-bottom: 0.8em;
    }
</style>
""", unsafe_allow_html=True)

st.image("https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png", width=110)

st.markdown("""
<h1>Verificador <span style='color:#d4af37;'>RVS</span></h1>
<p>Automatize a conferência de jornadas com base nos arquivos PDF de contagem</p>
""", unsafe_allow_html=True)

ABR_DIAS_PT = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]

def dia_da_semana(data_str):
    d = datetime.strptime(data_str, '%d/%m/%y')
    return ABR_DIAS_PT[d.weekday()]

limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25, format="%0.2f")
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos", value=True)

uploaded_file = st.file_uploader("Envie o PDF da contagem", type=["pdf"])

if uploaded_file:
    dias_excedidos = []
    registros_iguais = []
    ultima_data = None

    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for i, page in enumerate(pdf.pages):
            texto = page.extract_text() or ""
            linhas = texto.split('\n')
            # Captura todas as datas no formato dd/mm/aa
            datas = [datetime.strptime(data, '%d/%m/%y') for linha in linhas for data in re.findall(r'\d{2}/\d{2}/\d{2}', linha)]
            
            # Define a última data da página, se houver
            if datas:
                ultima_data = max(datas)

            for linha in linhas:
                if re.match(r'^\d{2}/\d{2}/\d{2}', linha):
                    data_str = linha[:8]
                    dia_semana = dia_da_semana(data_str)

                    horarios = re.findall(r'\d{2}:\d{2}', linha)
                    if not horarios or len(horarios) < 2:
                        continue

                    valores = re.findall(r'\d+,\d+', linha)
                    try:
                        a01 = float(valores[0].replace(",", "."))
                        if a01 > limite:
                            dias_excedidos.append((f"{data_str} {dia_semana}", a01, ultima_data, i+1))
                    except:
                        pass

                    if verificar_identicos:
                        pares = list(zip(horarios[::2], horarios[1::2]))
                        for entrada, saida in pares:
                            if entrada == saida:
                                registros_iguais.append((f"{data_str} {dia_semana}", f"{entrada} - {saida}", ultima_data, i+1))

    # Obtém o mês/ano com base na última data
    mes_extenso = ultima_data.strftime('%B').capitalize() if ultima_data else 'Mês desconhecido'
    ano_ref = ultima_data.year if ultima_data else '---'
    mes_referencia = f"{mes_extenso.upper()}/{ano_ref}"

    # Título da Verificação
    st.markdown('<div class="header-gold">Resultado da Verificação</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-custom">Dias com mais horas que o limite:</div>', unsafe_allow_html=True)

    # Exibição dos resultados em caixas
    if dias_excedidos:
        for d in dias_excedidos:
            st.markdown(
                f"<div class='result-box'><strong>{d[0]}</strong> | {d[1]:.2f}h | {mes_referencia} | Página {d[3]}</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='result-box none'>Nenhum dia excedeu o limite de horas.</div>",
            unsafe_allow_html=True
        )

    if verificar_identicos:
        if registros_iguais:
            st.markdown('<div class="subtitle-custom">Registros com entrada/saída idênticos:</div>', unsafe_allow_html=True)
            for r in registros_iguais:
                st.markdown(
                    f"<div class='result-box'><strong>{r[0]}</strong> | {r[1]} | {mes_referencia} | Página {r[3]}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                "<div class='result-box none'>Nenhum registro idêntico encontrado.</div>",
                unsafe_allow_html=True
            )

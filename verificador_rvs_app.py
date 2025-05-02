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

    body, [class*="css"], .stApp {
        font-family: 'Roboto', sans-serif !important;
        background-color: #21242B !important;
        color: #f5f5f5 !important;
    }
    /* Logo sem bordas arredondadas */
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
    /* Checkbox com check verde */
    section[data-testid="stCheckbox"] svg {
        stroke: #27d154 !important;
        filter: drop-shadow(0 0 3px #27d15488);
        fill: #27d154 !important;
    }
    section[data-testid="stCheckbox"]:hover svg {
        stroke: #39ef74 !important;
        filter: drop-shadow(0 0 6px #39ef74cc);
        fill: #39ef74 !important;
    }
    .stMarkdown h1 {
        color: #fafafa !important;
        font-size: 2.5rem;
        font-weight: 800;
    }
    .stMarkdown h2, h4 {
        color: #e4e4e4 !important;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .stMarkdown p, label {
        color: #c7c7c7 !important;
        font-size: 17px;
    }

    /* Resultados: Estilo clean com fundo claro */
    .result-block {
        background: #f7f7f8; /* Cinza bem claro */
        color: #21242B;
        padding: 12px 14px;
        box-shadow: 0 2px 8px #00000022;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 16px;
        border-left: 4px solid #d4af37; /* Dourado como indicador */
    }
    .result-block.ok {
        border-left: 4px solid #27d154; /* Verde elegante */
        color: #1b3c24; /* Verde escuro */
    }
    .result-block.none {
        border-left: 4px solid #468cfb; /* Azul discreto */
        background: #e8f1fc; /* Azul claro e leve */
        color: #163a67; /* Azul escuro */
    }
</style>
""", unsafe_allow_html=True)

# Exibe logo com as correções
st.image("https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png", width=110)

st.markdown("""
<h1>Verificador <span style='color:#d4af37;'>RVS</span></h1>
<p>Automatize a conferência de jornadas com base nos arquivos PDF de contagem</p>
""", unsafe_allow_html=True)

# Função/conversões
MESES_PT = {
    1: 'JANEIRO', 2: 'FEVEREIRO', 3: 'MARÇO', 4: 'ABRIL',
    5: 'MAIO', 6: 'JUNHO', 7: 'JULHO', 8: 'AGOSTO',
    9: 'SETEMBRO', 10: 'OUTUBRO', 11: 'NOVEMBRO', 12: 'DEZEMBRO'
}

limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25, format="%0.2f")
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos", value=True)

# Upload
with st.container():
    st.markdown("<h4>📎 Upload do Arquivo</h4><p>Envie o PDF abaixo para realizar a verificação.</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Envie o PDF da contagem de horas", type=["pdf"])

if uploaded_file:
    dias_excedidos = []
    registros_iguais = []

    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for i, page in enumerate(pdf.pages):
            texto = page.extract_text() or ""
            linhas = texto.split('\n')
            datas = [re.findall(r'(\d{2}/\d{2}/\d{4})', linha) for linha in linhas if re.search(r'\d{2}/\d{2}/\d{4}', linha)]
            datas = [item for sublist in datas for item in sublist]

            try:
                data_final = max(datetime.strptime(data, '%d/%m/%Y') for data in datas)
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
                            dias_excedidos.append((linha[:10], a01, mes_ref, i+1))
                    except:
                        pass

                    if verificar_identicos:
                        pares = list(zip(horarios[::2], horarios[1::2]))
                        for entrada, saida in pares:
                            if entrada == saida:
                                registros_iguais.append((linha[:10], f"{entrada} - {saida}", mes_ref, i+1))

    st.markdown("---")
    st.subheader("Resultado da Verificação")

    if dias_excedidos:
        st.write("### Dias com mais horas que o limite:")
        for d in dias_excedidos:
            st.markdown(
                f"<div class='result-block'><strong>{d[0]}</strong> | {d[1]} | {d[2]} | Página {d[3]}</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='result-block ok'><strong>Nenhum dia excedeu o limite de horas.</strong></div>",
            unsafe_allow_html=True
        )

    if verificar_identicos:
        if registros_iguais:
            st.write("### Registros com entrada/saída idênticos:")
            for r in registros_iguais:
                st.markdown(
                    f"<div class='result-block none'><strong>{r[0]}</strong> | {r[1]} | {r[2]} | Página {r[3]}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                "<div class='result-block none'>Nenhum registro idêntico encontrado.</div>",
                unsafe_allow_html=True
            )

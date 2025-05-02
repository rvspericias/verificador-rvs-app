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
        color: #d4af37 !important;  /* Cor dourada */
        font-weight: 900;
        font-size: 2.4rem !important;  /* Tamanho maior */
        margin-top: 1em;
        margin-bottom: 0.8em;  /* Espaçamento reduzido */
        text-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
        text-align: left;
    }

    /* ===== Caixa de Resultados ===== */
    .result-box {
        background: #fff8dc;  /* Tom de amarelo claro (bege) */
        color: #333333;
        padding: 10px 18px;  /* Espaçamento interno */
        border-radius: 12px;  /* Bordas arredondadas */
        border-left: 8px solid #d4af37;  /* Linha lateral dourada */
        margin-bottom: 10px;  /* Espaçamento inferior */
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Leve sombra para destacar */
        font-size: 15px;  /* Tamanho padrão da fonte */
        line-height: 1.5;
    }

    /* ===== Caixa para Nenhum Registro Encontrado ===== */
    .result-box.none {
        background: #eaf4ff;  /* Azul claro */
        color: #163a67;
        border-left: 8px solid #468cfb;  /* Linha lateral azul */
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

# Abreviações dos dias da semana em PT-BR
ABR_DIAS_PT = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]

# Função correta para data + sigla do dia em PT-BR
def dia_da_semana(data_str):
    d = datetime.strptime(data_str, '%d/%m/%y')
    return ABR_DIAS_PT[d.weekday()]

# Dicionário de meses em português
MESES_PT = {
    1: 'JANEIRO', 2: 'FEVEREIRO', 3: 'MARÇO', 4: 'ABRIL',
    5: 'MAIO', 6: 'JUNHO', 7: 'JULHO', 8: 'AGOSTO',
    9: 'SETEMBRO', 10: 'OUTUBRO', 11: 'NOVEMBRO', 12: 'DEZEMBRO'
}

# Entrada de dados
limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25, format="%0.2f")
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos", value=True)

# Upload do arquivo
uploaded_file = st.file_uploader("Envie o PDF da contagem", type=["pdf"])

if uploaded_file:
    dias_excedidos = []
    registros_iguais = []

    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for i, page in enumerate(pdf.pages):
            texto = page.extract_text() or ""
            linhas = texto.split('\n')
            datas = [re.findall(r'(\d{2}/\d{2}/\d{2})', linha) for linha in linhas if re.search(r'\d{2}/\d{2}/\d{2}', linha)]
            datas = [item for sublist in datas for item in sublist]

            try:
                data_final = max(datetime.strptime(data, '%d/%m/%Y') for data in datas)
                mes_ref = f"{MESES_PT[data_final.month]}/{data_final.year}"
            except:
                mes_ref = "Mês Desconhecido"

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
                            dias_excedidos.append((f"{data_str} {dia_semana}", a01, mes_ref, i+1))
                    except:
                        pass

                    if verificar_identicos:
                        pares = list(zip(horarios[::2], horarios[1::2]))
                        for entrada, saida in pares:
                            if entrada == saida:
                                registros_iguais.append((f"{data_str} {dia_semana}", f"{entrada} - {saida}", mes_ref, i+1))

    # Título da Verificação
    st.markdown('<div class="header-gold">Resultado da Verificação</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-custom">Dias com mais horas que o limite:</div>', unsafe_allow_html=True)

    # Exibição de resultados em caixas
    if dias_excedidos:
        for d in dias_excedidos:
            st.markdown(
                f"<div class='result-box'><strong>{d[0]}</strong> | {d[1]}h | {d[2]} | Página {d[3]}</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='result-box ok'><strong>Nenhum dia excedeu o limite de horas.</strong></div>",
            unsafe_allow_html=True
        )

    if verificar_identicos:
        if registros_iguais:
            st.markdown('<div class="subtitle-custom">Registros com entrada/saída idênticos:</div>', unsafe_allow_html=True)
            for r in registros_iguais:
                st.markdown(
                    f"<div class='result-box'><strong>{r[0]}</strong> | {r[1]} | {r[2]} | Página {r[3]}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                "<div class='result-box none'>Nenhum registro idêntico encontrado.</div>",
                unsafe_allow_html=True
            )

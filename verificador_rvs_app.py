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
    /* Checkbox com check VERDE */
    section[data-testid="stCheckbox"] svg {
        stroke: #27d154 !important; /* Deixe #27d154 para verde forte, ou troque por #4b9df9 para azul */
        fill: #27d154 !important; /* Troque por #4b9df9 para azul */
        /* Para azul descomente a linha abaixo e comente as linhas acima */
        /* stroke: #4b9df9 !important; fill: #4b9df9 !important; */
        filter: drop-shadow(0 0 3px #27d15488); /* Opcional: glow ao redor do check */
    }
    section[data-testid="stCheckbox"]:hover svg {
        stroke: #39ef74 !important; /* Ou #3ba1fa para azul-claro no hover */
        fill: #39ef74 !important;   /* Ou #3ba1fa para azul-claro no hover */
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
    /* Mira SVG ao topo dos resultados */
    .sniper-wrap {
        width:100%%; display:flex; justify-content: center; margin-bottom: 14px;
    }
    .sniper-svg {
        width: 62px; height: 62px; display: block;
        filter: drop-shadow(0 2px 7px #224a85a0);
    }

    /* Resultados: Estilo clean com fundo claro */
    .result-block {
        background: #f7f7f8;
        color: #21242B;
        padding: 12px 14px;
        box-shadow: 0 2px 8px #00000022;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 16px;
        border-left: 8px solid #d4af37;
    }
    .result-block.ok {
        border-left: 8px solid #27d154;
        color: #1b3c24;
    }
    .result-block.none {
        border-left: 8px solid #468cfb;
        background: #e8f1fc;
        color: #163a67;
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

limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25, format="%0.2f")
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos", value=True)

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

            import streamlit as st

            # Defina o seu CSS personalizado
            st.markdown("""
                <style>
                .header-gold {
                font-size: 24px;
                font-weight: bold;
                color: gold;
                text-align: center;
                margin-top: 10px;
            }
            .result-block {
            margin-top: 5px;  # Ajuste também outros margens, se necessário
            }
    </style>
""", unsafe_allow_html=True)

# Use a classe personalizada para o título
st.markdown('<div class="header-gold">Resultado da Verificação</div>', unsafe_allow_html=True)

if dias_excedidos:  # Corrigido para a indentação correta
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

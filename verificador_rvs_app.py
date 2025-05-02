import streamlit as st
import pdfplumber
import re
from io import BytesIO
from datetime import datetime
import calendar

st.set_page_config(
    page_title="Verificador RVS",
    page_icon="https://raw.githubusercontent.com/carlosrvs/verificador-rvs-app/main/logo-min-flat.png",
    layout="centered"
)

st.markdown("""
<style>
    /* ... (todo o CSS igual ao anterior, pode colar por cima) ... */
    .header-gold {
        color: #d4af37 !important;
        font-weight: 700;
        font-size: 1.5rem;
        margin-top: 1.5em;
        margin-bottom: 1em;
    }
    .result-block {
        background: #f7f7f8;
        color: #21242B;
        padding: 12px 14px;
        box-shadow: 0 2px 8px #0003;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 16px;
        border-left: 6px solid #d4af37;
    }
    .result-block.ok {
        border-left: 6px solid #27d154;
        color: #1b3c24;
    }
    .result-block.none {
        border-left: 6px solid #468cfb;
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

    st.markdown('<div class="header-gold">Resultado da Verificação</div>', unsafe_allow_html=True)

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

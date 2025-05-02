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

# CSS Global — usando st.write para evitar problemas de renderização
st.write(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif !important;
            background-color: #000 !important;
            color: #fff !important;
        }
        .appview-container, .main, .block-container {
            background: none !important;
        }
        .main > div:first-child, .block-container {
            background: #202228 !important;
            border-radius: 20px !important;
            box-shadow: 0 6px 60px 0 rgba(0,0,0,0.9), 0 1.5px 4px 0 #FFD70020;
            padding: 3em 2em 2em 2em !important;
            margin-top: 0.2em !important;
            min-width: 350px !important;
            max-width: 650px !important;
        }

        .rvs-main-title, .rvs-section-title {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: 1px;
        }
        .rvs-main-title {
            font-size: 2.2em;
            color: #FFD700 !important;
            text-shadow: 0 2px 12px #B7974C99, 0 1px 0 #fff;
            margin-bottom: 16px;
            margin-top: 10px;
        }
        .rvs-section-title {
            font-size: 1.35em;
            color: #fffbea !important;
            text-shadow: 0 1.5px 8px #FFD700CC, 0 1.5px 0 #36330099;
            margin-bottom: 10px;
            margin-top: 32px;
        }
        .divider-gold {
            width: 90px;
            height: 3px;
            border-radius: 2px;
            margin: 0.8em 0 1.6em 0;
            background: linear-gradient(90deg,#FFD700 45%,#B7974C 100%);
            box-shadow: 0 0 10px #613d0680;
        }
        p, label, .stNumberInput label {
            color: #bbb !important;
            font-size: 17px !important;
        }
        .stNumberInput label {
            font-weight: 500;
        }
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            background: #232323 !important;
            border: 1.5px solid #FFD70080 !important;
            color: #FFD700 !important;
            border-radius: 10px !important;
            font-size: 16px !important;
        }
        .stCheckbox>label > div:first-child {
            background: #FFD700 !important;
            border-color: #FFD700 !important;
        }
        .stFileUploader {
            background: #181818 !important;
            border-radius: 14px !important;
            border: 1.5px solid #FFD70080 !important;
            box-shadow: 0 0 14px 0 #FFD70033;
            color: #FFD700 !important;
            padding: 1.5em 1.25em !important;
            margin-bottom: 1em;
        }
        .stFileUploader label, .stFileUploader span {
            color: #fff !important;
            font-size: 16px !important;
        }
        .stButton>button {
            background: linear-gradient(90deg,#FFD700 40%,#B7974C 100%);
            color: #202228 !important;
            font-weight: 700 !important;
            border: none;
            padding: 0.5em 1.4em;
            border-radius: 10px;
            box-shadow: 0 2px 8px #FFD70025;
            font-size: 1em;
            letter-spacing: 1px;
            transition: all 0.25s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg,#FFE066,#FFD700 80%);
            color: #0e0e0e !important;
            box-shadow: 0 0 16px #FFD70088;
        }
        .rvs-card {
            background: linear-gradient(90deg,#232323 60%,#282511 100%);
            border-left: 7px solid #FFD700;
            color: #fff;
            padding: 1em 0.9em;
            margin-bottom: 12px;
            border-radius: 10px;
            font-size: 16px;
            box-shadow: 0 1px 12px #FFD7000D;
            display: flex;
            align-items: center;
        }
        .rvs-card strong {
            color: #FFD700;
            font-weight: 700;
        }
        .rvs-card.ok {
            background: #222;
            border-left: 7px solid #149a57;
            color: #bbf7c2;
        }
        .rvs-card.none {
            background: #181818;
            border-left: 7px solid #4285f4;
            color: #e7f0fd;
        }
        .rvs-card.grey {
            background: #212121;
            border-left: 7px solid #888;
            color: #ccc;
        }
        @media (max-width: 650px) {
            .main > div:first-child, .block-container { padding: 1.2em !important; }
            .rvs-main-title { font-size: 1.3em !important; }
            .divider-gold { width: 60px; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo centralizada, apenas glow dourado
st.markdown("""
<div style='display: flex; justify-content: center; margin-top: 32px; margin-bottom: 10px;'>
  <img 
    src='https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png' 
    width='112'
    style='filter: drop-shadow(0 8px 22px #FFD700BB) drop-shadow(0 0.5px 1.5px #FFF);'
    alt='Logo RVS'
  />
</div>
""", unsafe_allow_html=True)

# Título principal e divisor
st.markdown("<h1 class='rvs-main-title'>Verificador RVS</h1>", unsafe_allow_html=True)
st.markdown("<div class='divider-gold'></div>", unsafe_allow_html=True)
st.markdown(
    "<p style='margin-top: -1em; margin-bottom: 1.0em;font-size:21px;letter-spacing:0.02em;'>"
    "Automatize a conferência de jornadas com base nos arquivos PDF de contagem"
    "</p>",
    unsafe_allow_html=True
)

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
    <h4 style='color: #FFD700; font-weight: 600;'>📎 Upload do Arquivo</h4>
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

    st.markdown("<div class='divider-gold'></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='rvs-main-title'>Resultado da Verificação</h2>", unsafe_allow_html=True)

    if dias_excedidos:
        st.markdown("<h3 class='rvs-section-title'>Dias com mais horas que o limite:</h3>", unsafe_allow_html=True)
        for d in dias_excedidos:
            st.markdown(f"""
            <div class='rvs-card'>
                <strong>{d[0]}</strong> | {d[1]}h | {d[2]} | Página {d[3]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='rvs-card ok'>
            <strong>Nenhum dia excedeu o limite de horas.</strong>
        </div>
        """, unsafe_allow_html=True)

    if verificar_identicos:
        if registros_iguais:
            st.markdown("<h3 class='rvs-section-title'>Registros com entrada/saída idênticos:</h3>", unsafe_allow_html=True)
            for r in registros_iguais:
                st.markdown(f"""
                <div class='rvs-card grey'>
                    <strong>{r[0]}</strong> | {r[1]} | {r[2]} | Página {r[3]}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='rvs-card none'>
                Nenhum registro idêntico encontrado.
            </div>
            """, unsafe_allow_html=True)

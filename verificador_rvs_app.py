import streamlit as st
import pdfplumber
import re
from datetime import datetime
from io import BytesIO

# Configuração inicial obrigatória
st.set_page_config(
    page_title="Verificador RVS",
    page_icon="https://raw.githubusercontent.com/carlosrvs/verificador-rvs-app/main/logo-min-flat.png",
    layout="centered"
)

# Estilo CSS para ajustar a estética do layout
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
        font-weight: 700 !important;
        border-radius: 10px;
        font-size: 19px;
    }
    /* Estilização das labels */
    div[data-testid="stNumberInput"] > label,
    div[data-testid="stFileUploader"] > label {
        color: #d4af37 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        text-shadow: 0 1px 6px rgba(0, 0, 0, 0.6);
    }
    /* Checkbox Label (específico para o span do texto) */
    div[data-testid="stCheckbox"] > label > div[data-testid="stMarkdownContainer"] > span {
        color: #d4af37 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        text-shadow: 0 1px 6px rgba(0, 0, 0, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Título e descrição
st.image("https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png", width=110)
st.markdown("""
<h1 style='color: #d4af37;'>Verificador <span style="color: #d4af37;">RVS</span></h1>
<p>Automatize a conferência de jornadas com base nos arquivos PDF de contagem.</p>
""", unsafe_allow_html=True)

# Widgets: inputs e uploads
limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25)
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos")
uploaded_file = st.file_uploader("Envie o PDF da contagem", type=["pdf"])

# Condicional para processar o upload
if uploaded_file:
    dias_excedidos = []
    registros_iguais = []

    # Processar o PDF
    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for page in pdf.pages:
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
                        dias_excedidos.append((data_str, a01))

                    if verificar_identicos:
                        pares = list(zip(horarios[::2], horarios[1::2]))
                        for entrada, saida in pares:
                            if entrada == saida:
                                registros_iguais.append((data_str, f"{entrada} - {saida}"))

    # Resultado da verificação
    st.markdown('<h2 style="color: #d4af37;">Resultado da Verificação</h2>', unsafe_allow_html=True)
    st.markdown("### Dias com mais horas que o limite:")
    if dias_excedidos:
        for d in dias_excedidos:
            st.write(f"**{d[0]}** — {d[1]} horas")
    else:
        st.write("Nenhum dia excedeu o limite.")

    if verificar_identicos:
        st.markdown("### Registros de entrada/saída idênticos:")
        if registros_iguais:
            for r in registros_iguais:
                st.write(f"**{r[0]}** — {r[1]}")
        else:
            st.write("Nenhum registro idêntico encontrado.")

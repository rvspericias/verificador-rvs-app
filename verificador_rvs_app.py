
import streamlit as st
import pdfplumber
import re
from io import BytesIO

st.set_page_config(page_title="Verificador RVS", layout="centered")

st.markdown("""
<style>
    .main {
        background-color: #fdfdfd;
        color: #333;
    }
    .stButton>button {
        background-color: #d4af37;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.image("https://i.imgur.com/BMiGRHt.png", width=100)
st.title("Verificador RVS")
st.caption("Automatize a conferência de jornadas com base nos arquivos PDF de contagem")

# Limite de horas
limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25, format="%0.2f")

# Verificação de registros idênticos
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos", value=True)

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Envie o PDF da contagem de horas", type=["pdf"])

if uploaded_file:
    dias_excedidos = []
    registros_iguais = []

    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if not texto:
                continue
            linhas = texto.split('\n')
            mes_ref = next((re.search(r'(JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)/\d{4}', l)
                           for l in linhas if re.search(r'/\d{4}', l)), None)
            mes_ref = mes_ref.group(0) if mes_ref else "Mês Desconhecido"

            for linha in linhas:
                if re.match(r'^\d{2}/\d{2}/\d{2}', linha):
                    horarios = re.findall(r'\d{2}:\d{2}', linha)
                    if not horarios or len(horarios) < 2:
                        continue
                    valores = re.findall(r'\d+,\d+', linha)
                    try:
                        a01 = float(valores[0].replace(",", "."))
                        if a01 > limite:
                            dias_excedidos.append((linha[:8], a01, mes_ref))
                    except:
                        pass

                    if verificar_identicos:
                        pares = list(zip(horarios[::2], horarios[1::2]))
                        for ent, sai in pares:
                            if ent == sai:
                                registros_iguais.append((linha[:8], f"{ent} - {sai}", mes_ref))

    st.markdown("---")
    st.subheader("Resultado da Verificação")

    if dias_excedidos:
        st.write("### Dias com mais horas que o limite:")
        for d in dias_excedidos:
            st.write(f"- {d[0]} | {d[1]}h | {d[2]}")
    else:
        st.success("Nenhum dia excedeu o limite de horas.")

    if verificar_identicos:
        if registros_iguais:
            st.write("### Registros com entrada/saída idênticos:")
            for r in registros_iguais:
                st.warning(f"- {r[0]} | {r[1]} | {r[2]}")
        else:
            st.info("Nenhum registro idêntico encontrado.")

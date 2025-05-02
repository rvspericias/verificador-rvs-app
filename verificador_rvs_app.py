
import streamlit as st
import pdfplumber
import re
from io import BytesIO

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
        background-color: #ffffff;
        color: #222222;
    }

    .stButton>button {
        background-color: #d4af37;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5em 1em;
        border-radius: 8px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #c49d2e;
    }
</style>
""", unsafe_allow_html=True)

st.image("https://raw.githubusercontent.com/rvspericias/verificador-rvs-app/refs/heads/main/logo-min-flat.png", width=100)

st.markdown("""
<h1 style='font-family: Roboto; font-size: 42px; color: #222; margin-bottom: 0;'>Verificador <span style='color:#d4af37;'>RVS</span></h1>
<p style='font-family: Roboto; font-size: 18px; color: #555; margin-top: 0;'>Automatize a conferência de jornadas com base nos arquivos PDF de contagem</p>
""", unsafe_allow_html=True)

limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25, format="%0.2f")
verificar_identicos = st.checkbox("Verificar registros de entrada/saída idênticos", value=True)

with st.container():
    st.markdown("""
    <h4 style='font-family: Roboto; color: #444;'>📎 Upload do Arquivo</h4>
    <p style='color: #777;'>Selecione o arquivo PDF da contagem de horas para verificar os registros.</p>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Envie o PDF da contagem de horas", type=["pdf"])

if uploaded_file:
    dias_excedidos = []
    registros_iguais = []

    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        for idx, page in enumerate(pdf.pages):
            texto = page.extract_text()
            if not texto:
                continue

            linhas = texto.split('\n')
            mes_ref = next((re.search(r'(JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)/\d{4}', l)
                            for l in linhas), None)
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
                            dias_excedidos.append((linha[:8], a01, mes_ref, idx + 1))
                    except:
                        pass

                    if verificar_identicos:
                        pares = list(zip(horarios[::2], horarios[1::2]))
                        for ent, sai in pares:
                            if ent == sai:
                                registros_iguais.append((linha[:8], f"{ent} - {sai}", mes_ref, idx + 1))

    st.markdown("---")
    st.subheader("Resultado da Verificação")

    if dias_excedidos:
        st.write("### Dias com mais horas que o limite:")
        for d in dias_excedidos:
            st.markdown(f"""
            <div style='background:#fff8dc; padding:10px; border-left:5px solid #d4af37; margin-bottom:8px; border-radius:6px;'>
                <strong>{d[0]}</strong> | {d[1]} | {d[2]} | Página {d[3]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:#e6f4ea; padding:10px; border-left:5px solid #2e7d32; margin-bottom:8px; border-radius:6px;'>
            <strong>Nenhum dia excedeu o limite de horas.</strong>
        </div>
        """, unsafe_allow_html=True)

    if verificar_identicos:
        if registros_iguais:
            st.write("### Registros com entrada/saída idênticos:")
            for r in registros_iguais:
                st.markdown(f"""
                <div style='background:#f8f9fa; padding:10px; border-left:5px solid #888; margin-bottom:8px; border-radius:6px;'>
                    <strong>{r[0]}</strong> | {r[1]} | {r[2]} | Página {r[3]}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum registro idêntico encontrado.")

import streamlit as st
import pdfplumber
import re
from datetime import datetime
from io import BytesIO

# Função para verificar se o formato do PDF é o novo ou antigo
def identificar_formato(texto):
    if "TOTAL" in texto:  # Verifica a presença da coluna TOTAL
        return 'novo'
    return 'antigo'

# Função para extrair dados no formato antigo
def processar_antigo(texto, limite):
    dias_excedidos = []
    registros_iguais = []
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
            pares = list(zip(horarios[::2], horarios[1::2]))
            for entrada, saida in pares:
                if entrada == saida:
                    registros_iguais.append((data_str, entrada))
    return dias_excedidos, registros_iguais

# Função para extrair dados no formato novo
def processar_novo(texto, limite):
    dias_excedidos = []
    registros_iguais = []
    linhas = texto.split('\n')
    for linha in linhas:
        if re.match(r'^\d{2}', linha):
            partes = linha.split()
            data_str = partes[0]
            try:
                horas = float(partes[-1].replace(',', '.'))  # Captura o valor da coluna TOTAL
            except ValueError:
                continue
            if horas > limite:
                dias_excedidos.append((data_str, horas))
            # Verificando registros de entrada/saída idênticos
            horarios = re.findall(r'\d{2}:\d{2}', linha)
            pares = list(zip(horarios[::2], horarios[1::2]))
            for entrada, saida in pares:
                if entrada == saida:
                    registros_iguais.append((data_str, entrada))
    return dias_excedidos, registros_iguais

# Código principal do Streamlit
st.set_page_config(page_title="Verificador RVS", page_icon="https://raw.githubusercontent.com/carlosrvs/verificador-rvs-app/main/logo-min-flat.png", layout="centered")
st.markdown("<h1 style='color: #ffffff;'>Verificador <span style='color: #d4af37;'>RVS</span></h1>", unsafe_allow_html=True)

limite = st.number_input("Limite máximo de horas por dia (ex: 17.00)", min_value=0.0, max_value=24.0, value=17.00, step=0.25)
uploaded_file = st.file_uploader("Envie o PDF da contagem", type=["pdf"])

if uploaded_file:
    with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() or ""
        
        # Identificar formato
        formato = identificar_formato(texto)
        
        if formato == 'novo':
            dias_excedidos, registros_iguais = processar_novo(texto, limite)
        else:
            dias_excedidos, registros_iguais = processar_antigo(texto, limite)

        st.markdown('<h2 class="result-header">Resultado da Verificação</h2>', unsafe_allow_html=True)
        
        # Exibir resultados para dias excedidos
        st.markdown('<h3 class="subtitle">Dias com mais horas que o limite:</h3>', unsafe_allow_html=True)
        if dias_excedidos:
            for data, horas in dias_excedidos:
                st.markdown(f"<div class='result-box exceeded'><strong>{data}</strong> | {horas:.2f} horas</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-box exceeded'>Nenhum dia excedeu o limite de horas.</div>", unsafe_allow_html=True)

        # Exibir resultados para registros idênticos
        st.markdown('<h3 class="subtitle">Registros de entrada/saída idênticos:</h3>', unsafe_allow_html=True)
        if registros_iguais:
            for data, registro in registros_iguais:
                st.markdown(f"<div class='result-box identical'><strong>{data}</strong> | {registro}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-box identical'>Nenhum registro idêntico encontrado.</div>", unsafe_allow_html=True)

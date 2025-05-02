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
    /* Main page background */
    body {
        background-color: #f5f5f5 !important;
    }
    
    /* Checkbox style */
    .stCheckbox [aria-checked="true"] + label:before {
        background-color: #27d154 !important;
        border-color: #27d154 !important;
    }
    
    /* Header and other styles */
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

# [...] (restante do código permanece igual)

# Adicionei apenas as alterações de estilo necessárias:
# 1. Cor de fundo da página para cinza claro (#f5f5f5)
# 2. Cor do checkbox marcado para verde (#27d154)

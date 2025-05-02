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
    .sniper-wrap {
        width:100%%; display:flex; justify-content: center; margin-bottom: 14px;
    }
    .sniper-svg {
        width: 62px; height: 62px; display: block;
        filter: drop-shadow(0 2px 7px #224a85a0;
    }
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

    /* ===== Melhorias solicitadas ===== */
    .header-gold {
        /* Mantém os estilos originais */
        color: #d4af37 !important;
        font-weight: 900;
        font-size: 2.1rem !important;
        margin-top: 1.5em;
        margin-bottom: 0.25em; /* <--- Reduz espaçamento inferior (ajuste fino) */
        letter-spacing: 0.01em;
        text-shadow: 0 1px 12px #00000022, 0 0px 14px #d4af373A;
        font-family: 'Roboto', sans-serif !important;
        line-height: 1.1;
        text-align: left;
    }
    .subtitle-custom {
        font-size: 1.01rem !important; /* <--- Bem menor que o título */
        color: #e4e4e4 !important;
        font-weight: 600;
        margin-top: 0.09em; /* <--- Quase elimina o espaço acima */
        margin-bottom: 0.55em;
        font-family: 'Roboto', sans-serif !important;
        letter-spacing: 0.01em;
        text-align: left;
    }
    /* ===== Fim das melhorias ===== */
</style>
""", unsafe_allow_html=True)

# Exemplo de uso das novas classes:
st.markdown('<div class="header-gold">Resultado da Verificação</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-custom">Dias com mais horas que o limite:</div>', unsafe_allow_html=True)

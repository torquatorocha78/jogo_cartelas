import streamlit as st

# Configuração da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Mágica da Matemática Binária",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. ESTILIZAÇÃO CSS CUSTOMIZADA ---
# Melhoria visual baseada nos seus pontos, com tratamento de contraste e responsividade.
st.markdown(
    """
    <style>
    .cartela-box {
        background-color: rgba(30, 30, 47, 0.6);
        border: 1px solid #4F46E5;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .grid-numeros {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .numero-item {
        background: linear-gradient(135deg, #312E81, #4F46E5);
        color: #FFFFFF !important;
        padding: 6px;
        border-radius: 6px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .numero-item:hover {
        transform: scale(1.1);
        box-shadow: 0 0 8px #818CF8;
    }
    .titulo-cartela {
        text-align: center;
        color: #818CF8;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. CAMADA DE NEGÓCIO E ALGORITMOS (CACHEADO) ---
@st.cache_data
def gerar_cartelas(max_num: int = 127) -> dict[int, list[int]]:
    """
    Gera as cartelas dinamicamente com base nas potências de 2.
    Para max_num = 127, serão geradas 7 cartelas (bits de 2^0 a 2^6).
    """
    num_bits = max_num.bit_length()
    cartelas = {2**i: [] for i in range(num_bits)}

    for num in range(1, max_num + 1):
        for i in range(num_bits):
            if (num >> i) & 1:
                cartelas[2**i].append(num)

    return cartelas

# Inicializa as cartelas (limite aumentado para 127)
LIMITE_MAXIMO = 127
cartelas = gerar_cartelas(LIMITE_MAXIMO)

# --- 3. CONTROLE DE ESTADO (SESSION STATE) ---
# Inicialização segura dos estados dos checkboxes
for bit_value in cartelas.keys():
    state_key = f"cartela_{bit_value}"
    if state_key not in st.session_state:
        st.session_state[state_key] = False

# --- 4. INTERFACE DO USUÁRIO (UI) ---

st.title("🔮 O Mistério do Sistema Binário")
st.write(
    f"Pense em um número de **1 a {LIMITE_MAXIMO}**. "
    "Selecione 'Sim' abaixo de cada cartela onde seu número aparece. Eu vou adivinhá-lo!"
)

# Botão Limpar Seleção (Melhoria 2)
if st.button("🔄 Limpar Seleção", type="secondary"):
    for bit_value in cartelas.keys():
        st.session_state[f"cartela_{bit_value}"] = False
    st.rerun()

st.divider()

# --- 5. RENDERIZAÇÃO DAS CARTELAS EM GRID (Melhoria 1 adaptada para 7 itens) ---
# Como são 7 cartelas, usamos 2 linhas de 4 colunas (a última fica vazia para layout limpo)
cartelas_itens = list(cartelas.items())
colunas_por_linha = 4

for i in range(0, len(cartelas_itens), colunas_por_linha):
    chunk = cartelas_itens[i : i + colunas_por_linha]
    cols = st.columns(colunas_por_linha)

    for idx, (bit_value, numeros) in enumerate(chunk):
        with cols[idx]:
            # Container visual da cartela
            st.markdown(f"<div class='titulo-cartela'>Cartela {bit_value}</div>", unsafe_allow_html=True)

            # Grid de números em HTML/CSS para performance e controle de hover
            numeros_html = "".join([f"<div class='numero-item'>{n}</div>" for n in numeros])
            st.markdown(
                f"<div class='cartela-box'><div class='grid-numeros'>{numeros_html}</div></div>",
                unsafe_allow_html=True
            )

            # Checkbox vinculado diretamente ao Session State
            st.checkbox(
                "Meu número está aqui",
                key=f"cartela_{bit_value}"
            )

st.divider()

# --- 6. CÁLCULO DO RESULTADO E EXPLICAÇÃO (Melhoria 3, 4 e 6) ---
resultado = sum(
    bit_value for bit_value, _ in cartelas_itens 
    if st.session_state[f"cartela_{bit_value}"]
)

if resultado > 0:
    st.success(f"### 🎉 O número que você pensou é: **{resultado}**!")

    # Detalhamento didático
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🖥️ Lógica Binária por trás da Mágica")
        # Mostra o número binário com 7 bits preenchidos com zeros à esquerda
        binario = bin(resultado)[2:].zfill(7)
        st.code(
            f"Número Decimal: {resultado}\n"
            f"Representação Binária: {binario}",
            language="text"
        )

    with col2:
        st.markdown("### 🧮 Explicação Matemática")
        # Constrói dinamicamente a soma das potências de 2 ativas
        partes_soma = [
            str(bit_value) for bit_value, _ in cartelas_itens 
            if st.session_state[f"cartela_{bit_value}"]
        ]
        expressao_soma = " + ".join(partes_soma)

        st.write(
            f"Cada cartela que você marcou representa uma potência de 2. "
            f"O truque soma o primeiro elemento de cada cartela marcada:\n\n"
            f"**{resultado} = {expressao_soma}**"
        )
else:
    st.info("💡 Selecione 'Sim' nas cartelas para começar a mágica!")

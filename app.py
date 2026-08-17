import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Mestre das Cartelas Mágicas",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para deixar as cartelas bonitas e responsivas
st.markdown("""
<style>
    .cartela-container {
        background-color: #1E1E2F;
        border: 2px solid #4F46E5;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    .cartela-title {
        color: #6366F1;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        border-bottom: 1px solid #4F46E5;
        padding-bottom: 5px;
    }
    .grid-numeros {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.1rem;
        font-weight: bold;
        color: #E2E8F0;
    }
    .numero-item {
        background-color: #2D2D44;
        padding: 4px;
        border-radius: 4px;
    }
    .destaque-primeiro {
        color: #F59E0B; /* Destaque para o primeiro número da cartela */
    }
</style>
""", unsafe_allow_html=True)


def gerar_cartelas(max_numero=63):
    """
    Gera as cartelas dinamicamente com base na lógica binária.
    Retorna um dicionário onde a chave é a potência de 2 (primeiro número da cartela)
    e o valor é a lista de números que pertencem a essa cartela.
    """
    cartelas = {}
    # 6 cartelas cobrem de 1 a 63 (2^0 até 2^5)
    for i in range(6):
        valor_cartela = 2**i
        numeros_cartela = []
        for num in range(1, max_numero + 1):
            # Verifica se o i-ésimo bit está ativo no número
            if (num >> i) & 1:
                numeros_cartela.append(num)
        cartelas[valor_cartela] = numeros_cartela
    return cartelas


# Inicialização das cartelas
cartelas = gerar_cartelas()

# Título e Introdução
st.title("🔮 O Mestre das Cartelas Mágicas")
st.markdown("""
### Como Jogar:
1. Pense em um número inteiro de **1 a 63** (não me diga qual é!).
2. Olhe atentamente para as **6 cartelas** abaixo.
3. Marque a caixinha correspondente **apenas** nas cartelas onde o seu número pensado aparece.
4. Clique no botão **"Adivinhar Número"** para ver a mágica acontecer!
""")

st.write("---")

# Criar um layout de colunas para as cartelas (3 colunas x 2 linhas)
cols = st.columns(3)
escolhas = {}

# Renderizar as cartelas
for index, (primeiro_num, numeros) in enumerate(cartelas.items()):
    col_index = index % 3
    with cols[col_index]:
        # HTML para renderizar a cartela formatada em Grid
        grid_html = "".join([
            f'<div class="numero-item {"destaque-primeiro" if n == primeiro_num else ""}">{n:02d}</div>'
            for n in numeros
        ])

        st.markdown(f"""
        <div class="cartela-container">
            <div class="cartela-title">Cartela {index + 1}</div>
            <div class="grid-numeros">
                {grid_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Checkbox para o usuário selecionar se o número está nesta cartela
        escolhas[primeiro_num] = st.checkbox(
            f"Meu número está na Cartela {index + 1}", 
            key=f"cartela_{primeiro_num}"
        )

st.write("---")

# Seção de adivinhação
col_btn, col_res = st.columns([1, 2])

with col_btn:
    st.write("")
    st.write("")
    botao_adivinhar = st.button("🔮 Adivinhar Meu Número!", use_container_width=True, type="primary")

with col_res:
    if botao_adivinhar:
        # Lógica matemática: soma do primeiro número de cada cartela selecionada
        resultado = sum(primeiro_num for primeiro_num, selecionado in escolhas.items() if selecionado)

        if resultado > 0:
            st.balloons()
            st.success(f"### 🎉 Eu sei o seu número! Você pensou no número **{resultado}**!")
            st.info(
                f"**Segredo do Mestre:** Eu somei silenciosamente os primeiros números das cartelas que você escolheu: "
                f"({ ' + '.join([str(num) for num, sel in escolhas.items() if sel]) }) = **{resultado}**! 😉"
            )
        else:
            st.warning("⚠️ Você não selecionou nenhuma cartela! Pense em um número e marque as cartelas onde ele aparece.")

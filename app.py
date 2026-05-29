
import streamlit as st

st.set_page_config(
    page_title="Apresentação com Placar",
    layout="wide"
)

# =========================
# CSS: slides centralizados + placar fixo no rodapé
# =========================
st.markdown(
    """
    <style>

    /* esconde o header padrão para aproveitar a tela inteira */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* zera o padding/limite do container principal para o slide
       poder ocupar a tela toda sem gerar scroll */
    [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* o container dos slides ocupa a tela inteira (descontando o
       espaço do placar) e centraliza o conteúdo nos dois eixos */
    .st-key-slides {
        box-sizing: border-box;
        min-height: 80vh;
        padding: 2rem 2rem 2rem 2rem;
        display: flex !important;
        flex-direction: column;
        justify-content: center !important;
        align-items: center !important;
        text-align: center;
    }

    /* esconde os botões de passar slide */
    button[kind="tertiary"] {
        display: none;
    }

    /* placar colado na parte inferior da tela */
    .st-key-placar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #0e1117;
        padding: 10px 150px;
        border-top: 1px solid #444;
        z-index: 999;
    }

    /* centraliza o texto dos jogadores e valores de seus placares */
    .st-key-placar .stElementContainer {
        text-align: center;
    }

    /* esconde o atalho de teclado para botões */
    .stButton kbd {
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Esconde os links de ancora nos headers, subheaders e markdown
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

# =========================
# Estado inicial
# =========================
if "slide" not in st.session_state:
    st.session_state.slide = 0

if "scores" not in st.session_state:
    st.session_state.scores = {
        "Igot": 0,
        "Tatá": 0,
        "Tenshi": 0,
    }

shortcut_map = {
    "Igot": ("1", "Shift+1"),
    "Tatá": ("2", "Shift+2"),
    "Tenshi": ("3", "Shift+3"),
}

# =========================
# Slides (apenas conteúdo)
# =========================
slides = [
    {"content": "Bem-vindo à apresentação."},
    {"content": "Aqui você pode colocar qualquer texto."},
    {"content": "O placar continua visível o tempo todo."},
]

# =========================
# Área dos slides (centralizada vertical e horizontalmente)
# =========================
with st.container(key="slides"):

    current_slide = slides[st.session_state.slide]

    st.markdown(
        f"""
        <div style="
            text-align: center;
            font-size: 3.5rem;
            font-weight: 600;
            line-height: 1.4;
            width: 100%;
        ">
            {current_slide["content"]}
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅", shortcut="ArrowLeft", type="tertiary"):
            if st.session_state.slide > 0:
                st.session_state.slide -= 1
                st.rerun()

    with col2:
        with st.container(horizontal=True, horizontal_alignment="right"):
            if st.button("➡", shortcut="ArrowRight", type="tertiary"):
                if st.session_state.slide < len(slides) - 1:
                    st.session_state.slide += 1
                    st.rerun()

# =========================
# Placar fixo no rodapé
# =========================
with st.container(key="placar"):

    player_cols = st.columns(len(st.session_state.scores))

    for player, player_col in zip(st.session_state.scores, player_cols):

        with player_col:

            st.subheader(player, anchor=None)

            st.markdown(
                f"# {st.session_state.scores[player]}"
            )

            minus, plus = st.columns(2)

            minus_shortcut, plus_shortcut = shortcut_map[player]

            with minus:
                with st.container(horizontal=True, horizontal_alignment="right"):
                    if st.button(
                        "-",
                        key=f"minus_{player}",
                        shortcut=minus_shortcut,
                        type="secondary" # change to tertiary to hide
                    ):
                        st.session_state.scores[player] -= 1
                        st.rerun()

            with plus:

                if st.button(
                    "+",
                    key=f"plus_{player}",
                    shortcut=plus_shortcut,
                    type="secondary" # change to tertiary to hide
                ):
                    st.session_state.scores[player] += 1
                    st.rerun()

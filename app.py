
import streamlit as st

st.set_page_config(
    page_title="Game Changer",
    layout="wide"
)

# =========================
# Slides loaded from slides.txt
# Each line = 1 slide
# =========================
with open("slides.txt", "r", encoding="utf-8") as file:
    slides = [
        line.strip()
        for line in file
    ]

# =========================
# Players loaded from players.txt
# Format:
# Name;StartingPoints
# =========================
if "scores" not in st.session_state:

    st.session_state.scores = {}

    with open("players.txt", "r", encoding="utf-8") as file:

        for line in file.readlines():

            line = line.strip()

            if not line:
                continue

            name, score = line.split(";")

            st.session_state.scores[name.strip()] = int(score.strip())


# =========================
# CSS: Centered slides and fixed scoreboard on footer
# =========================
st.markdown(
    """
    <style>

    /* hides default streamlit header */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* removes main container padding/limit so the slide can occupy
       the entire screen without a scroll bar */
    [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* removes gap around the slide */
    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    /* slides container occupies a percentage of the whole screen
       to adjust for the scoreboard space */
    .st-key-slides {
        box-sizing: border-box;
        min-height: 75vh; /* 100vh - scoreboard's height */
        max-height: 75vh;
        padding: 2rem;
        display: flex !important;
        flex-direction: column;
        justify-content: center !important;
        align-items: center !important;
        text-align: center;
    }

    /* hides slides navigation's buttons (and possibly the scoreboard's) */
    button[kind="tertiary"] {
        display: none;
    }

    /* fixed footer scoreboard */
    .st-key-scoreboard {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #0e1117;
        padding: 10px 150px;
        border-top: 1px solid #444;
        z-index: 999;
        height: 25vh;
    }

    .st-key-scoreboard {
        /* centers text and points in the scoreboard */
        .stElementContainer {
            text-align: center;
        }

        /* controls player and score font size */
        h1, h2 {
            font-size: 3rem !important;
        }
    }

    /* hides the shortcut tooltip from buttons */
    .stButton kbd {
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Hides link anchor elements from default streamlit elements
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

# =========================
# Initial state
# =========================
if "slide" not in st.session_state:
    st.session_state.slide = 0

# =========================
# Slide area (centered horizontally and vertically)
# =========================
with st.container(key="slides"):

    current_slide = slides[st.session_state.slide]

    if current_slide:
        font_size = max(
            2.5,
            min(
                10,
                70 / (len(current_slide) ** 0.5)
            )
        )
    else:
        font_size = 10

    st.markdown(
        f"""
        <div style="
            text-align: center;
            font-size:{font_size}rem;
            font-weight: 600;
            line-height: 1.4;
            width: 100%;
        ">
            {current_slide}
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
# Fixed scoreboard on footer
# =========================
with st.container(key="scoreboard"):

    player_cols = st.columns(len(st.session_state.scores))

    for index, (player, player_col) in enumerate(
        zip(st.session_state.scores, player_cols),
        start=1
    ):

        with player_col:

            st.header(player)

            st.markdown(
                f"# {st.session_state.scores[player]}"
            )

            minus, plus = st.columns(2)

            with minus:
                with st.container(horizontal=True, horizontal_alignment="right"):
                    if st.button(
                        "-",
                        key=f"minus_{player}",
                        shortcut=str(index),
                        type="secondary" # change to tertiary to hide
                    ):
                        st.session_state.scores[player] -= 1
                        st.rerun()

            with plus:

                if st.button(
                    "+",
                    key=f"plus_{player}",
                    shortcut=f"Shift+{index}",
                    type="secondary" # change to tertiary to hide
                ):
                    st.session_state.scores[player] += 1
                    st.rerun()

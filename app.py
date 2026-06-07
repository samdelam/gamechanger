import streamlit as st
import base64
from pathlib import Path
import json
import time

st.set_page_config(
    page_title="Game Changer",
    layout="wide"
)

# ==================================================
# Loads custom fonts
# ==================================================
def load_font(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

dseg7_classic = load_font("fonts/DSEG7Classic-Regular.ttf")
trade_gothic_bold_condensed = load_font("fonts/trade-gothic-lt-std-bold-condensed-no-20-5872def1d27d8.otf")

st.markdown(
    f"""
    <style>

    @font-face {{
        font-family: 'DSEG7';
        src: url("data:font/ttf;base64,{dseg7_classic}") format('truetype');
    }}

    @font-face {{
        font-family: 'TradeGothicBoldCondensed';
        src: url("data:font/otf;base64,{trade_gothic_bold_condensed}") format('opentype');
        font-weight: 700;
        font-style: normal;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# Loads cover slide
# ==================================================
cover_image = None

for candidate in [
    "cover.png",
    "cover.jpg",
    "cover.jpeg",
    "cover.webp"
]:
    if Path(candidate).exists():
        cover_image = candidate
        break

has_cover = cover_image is not None
text_slide_offset = 1 if has_cover else 0

# ==================================================
# Slides loaded from slides.txt
# Each line = 1 slide
# ==================================================
with open("slides.txt", "r", encoding="utf-8") as file:
    slides = [
        line.strip()
        for line in file
    ]

# ==================================================
# Loading information from config.json
# ==================================================
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

# ==================================================
# Player info
# ==================================================
if "players" not in st.session_state:
    st.session_state.players = {}

    for player in config["players"]:
        st.session_state.players[player["name"]] = {
            "score": player["starting_score"],
            "starting_slide": player["starting_slide"],
            "can_win": player["can_win"]
        }

# ==================================================
# Winner texts
# ==================================================
winner_config = config.get("winner", {})
winner_enabled = winner_config.get("enabled", False)

if winner_enabled:
    winner_single_title = winner_config["single"]["title"]
    winner_single_score = winner_config["single"]["score_text"]

    winner_multiple_title = winner_config["multiple"]["title"]
    winner_separator = winner_config["multiple"]["separator"]
    winner_multiple_score = winner_config["multiple"]["score_text"]

# ==================================================
# Loads sounds
# ==================================================
sounds_settings = config.get("sounds", {})

slide_sound_enabled = sounds_settings.get("slide", True)

gain_points_sound_enabled = sounds_settings.get("gain_points",True)
gain_points_sound_delay_seconds = sounds_settings.get("gain_points_delay_seconds",1.0)
lose_points_sound_enabled = sounds_settings.get("lose_points",True)
lose_points_sound_delay_seconds = sounds_settings.get("lose_points_delay_seconds",1.0)

if slide_sound_enabled:
    with open("slide.wav", "rb") as f:
        slide_sound_bytes = f.read()
if gain_points_sound_enabled:
    with open("gain_point.wav", "rb") as f:
        gain_points_sound_bytes = f.read()
if lose_points_sound_enabled:
    with open("lose_point.wav", "rb") as f:
        lose_points_sound_bytes = f.read()

# ==================================================
# Buttons
# ==================================================
buttons_settings = config.get("buttons", {})

slide_buttons_enabled = buttons_settings.get("slide", False)
points_buttons_enabled = buttons_settings.get("points", False)

slide_buttons_css_type = "secondary" if slide_buttons_enabled else "tertiary"
points_buttons_css_type = "secondary" if points_buttons_enabled else "tertiary"

# ==================================================
# Shortcuts
# ==================================================
buttons_settings = config.get("shortcuts", {})

slide_next_shortcut = buttons_settings.get("slide_next", "ArrowRight")
slide_previous_shortcut = buttons_settings.get("slide_previous", "ArrowLeft")

points_modifier_shortcut = buttons_settings.get("points_modifier", "Shift")
points_inverted_shortcut = buttons_settings.get("points_inverted", False)

# ==================================================
# CSS: Centered slides and fixed scoreboard on footer
# ==================================================
scoreboard_height = "23vh"
slides_margin = "1rem"
slides_height = f"calc(100vh - {scoreboard_height} - ({slides_margin} *2))"

st.markdown(
    f"""
    <style>

    /* overwrites default font */

    html,
    body,
    [data-testid="stAppViewContainer"] {{
        font-family: 'TradeGothicBoldCondensed' !important;
    }}

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    span,
    div,
    button {{
        font-family: 'TradeGothicBoldCondensed' !important;
    }}

    /* overall black blackground */
    [data-testid="stAppViewContainer"] {{
        background: black;
    }}

    /* hides default streamlit header */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}

    /* removes main container padding/limit so the slide can occupy
       the entire screen without a scroll bar */
    [data-testid="stMainBlockContainer"] {{
        padding: 0 !important;
        max-width: 100% !important;
    }}

    /* removes gap around the slide */
    [data-testid="stVerticalBlock"] {{
        gap: 0 !important;
    }}

    /* slides container occupies a percentage of the whole screen
       to adjust for the scoreboard space */
    .st-key-slides {{
        box-sizing: border-box;
        min-height: {slides_height};
        max-height: {slides_height};
        padding: 2rem;
        display: flex !important;
        flex-direction: column;
        justify-content: center !important;
        align-items: center !important;
        text-align: center;
        width: calc(100% - ({slides_margin} * 2));
        position: relative;

        /* game changer prompt backgroud */
        background: #dcdcdc;
        border-radius: 5rem;
        margin: {slides_margin};
        box-shadow:
            inset 0 0 0 1px rgba(0,0,0,.08);
        color: #111111;

        /* configure navigation buttons, if visible */
        button[kind="secondary"] {{
            color: #dcdcdc;
            background: #111111;
        }}

        .stHorizontalBlock:last-child {{
            width: auto;
            position: absolute;
            bottom: 2rem;
            left: 2rem;
            right: 2rem;
        }}
    }}

    /* fixed footer scoreboard */
    .st-key-scoreboard {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: black;
        padding: 10px 150px;
        z-index: 999;
        height: {scoreboard_height};

        /* centers text and points in the scoreboard */
        .stElementContainer {{
            text-align: center;
        }}

        /* controls player font */
        h2 {{
            font-size: 3rem !important;
        }}

        button[kind="secondary"] {{
            margin-top: 20px;
            width: 33px !important;
            min-width: 33px !important;
        }}
    }}

    /* hides the shortcut tooltip from buttons */
    .stButton kbd {{
        display: none;
    }}

    /* scores custom class for different font and color */
    .score-value {{
        font-family: 'DSEG7', monospace !important;
        color: #ff2a2a !important;
        text-shadow:
            0 0 5px #ff2a2a,
            0 0 10px #ff2a2a,
            0 0 20px #ff2a2a;

        font-size: 3rem !important;
        font-weight: normal !important;
    }}

    /* hides slides navigation's buttons (and possibly the scoreboard's) */
    button[kind="tertiary"] {{
        display: none;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# Hides link anchor elements from default streamlit elements
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

# ==================================================
# Initial state
# ==================================================
if "slide" not in st.session_state:
    st.session_state.slide = 0
if "last_slide" not in st.session_state:
    st.session_state.last_slide = st.session_state.slide
slide_changed = (
    st.session_state.slide
    != st.session_state.last_slide
)

if "pending_gain_sound" not in st.session_state:
    st.session_state.pending_gain_sound = None
if "pending_lose_sound" not in st.session_state:
    st.session_state.pending_lose_sound = None

# ==================================================
# Slide area
# ==================================================
with st.container(key="slides"):

    is_cover_slide = (
        has_cover
        and st.session_state.slide == 0
    )

    winner_slide = (
        winner_enabled
        and st.session_state.slide == len(slides) + text_slide_offset
    )

    if not is_cover_slide and not winner_slide:
        text_slide_index = (
            st.session_state.slide
            - text_slide_offset
        )

        current_slide = slides[text_slide_index]

    if is_cover_slide:
        st.markdown(
            f"""
            <style>
            .st-key-slides {{
                padding: 0 !important;
                overflow: hidden;
                min-height: calc(100vh - ({slides_margin} * 2)) !important;"
                max-height: calc(100vh - ({slides_margin} * 2)) !important;"
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        st.image(
            cover_image,
            width="stretch",
        )
    elif winner_slide:
        eligible_players = [
            (name, data)
            for name, data in st.session_state.players.items()
            if data["can_win"]
        ]

        highest_score = max(
            player["score"]
            for _, player in eligible_players
        )

        winners = [
            name
            for name, player in eligible_players
            if player["score"] == highest_score
        ]
        
        if len(winners) == 1:
            winners_title = winner_single_title
            winners_text = winners[0]
            winners_score = winner_single_score.format(score=highest_score)
        else:
            winners_title = winner_multiple_title
            winners_score = winner_multiple_score.format(score=highest_score)
            if len(winners) == 2:
                winners_text = f"{winners[0]} {winner_separator} {winners[1]}"
            else:
                winners_text = ", ".join(winners[:-1])
                winners_text += f" {winner_separator} {winners[-1]}"

        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:6rem;
                font-weight:600;
            ">
                {winners_title}
            </div>

            <div style="
                text-align:center;
                font-size:8rem;
                font-weight:800;
            ">
                {winners_text}
            </div>

            <div style="
                text-align:center;
                font-size:6rem;
                font-weight:600;
            ">
                {winner_single_score.replace("{score}", str(highest_score))}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
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
            ">
                {current_slide}
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.slide > 0:
            if st.button("⬅", shortcut=slide_previous_shortcut, type=slide_buttons_css_type):
                st.session_state.slide -= 1
                st.rerun()

    max_slide = len(slides) if winner_enabled else len(slides) - 1
    max_slide += text_slide_offset
    with col2:
        if st.session_state.slide < max_slide:
            with st.container(horizontal=True, horizontal_alignment="right"):
                if st.button("➡", shortcut=slide_next_shortcut, type=slide_buttons_css_type):
                    st.session_state.slide += 1
                    st.rerun()

# ==================================================
# Fixed scoreboard on footer
# ==================================================
if not is_cover_slide:
    with st.container(key="scoreboard"):
        visible_players = [
            (name, data)
            for name, data in st.session_state.players.items()
            if st.session_state.slide >= data["starting_slide"] + text_slide_offset - 1
        ]

        player_cols = st.columns(len(visible_players))

        for index, ((player, data), player_col) in enumerate(
            zip(visible_players, player_cols),
            start=1
        ):
            with player_col:
                st.header(player)

                st.markdown(
                    f"""
                    <div class="score-value">
                        {data['score']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                minus, plus = st.columns(2)
                minusShortcut = str(index) if points_inverted_shortcut else f"{points_modifier_shortcut}+{index}"
                plusShortcut = f"{points_modifier_shortcut}+{index}" if points_inverted_shortcut else str(index)

                with minus:
                    with st.container(horizontal=True, horizontal_alignment="right"):
                        if st.button(
                            "-",
                            key=f"minus_{player}",
                            shortcut=minusShortcut,
                            type=points_buttons_css_type
                        ):
                            st.session_state.players[player]["score"] -= 1
                            st.session_state.pending_lose_sound = time.time()
                            st.rerun()

                with plus:
                    if st.button(
                        "+",
                        key=f"plus_{player}",
                        shortcut=plusShortcut,
                        type=points_buttons_css_type
                    ):
                        st.session_state.players[player]["score"] += 1
                        st.session_state.pending_gain_sound = time.time()
                        st.rerun()

# ==================================================
# Plays slide changed sound
# ==================================================
if slide_sound_enabled and slide_changed and not winner_slide:
    st.audio(
        slide_sound_bytes + f"SLIDE:{st.session_state.slide}".encode(),
        autoplay=True,
        format="audio/wav",
    )

st.session_state.last_slide = st.session_state.slide

# ==================================================
# Plays gain point sound
# ==================================================
if gain_points_sound_enabled and st.session_state.pending_gain_sound is not None:
    elapsed = time.time() - st.session_state.pending_gain_sound

    if elapsed >= gain_points_sound_delay_seconds:
        st.audio(
            gain_points_sound_bytes + bytes([int(time.time() * 1000) % 256]),
            autoplay=True,
            format="audio/wav",
        )

        st.session_state.pending_gain_sound = None

    else:
        time.sleep(0.1)
        st.rerun()

# ==================================================
# Plays lost point sound
# ==================================================
if lose_points_sound_enabled and st.session_state.pending_lose_sound is not None:
    elapsed = time.time() - st.session_state.pending_lose_sound

    if elapsed >= lose_points_sound_delay_seconds:
        st.audio(
            lose_points_sound_bytes + bytes([int(time.time() * 1000) % 256]),
            autoplay=True,
            format="audio/wav",
        )

        st.session_state.pending_lose_sound = None

    else:
        time.sleep(0.1)
        st.rerun()
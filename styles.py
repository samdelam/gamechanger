import streamlit as st

from assets import DSEG7_FONT_PATH, TRADE_GOTHIC_FONT_PATH, load_font


SCOREBOARD_HEIGHT = "23vh"
SLIDES_MARGIN = "2vmin"


def inject_font_css():
    dseg7_classic = load_font(DSEG7_FONT_PATH)
    trade_gothic_bold_condensed = load_font(TRADE_GOTHIC_FONT_PATH)

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
        unsafe_allow_html=True,
    )


def inject_app_css(scoreboard_enabled=True):
    if scoreboard_enabled:
        slides_height = f"calc(100vh - {SCOREBOARD_HEIGHT} - ({SLIDES_MARGIN} * 2))"
    else:
        slides_height = f"calc(100vh - ({SLIDES_MARGIN} * 2))"

    st.markdown(
        f"""
        <style>

        /* overwrites default font */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'TradeGothicBoldCondensed' !important;
        }}
        h1,h2,h3,h4,h5,h6,p,span,div,button {{
            font-family: 'TradeGothicBoldCondensed' !important;
        }}
        [data-testid="stIconMaterial"],
        [data-testid="stIconMaterial"] * {{
            font-family: "Material Symbols Rounded" !important;
        }}

        /* overall black blackground */
        [data-testid="stAppViewContainer"] {{ background: black; }}
        header[data-testid="stHeader"]     {{ display: none !important; }}

        [data-testid="stMainBlockContainer"] {{
            padding: 0 !important;
            max-width: 100% !important;
        }}

        /* removes gap around the slide */
        [data-testid="stVerticalBlock"] {{ gap: 0 !important; }}

        .st-key-slides {{
            box-sizing: border-box;
            min-height: {slides_height};
            max-height: {slides_height};
            padding: 4vmin;
            display: flex !important;
            flex-direction: column;
            justify-content: center !important;
            align-items: center !important;
            text-align: center;
            width: calc(100% - ({SLIDES_MARGIN} * 2));
            position: relative;
            background: #dcdcdc;
            border-radius: 10vmin;
            margin: {SLIDES_MARGIN};
            box-shadow: inset 0 0 0 1px rgba(0,0,0,.08);
            color: #111111;

            button[kind="secondary"] {{
                color: #dcdcdc;
                background: #111111;
            }}
            /* Slide navigation is positioned explicitly via its keyed wrapper.
               Avoid targeting generic .stHorizontalBlock:last-child because nested
               horizontal containers can overlap and block clicks. */
            .st-key-slide_navigation {{
                width: auto;
                position: absolute;
                bottom: 2rem;
                left: 2rem;
                right: 2rem;
            }}
        }}

        /* Keep both slide navigation buttons vertically aligned while allowing
           the next button to stay right-aligned inside its horizontal container. */
        .st-key-slides .st-key-slide_previous_nav,
        .st-key-slides .st-key-slide_settings_nav,
        .st-key-slides .st-key-slide_next_nav {{
            display: flex !important;
            align-items: center !important;
            min-height: 40px;
        }}

        .st-key-slides .st-key-slide_previous_nav,
        .st-key-slides .st-key-slide_settings_nav {{
            justify-content: flex-start !important;
        }}

        .st-key-slides .st-key-slide_next_nav {{
            justify-content: flex-end !important;
        }}

        .st-key-slides .st-key-slide_previous_nav .stButton,
        .st-key-slides .st-key-slide_settings_nav .stButton,
        .st-key-slides .st-key-slide_next_nav .stButton {{
            display: flex !important;
            align-items: center !important;
            margin: 0 !important;
        }}

        .st-key-scoreboard {{
            position: fixed;
            bottom: 0; left: 0;
            width: 100%;
            background: black;
            padding: 1vmin 10vw;
            z-index: 999;
            height: {SCOREBOARD_HEIGHT};

            .stElementContainer {{ text-align: center; }}
            h2 {{
                font-size: 4.5vmin !important;
                padding: 1vmin 0;
            }}
            button[kind="secondary"] {{
                margin-top: 2vmin;
                width: 4vmin !important;
                min-width: 4vmin !important;
                height: 4vmin !important;
                min-height: 4vmin !important;
                padding: 0;
            }}
        }}

        /* hides the shortcut tooltip from buttons */
        .stButton kbd {{ display: none; }}

        /* scores custom class for different font and color */
        .score-value {{
            font-family: 'DSEG7', monospace !important;
            color: #ff2a2a !important;
            text-shadow: 0 0 5px #ff2a2a, 0 0 10px #ff2a2a, 0 0 20px #ff2a2a;
            font-size: 5.2vmin !important;
            font-weight: normal !important;
        }}

        button[kind="tertiary"] {{ display: none; }}

        </style>
        """,
        unsafe_allow_html=True,
    )

    st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")


def cover_slide_css():
    st.markdown(
        f"""
        <style>
        .st-key-slides {{
            padding: 0 !important;
            overflow: hidden;
            min-height: calc(100vh - ({SLIDES_MARGIN} * 2)) !important;
            max-height: calc(100vh - ({SLIDES_MARGIN} * 2)) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_settings_editor_css():
    """Editor-only CSS. This overrides the global slide layout only while editing."""
    st.markdown(
        """
        <style>
        /* Settings screen shell only. Keeps slide/scoreboard styling untouched. */
        [data-testid="stMainBlockContainer"] {
            padding: 2rem clamp(1rem, 4vw, 4rem) 3rem !important;
            max-width: 1200px !important;
            margin: 0 auto !important;
        }

        .st-key-settings_editor {
            box-sizing: border-box;
            background: linear-gradient(180deg, #181818 0%, #101010 100%);
            color: #f2f2f2;
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 2rem;
            padding: 1.5rem 2rem 2rem;
            min-height: calc(100vh - 4rem);
            box-shadow: 0 24px 60px rgba(0,0,0,.35);
        }

        .st-key-settings_editor h1,
        .st-key-settings_editor h2,
        .st-key-settings_editor h3,
        .st-key-settings_editor p,
        .st-key-settings_editor label,
        .st-key-settings_editor span,
        .st-key-settings_editor div {
            color: #f2f2f2;
        }

        .st-key-settings_editor small,
        .st-key-settings_editor [data-testid="stWidgetLabel"],
        .st-key-settings_editor [data-testid="stWidgetLabel"] * {
            color: #d8d8d8 !important;
        }

        .st-key-settings_editor hr {
            border-color: rgba(255,255,255,.16) !important;
        }

        /* Tabs */
        .st-key-settings_editor [data-testid="stTabs"] {
            margin-top: .75rem;
        }

        .st-key-settings_editor [data-baseweb="tab-list"] {
            gap: .4rem;
            border-bottom: 1px solid rgba(255,255,255,.14);
        }

        .st-key-settings_editor [data-baseweb="tab"] {
            background: #242424;
            border: 1px solid rgba(255,255,255,.12);
            border-radius: .85rem .85rem 0 0;
            padding: .45rem .9rem;
        }

        .st-key-settings_editor [data-baseweb="tab"] p,
        .st-key-settings_editor [data-baseweb="tab"] span {
            color: #eaeaea !important;
        }

        .st-key-settings_editor [aria-selected="true"] {
            background: #333333 !important;
            border-color: rgba(255,255,255,.24) !important;
        }

        /* Inputs */
        .st-key-settings_editor [data-testid="stTextInput"],
        .st-key-settings_editor [data-testid="stNumberInput"],
        .st-key-settings_editor [data-testid="stFileUploader"] {
            max-width: 360px;
        }

        .st-key-settings_editor input,
        .st-key-settings_editor textarea,
        .st-key-settings_editor [data-baseweb="input"] {
            background: #242424 !important;
            color: #f8f8f8 !important;
            border-color: rgba(255,255,255,.22) !important;
        }

        .st-key-settings_editor input::placeholder,
        .st-key-settings_editor textarea::placeholder {
            color: #a8a8a8 !important;
        }

        .st-key-settings_editor [data-baseweb="input"]:focus-within {
            border-color: rgba(255,255,255,.55) !important;
            box-shadow: 0 0 0 1px rgba(255,255,255,.3) !important;
        }

        /* Checkboxes */
        .st-key-settings_editor [data-testid="stCheckbox"] label,
        .st-key-settings_editor [data-testid="stCheckbox"] p {
            color: #f2f2f2 !important;
        }

        /* File uploader */
        .st-key-settings_editor [data-testid="stFileUploaderDropzone"] {
            background: #202020 !important;
            border-color: rgba(255,255,255,.22) !important;
        }

        .st-key-settings_editor [data-testid="stFileUploaderDropzone"] small,
        .st-key-settings_editor [data-testid="stFileUploaderDropzone"] span,
        .st-key-settings_editor [data-testid="stFileUploaderDropzone"] p {
            color: #e7e7e7 !important;
        }

        /* Expanders */
        .st-key-settings_editor [data-testid="stExpander"] {
            background: #1f1f1f;
            border: 1px solid rgba(255,255,255,.14);
            border-radius: 1rem;
            overflow: hidden;
            margin-top: 1rem;
        }

        .st-key-settings_editor [data-testid="stExpander"] summary,
        .st-key-settings_editor [data-testid="stExpander"] summary * {
            color: #f6f6f6 !important;
        }

        .st-key-settings_editor [data-testid="stExpanderDetails"] {
            background: #181818;
            border-top: 1px solid rgba(255,255,255,.10);
        }

        /* Alerts */
        .st-key-settings_editor [data-testid="stAlert"] div,
        .st-key-settings_editor [data-testid="stAlert"] p,
        .st-key-settings_editor [data-testid="stAlert"] span {
            color: inherit !important;
        }

        /* Buttons: compact, readable, dark-friendly */
        .st-key-settings_editor .stButton > button,
        .st-key-settings_editor [data-testid="stDownloadButton"] > button {
            width: auto !important;
            min-width: 0 !important;
            padding-left: 1rem;
            padding-right: 1rem;
            border-radius: .8rem;
            border: 1px solid rgba(255,255,255,.18) !important;
        }

        .st-key-settings_editor button[kind="secondary"],
        .st-key-settings_editor [data-testid="stDownloadButton"] button {
            background: #2a2a2a !important;
            color: #f5f5f5 !important;
        }

        .st-key-settings_editor button[kind="secondary"]:hover,
        .st-key-settings_editor [data-testid="stDownloadButton"] button:hover {
            background: #383838 !important;
            color: #ffffff !important;
            border-color: rgba(255,255,255,.34) !important;
        }

        .st-key-settings_editor button[kind="primary"] {
            color: #ffffff !important;
        }

        .st-key-settings_editor [data-testid="stHorizontalBlock"] {
            gap: .75rem;
        }

        /* Keep Material icons readable after global font override. */
        .st-key-settings_editor [data-testid="stIconMaterial"],
        .st-key-settings_editor [data-testid="stIconMaterial"] * {
            font-family: "Material Symbols Rounded" !important;
            color: inherit !important;
        }

        @media (max-width: 800px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem !important;
            }
            .st-key-settings_editor {
                padding: 1rem;
                border-radius: 1.25rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

import streamlit as st

from assets import find_cover_image
from audio import play_pending_audio
from scoreboard import render_scoreboard
from settings_editor import render_settings_editor
from slides import render_slide_area
from state import init_session_state, slide_changed
from styles import inject_app_css, inject_font_css


st.set_page_config(
    page_title="Game Changer",
    layout="wide",
)

# Assets and derived slide offsets
inject_font_css()
cover_image = find_cover_image()
has_cover = cover_image is not None
text_slide_offset = 1 if has_cover else 0

# Runtime state
init_session_state(text_slide_offset)
changed_slide = slide_changed()

# Global app styling
inject_app_css()

# Main routing
is_cover_slide = False
winner_slide = False

if st.session_state.edit_mode:
    render_settings_editor(text_slide_offset)
else:
    is_cover_slide, winner_slide = render_slide_area(
        cover_image=cover_image,
        has_cover=has_cover,
        text_slide_offset=text_slide_offset,
    )

render_scoreboard(
    text_slide_offset=text_slide_offset,
    is_cover_slide=is_cover_slide,
)

play_pending_audio(
    slide_changed=changed_slide,
    winner_slide=winner_slide,
)

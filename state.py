import streamlit as st

from config_manager import apply_config, load_startup_config


def init_session_state(text_slide_offset):
    """Initialize all session state needed by the app."""
    if "config" not in st.session_state:
        apply_config(load_startup_config(), text_slide_offset)

    if "pending_gain_sound" not in st.session_state:
        st.session_state.pending_gain_sound = None
    if "pending_lose_sound" not in st.session_state:
        st.session_state.pending_lose_sound = None
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False
    if "slide" not in st.session_state:
        st.session_state.slide = 0
    if "last_slide" not in st.session_state:
        st.session_state.last_slide = st.session_state.slide

    # Incremented each time a new draft is loaded so every widget gets a fresh
    # key and Streamlit no longer ignores the new value= argument.
    if "form_generation" not in st.session_state:
        st.session_state.form_generation = 0


def slide_changed():
    return st.session_state.slide != st.session_state.last_slide

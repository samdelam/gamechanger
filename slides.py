import streamlit as st

from styles import cover_slide_css


def _render_cover_slide(cover_image):
    cover_slide_css()
    st.image(cover_image, width="stretch")


def _render_winner_slide():
    ss = st.session_state

    eligible_players = [
        (name, data)
        for name, data in ss.players.items()
        if data["can_win"]
    ]

    highest_score = max(data["score"] for _, data in eligible_players)
    winners = [name for name, data in eligible_players if data["score"] == highest_score]

    if len(winners) == 1:
        title = ss.winner_single_title
        text = winners[0]
        score = ss.winner_single_score.format(score=highest_score)
    else:
        title = ss.winner_multiple_title
        score = ss.winner_multiple_score.format(score=highest_score)
        separator = ss.winner_separator
        text = (
            f"{winners[0]} {separator} {winners[1]}"
            if len(winners) == 2
            else ", ".join(winners[:-1]) + f" {separator} {winners[-1]}"
        )

    st.markdown(
        f"""
        <div style="text-align:center;font-size:8vmin;font-weight:600">{title}</div>
        <div style="text-align:center;font-size:12vmin;font-weight:800">{text}</div>
        <div style="text-align:center;font-size:8vmin;font-weight:600">{score}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_text_slide(current_slide):
    font_size = (
        max(4.5, min(15, 70 / (len(current_slide) ** 0.5)))
        if current_slide
        else 15
    )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:{font_size}vmin;
            font-weight:600;
            line-height:1.4;
        ">{current_slide}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_slide_navigation(text_slide_offset):
    ss = st.session_state

    # Keep the absolute positioning on this wrapper only. The inner horizontal
    # containers align the buttons without covering each other.
    with st.container(key="slide_navigation"):
        col1, col2 = st.columns(2)

        with col1:
            if ss.slide > 0:
                with st.container(horizontal=True, horizontal_alignment="left", key="slide_previous_nav"):
                    if st.button("⬅", shortcut=ss.slide_previous_shortcut, type=ss.slide_buttons_css_type):
                        ss.slide -= 1
                        st.rerun()
            else:
                with st.container(horizontal=True, horizontal_alignment="left", key="slide_settings_nav"):
                    if st.button("⚙️", shortcut=ss.settings_shortcut, type=ss.settings_button_css_type):
                        ss.edit_mode = True
                        st.rerun()

        max_slide = (
            len(ss.slides) if ss.winner_enabled else len(ss.slides) - 1
        ) + text_slide_offset

        with col2:
            if ss.slide < max_slide:
                with st.container(horizontal=True, horizontal_alignment="right", key="slide_next_nav"):
                    if st.button("➡", shortcut=ss.slide_next_shortcut, type=ss.slide_buttons_css_type):
                        ss.slide += 1
                        st.rerun()


def render_slide_area(cover_image, has_cover, text_slide_offset):
    ss = st.session_state

    with st.container(key="slides"):
        is_cover_slide = has_cover and ss.slide == 0
        winner_slide = ss.winner_enabled and ss.slide == len(ss.slides) + text_slide_offset

        current_slide = ""
        if not is_cover_slide and not winner_slide:
            text_slide_index = ss.slide - text_slide_offset
            current_slide = (
                ss.slides[text_slide_index]
                if 0 <= text_slide_index < len(ss.slides)
                else ""
            )

        if is_cover_slide:
            _render_cover_slide(cover_image)
        elif winner_slide:
            _render_winner_slide()
        else:
            _render_text_slide(current_slide)

        _render_slide_navigation(text_slide_offset)

    return is_cover_slide, winner_slide

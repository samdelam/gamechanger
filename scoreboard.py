import time

import streamlit as st


def render_scoreboard(text_slide_offset, is_cover_slide):
    if st.session_state.edit_mode or is_cover_slide:
        return

    ss = st.session_state

    with st.container(key="scoreboard"):
        visible_players = [
            (name, data)
            for name, data in ss.players.items()
            if ss.slide >= data["starting_slide"] + text_slide_offset - 1
        ]

        for index, ((player, data), col) in enumerate(
            zip(visible_players, st.columns(len(visible_players))),
            start=1,
        ):
            with col:
                st.header(player)
                st.markdown(
                    f'<div class="score-value">{data["score"]}</div>',
                    unsafe_allow_html=True,
                )

                minus_col, plus_col = st.columns(2)
                minus_shortcut = (
                    str(index)
                    if ss.points_inverted_shortcut
                    else f"{ss.points_modifier_shortcut}+{index}"
                )
                plus_shortcut = (
                    f"{ss.points_modifier_shortcut}+{index}"
                    if ss.points_inverted_shortcut
                    else str(index)
                )

                with minus_col:
                    with st.container(horizontal=True, horizontal_alignment="right"):
                        if st.button(
                            "-",
                            key=f"minus_{player}",
                            shortcut=minus_shortcut,
                            type=ss.points_buttons_css_type,
                        ):
                            ss.players[player]["score"] -= 1
                            ss.pending_lose_sound = time.time() if ss.lose_points_sound_enabled else None
                            st.rerun()

                with plus_col:
                    if st.button(
                        "+",
                        key=f"plus_{player}",
                        shortcut=plus_shortcut,
                        type=ss.points_buttons_css_type,
                    ):
                        ss.players[player]["score"] += 1
                        ss.pending_gain_sound = time.time() if ss.gain_points_sound_enabled else None
                        st.rerun()

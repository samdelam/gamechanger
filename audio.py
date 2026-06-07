import time

import streamlit as st


def play_pending_audio(slide_changed, winner_slide):
    ss = st.session_state

    if ss.slide_sound_enabled and slide_changed and not winner_slide:
        st.audio(
            ss.slide_sound_bytes + f"SLIDE:{ss.slide}".encode(),
            autoplay=True,
            format="audio/wav",
        )

    ss.last_slide = ss.slide

    if ss.gain_points_sound_enabled and ss.pending_gain_sound is not None:
        elapsed = time.time() - ss.pending_gain_sound
        if elapsed >= ss.gain_points_sound_delay_seconds:
            st.audio(
                ss.gain_points_sound_bytes + bytes([int(time.time() * 1000) % 256]),
                autoplay=True,
                format="audio/wav",
            )
            ss.pending_gain_sound = None
        else:
            time.sleep(0.1)
            st.rerun()

    if ss.lose_points_sound_enabled and ss.pending_lose_sound is not None:
        elapsed = time.time() - ss.pending_lose_sound
        if elapsed >= ss.lose_points_sound_delay_seconds:
            st.audio(
                ss.lose_points_sound_bytes + bytes([int(time.time() * 1000) % 256]),
                autoplay=True,
                format="audio/wav",
            )
            ss.pending_lose_sound = None
        else:
            time.sleep(0.1)
            st.rerun()

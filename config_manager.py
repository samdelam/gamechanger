import json
import streamlit as st

from assets import CONFIG_FILE_PATH, GAIN_POINT_SOUND_PATH, LOSE_POINT_SOUND_PATH, SLIDE_SOUND_PATH, read_asset_bytes


# ==================================================
# Canonical defaults
# ==================================================
# This is the single source of default values for the game and settings editor.
CONFIG_DEFAULTS = {
    "slides": [
        "FIRST PROMPT",
        "NEXT SLIDE IS EMPTY",
        "",
        "A VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY BIG PROMPT",
        "DON'T SWEAR",
        "END OF GAME",
    ],
    "players": [
        {"name": "VIC", "starting_score": 50, "starting_slide": 1, "can_win": True},
        {"name": "JACOB", "starting_score": 50, "starting_slide": 1, "can_win": True},
        {"name": "LOU", "starting_score": 50, "starting_slide": 1, "can_win": True},
        {"name": "SWEAR JAR", "starting_score": 0, "starting_slide": 5, "can_win": False},
    ],
    "sounds": {
        "slide": True,
        "gain_points": True,
        "gain_points_delay_seconds": 0.5,
        "lose_points": True,
        "lose_points_delay_seconds": 0.5,
    },
    "buttons": {
        "slide": True,
        "points": True,
        "settings": True,
    },
    "shortcuts": {
        "slide_next": "ArrowRight",
        "slide_previous": "ArrowLeft",
        "settings": "s",
        "points_modifier": "Shift",
        "points_inverted": False,
    },
    "winner": {
        "enabled": True,
        "single": {
            "title": "AND THE WINNER IS:",
            "score_text": "WITH {score} POINTS",
        },
        "multiple": {
            "title": "AND THE WINNERS ARE:",
            "separator": "AND",
            "score_text": "WITH {score} POINTS",
        },
    },
}


def deep_merge(base, override):
    """Recursively merge *override* into a copy of *base*."""
    result = dict(base)

    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def load_config(source=None):
    """
    Return a fully-defaulted config dict.

    *source* may be:
      - None          → use hardcoded defaults only
      - dict          → merge an already-parsed imported/exported config
      - str / bytes   → parse imported/exported JSON text and merge it

    This function does not read config.json by itself. Use load_startup_config()
    when booting the app so local users can override defaults with a root
    config.json file.
    """
    if source is None:
        raw = {}
    elif isinstance(source, dict):
        raw = source
    else:
        raw = json.loads(source)

    return deep_merge(CONFIG_DEFAULTS, raw)


def load_startup_config():
    """
    Load the initial app config.

    If a config.json file exists in the project root, merge it over the
    hardcoded defaults and use it as the runtime config. If it is missing,
    fall back to the hardcoded defaults.
    """
    if CONFIG_FILE_PATH.exists():
        with CONFIG_FILE_PATH.open("r", encoding="utf-8") as file:
            return load_config(file.read())

    return load_config()


def load_players(config):
    """Build the live players dict from config."""
    return {
        player["name"]: {
            "score": player["starting_score"],
            "starting_slide": player["starting_slide"],
            "can_win": player["can_win"],
        }
        for player in config["players"]
    }


def apply_config(config, text_slide_offset=0):
    """
    Unpack every runtime variable from *config* into session_state and reload
    sound bytes as needed.
    """
    ss = st.session_state

    ss.config = config
    ss.slides = list(config["slides"])
    ss.players = load_players(config)

    # Sounds
    sounds = config["sounds"]
    ss.slide_sound_enabled = sounds["slide"]
    ss.gain_points_sound_enabled = sounds["gain_points"]
    ss.gain_points_sound_delay_seconds = sounds["gain_points_delay_seconds"]
    ss.lose_points_sound_enabled = sounds["lose_points"]
    ss.lose_points_sound_delay_seconds = sounds["lose_points_delay_seconds"]

    # Do not keep delayed audio queued when that sound is disabled.
    if not ss.gain_points_sound_enabled:
        ss.pending_gain_sound = None
    if not ss.lose_points_sound_enabled:
        ss.pending_lose_sound = None

    if ss.slide_sound_enabled:
        ss.slide_sound_bytes = read_asset_bytes(SLIDE_SOUND_PATH)
    if ss.gain_points_sound_enabled:
        ss.gain_points_sound_bytes = read_asset_bytes(GAIN_POINT_SOUND_PATH)
    if ss.lose_points_sound_enabled:
        ss.lose_points_sound_bytes = read_asset_bytes(LOSE_POINT_SOUND_PATH)

    # Buttons
    buttons = config["buttons"]
    ss.slide_buttons_css_type = "secondary" if buttons["slide"] else "tertiary"
    ss.points_buttons_css_type = "secondary" if buttons["points"] else "tertiary"
    ss.settings_button_css_type = "secondary" if buttons["settings"] else "tertiary"

    # Shortcuts
    shortcuts = config["shortcuts"]
    ss.slide_next_shortcut = shortcuts["slide_next"]
    ss.slide_previous_shortcut = shortcuts["slide_previous"]
    ss.settings_shortcut = shortcuts["settings"]
    ss.points_modifier_shortcut = shortcuts["points_modifier"]
    ss.points_inverted_shortcut = shortcuts["points_inverted"]

    # Winner
    winner = config["winner"]
    ss.winner_enabled = winner["enabled"]

    if ss.winner_enabled:
        ss.winner_single_title = winner["single"]["title"]
        ss.winner_single_score = winner["single"]["score_text"]
        ss.winner_multiple_title = winner["multiple"]["title"]
        ss.winner_separator = winner["multiple"]["separator"]
        ss.winner_multiple_score = winner["multiple"]["score_text"]

    # Keep the current slide inside the valid range after settings changes.
    if "slide" in ss:
        max_slide = (
            len(ss.slides) + text_slide_offset
            if ss.winner_enabled
            else len(ss.slides) - 1 + text_slide_offset
        )
        ss.slide = min(ss.slide, max(0, max_slide))

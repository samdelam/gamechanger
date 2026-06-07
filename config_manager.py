import json
import streamlit as st

from assets import CONFIG_FILE_PATH, GAIN_POINT_SOUND_PATH, LOSE_POINT_SOUND_PATH, SLIDE_SOUND_PATH, read_asset_bytes


# ==================================================
# Canonical defaults
# ==================================================
# This is the single source of default values for the game and settings editor.
CONFIG_DEFAULTS = {
    "players": [
        {"name": "VIC", "starting_score": 50, "starting_slide": 1, "can_win": True},
        {"name": "JACOB", "starting_score": 50, "starting_slide": 1, "can_win": True},
        {"name": "LOU", "starting_score": 50, "starting_slide": 1, "can_win": True},
        {"name": "SWEAR JAR", "starting_score": 0, "starting_slide": 5, "can_win": False},
    ],
    "slides": {
        "content": [
            "FIRST PROMPT",
            "NEXT SLIDE IS EMPTY",
            "",
            "A VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY BIG PROMPT",
            "DON'T SWEAR",
            "END OF GAME",
        ],
        "buttons": {
            "slide": True,
            "settings": True,
        },
        "shortcuts": {
            "slide_next": "ArrowRight",
            "slide_previous": "ArrowLeft",
            "settings": "S",
        },
        "sounds": {
            "slide": True,
        },
    },
    "scoreboard": {
        "enabled": True,
        "buttons": {
            "points": True,
        },
        "shortcuts": {
            "points_modifier": "Shift",
            "points_inverted": False,
        },
        "sounds": {
            "gain_points": True,
            "gain_points_delay_seconds": 0.5,
            "lose_points": True,
            "lose_points_delay_seconds": 0.5,
        },
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
    ss.slides = list(config["slides"]["content"])
    ss.players = load_players(config)

    # Slide settings
    slide_settings = config["slides"]
    slide_buttons = slide_settings["buttons"]
    slide_shortcuts = slide_settings["shortcuts"]
    slide_sounds = slide_settings["sounds"]

    ss.slide_buttons_css_type = "secondary" if slide_buttons["slide"] else "tertiary"
    ss.settings_button_css_type = "secondary" if slide_buttons["settings"] else "tertiary"
    ss.slide_next_shortcut = slide_shortcuts["slide_next"]
    ss.slide_previous_shortcut = slide_shortcuts["slide_previous"]
    ss.settings_shortcut = slide_shortcuts["settings"]
    ss.slide_sound_enabled = slide_sounds["slide"]

    # Scoreboard settings
    scoreboard = config["scoreboard"]
    scoreboard_buttons = scoreboard["buttons"]
    scoreboard_shortcuts = scoreboard["shortcuts"]
    scoreboard_sounds = scoreboard["sounds"]

    ss.scoreboard_enabled = scoreboard["enabled"]
    ss.points_buttons_css_type = "secondary" if scoreboard_buttons["points"] else "tertiary"
    ss.points_modifier_shortcut = scoreboard_shortcuts["points_modifier"]
    ss.points_inverted_shortcut = scoreboard_shortcuts["points_inverted"]

    ss.gain_points_sound_enabled = scoreboard_sounds["gain_points"]
    ss.gain_points_sound_delay_seconds = scoreboard_sounds["gain_points_delay_seconds"]
    ss.lose_points_sound_enabled = scoreboard_sounds["lose_points"]
    ss.lose_points_sound_delay_seconds = scoreboard_sounds["lose_points_delay_seconds"]

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

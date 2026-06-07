# CONFIG_SCHEMA describes the editor UI only: labels, layout, widget types,
# and conditions. It intentionally does not contain default values.
# CONFIG_DEFAULTS in config_manager.py is the single source of defaults.
CONFIG_SCHEMA = [
    {
        "section": "players",
        "label": "Players",
        "type": "player_list",
        "item_fields": [
            {"type": "text", "label": "Name", "key": "name"},
            {"type": "number", "label": "Starting score", "key": "starting_score"},
            {"type": "number", "label": "Starting slide", "key": "starting_slide"},
            {"type": "checkbox", "label": "Can win", "key": "can_win"},
        ],
    },
    {
        "section": "slides",
        "label": "Slides",
        "type": "slide_list",
        "fields": [
            {
                "type": "group",
                "group_label": "### Slide buttons",
                "group_key": "buttons",
                "fields": [
                    {"type": "checkbox", "label": "Slide buttons", "key": "slide"},
                    {"type": "checkbox", "label": "Settings button", "key": "settings"},
                ],
            },
            {
                "type": "group",
                "group_label": "### Slide shortcuts",
                "group_key": "shortcuts",
                "fields": [
                    {"type": "text", "label": "Next slide key", "key": "slide_next"},
                    {"type": "text", "label": "Previous slide key", "key": "slide_previous"},
                    {"type": "text", "label": "Open settings key", "key": "settings"},
                ],
            },
            {
                "type": "group",
                "group_label": "### Slide sounds",
                "group_key": "sounds",
                "fields": [
                    {"type": "checkbox", "label": "Slide sound", "key": "slide"},
                ],
            },
        ],
    },
    {
        "section": "scoreboard",
        "label": "Scoreboard",
        "type": "section",
        "fields": [
            {"type": "checkbox", "label": "Show scoreboard", "key": "enabled"},
            {
                "type": "group",
                "group_label": "### Scoreboard buttons",
                "group_key": "buttons",
                "condition": lambda values: values.get("enabled", False),
                "fields": [
                    {"type": "checkbox", "label": "Points buttons", "key": "points"},
                ],
            },
            {
                "type": "group",
                "group_label": "### Scoreboard sounds",
                "group_key": "sounds",
                "condition": lambda values: values.get("enabled", False),
                "layout": "columns",
                "columns": [
                    [
                        {"type": "checkbox", "label": "Gain points sound", "key": "gain_points"},
                        {
                            "type": "number",
                            "label": "Gain sound delay (seconds)",
                            "key": "gain_points_delay_seconds",
                            "step": 0.1,
                            "condition": lambda values: values.get("gain_points", True),
                        },
                    ],
                    [
                        {"type": "checkbox", "label": "Lose points sound", "key": "lose_points"},
                        {
                            "type": "number",
                            "label": "Lose sound delay (seconds)",
                            "key": "lose_points_delay_seconds",
                            "step": 0.1,
                            "condition": lambda values: values.get("lose_points", True),
                        },
                    ],
                ],
            },
            {
                "type": "group",
                "group_label": "### Scoreboard shortcuts",
                "group_key": "shortcuts",
                "condition": lambda values: values.get("enabled", False),
                "description": (
                    "Point shortcuts are assigned by player order. Press a number key "
                    "such as 1, 2, 3, and so on to add one point to that player. "
                    "Press Shift+number, such as Shift+1 or Shift+2, to remove one point. "
                    "Change the Points Modifier key to use a modifier other than Shift. "
                    "Enable Invert point shortcuts to reverse that behavior, making the "
                    "number key remove points and modifier+number add points instead."
                ),
                "fields": [
                    {"type": "text", "label": "Points Modifier key", "key": "points_modifier"},
                    {"type": "checkbox", "label": "Invert point shortcuts", "key": "points_inverted"},
                ],
            },
        ],
    },
    {
        "section": "winner",
        "label": "Winner Screen",
        "type": "section",
        "fields": [
            {"type": "checkbox", "label": "Enable winner screen", "key": "enabled"},
            {
                "type": "group",
                "group_label": "### Single winner",
                "group_key": "single",
                "condition": lambda values: values.get("enabled", False),
                "fields": [
                    {"type": "text", "label": "Title", "key": "title"},
                    {"type": "text", "label": "Score text", "key": "score_text"},
                ],
            },
            {
                "type": "group",
                "group_label": "### Multiple winners (Tie)",
                "group_key": "multiple",
                "condition": lambda values: values.get("enabled", False),
                "fields": [
                    {"type": "text", "label": "Title", "key": "title"},
                    {"type": "text", "label": "Separator", "key": "separator"},
                    {"type": "text", "label": "Score text", "key": "score_text"},
                ],
            },
        ],
    },
]

import json
from copy import deepcopy

import streamlit as st

from config_manager import CONFIG_DEFAULTS, apply_config, load_config
from settings_schema import CONFIG_SCHEMA
from styles import inject_settings_editor_css


def _path_get(data, path, fallback=None):
    """Read a nested value from a dict/list path."""
    ref = data

    for part in path:
        try:
            ref = ref[part]
        except (KeyError, IndexError, TypeError):
            return fallback

    return ref


def _field_default(default_path):
    """Return the canonical default for a field from CONFIG_DEFAULTS only."""
    return _path_get(CONFIG_DEFAULTS, default_path)


def _new_player(player_number):
    """Build a new player using canonical defaults as the template."""
    default_player = _path_get(CONFIG_DEFAULTS, ["players", 0], {}) or {}

    return {
        "name": f"PLAYER {player_number}",
        "starting_score": default_player.get("starting_score", 0),
        "starting_slide": default_player.get("starting_slide", 1),
        "can_win": default_player.get("can_win", True),
    }


def _new_slide():
    """Build a new empty slide."""
    return ""


def _stage_players(players):
    """Persist the current player editor draft and refresh dynamic widget keys."""
    st.session_state.edit_draft["players"] = players
    st.session_state.form_generation += 1
    st.rerun()


def _stage_slides(slides):
    """Persist the current slide editor draft and refresh dynamic widget keys."""
    st.session_state.edit_draft["slides"] = slides
    st.session_state.form_generation += 1
    st.rerun()


def _widget_value(source_data, field_key, default_path):
    """Value used to populate widgets: source first, canonical defaults second."""
    if isinstance(source_data, dict) and field_key in source_data:
        return source_data[field_key]

    return _field_default(default_path)


def _move_item(items, index, direction):
    """Return a reordered copy of *items* moving index by direction (-1 or +1)."""
    new_items = list(items)
    target = index + direction

    if 0 <= index < len(new_items) and 0 <= target < len(new_items):
        new_items[index], new_items[target] = new_items[target], new_items[index]

    return new_items


def _render_field(field, current_values, source_data, key_prefix, gen, default_path):
    """Render one leaf widget; return (key, value) or None if condition fails."""
    condition = field.get("condition")
    if condition and not condition(current_values):
        return None

    field_type = field["type"]
    label = field["label"]
    field_key = field["key"]
    value = _widget_value(source_data, field_key, default_path)
    widget_key = f"g{gen}__{key_prefix}__{field_key}"

    if field_type == "text":
        result = st.text_input(label, value=value or "", key=widget_key)
    elif field_type == "number":
        result = st.number_input(label, value=value, step=field.get("step", 1), key=widget_key)
    elif field_type == "checkbox":
        result = st.checkbox(label, value=bool(value), key=widget_key)
    else:
        return None

    return field_key, result


def _render_field_grid(fields, current_values, source_data, key_prefix, gen, default_path_builder, max_columns=3):
    """Render fields in compact rows instead of stretching every input full width."""
    output = {}
    visible_fields = []

    # Conditions can depend on values rendered earlier in the same section.
    for field in fields:
        condition = field.get("condition")
        if condition and not condition({**current_values, **output}):
            continue
        visible_fields.append(field)

    for start in range(0, len(visible_fields), max_columns):
        row_fields = visible_fields[start : start + max_columns]
        cols = st.columns(len(row_fields))

        for col, field in zip(cols, row_fields):
            with col:
                pair = _render_field(
                    field,
                    {**current_values, **output},
                    source_data,
                    key_prefix,
                    gen,
                    default_path_builder(field),
                )
                if pair:
                    output[pair[0]] = pair[1]

    return output


def _render_player_list(section_def, config, gen):
    output = {}
    players_out = []
    players_source = config.get("players", [])

    add_col, hint_col = st.columns([1, 5])
    with add_col:
        if st.button("➕ Add player", key=f"g{gen}__add_player_top", type="secondary"):
            _stage_players(players_source + [_new_player(len(players_source) + 1)])
    with hint_col:
        st.caption("Use ↑ and ↓ to reorder players.")

    if not players_source:
        st.info("No players yet. Add one to get started.")

    for index, player in enumerate(players_source):
        player_name = player.get("name") or f"Player {index + 1}"

        with st.expander(f"Player {index + 1}: {player_name}", expanded=False):
            fields = section_def["item_fields"]
            row = st.columns([3, 1.2, 1.2, 1.1, 0.75, 0.75, 1.4])
            player_values = {}

            for col, field in zip(row[:4], fields):
                with col:
                    pair = _render_field(
                        field,
                        player_values,
                        player,
                        f"player_{index}",
                        gen,
                        ["players", index, field["key"]],
                    )
                    if pair:
                        player_values[pair[0]] = pair[1]

            staged_players = players_out + [player_values] + players_source[index + 1 :]

            with row[4]:
                st.write(" ")
                st.write(" ")
                if st.button(
                    "↑",
                    key=f"g{gen}__move_player_up_{index}",
                    type="secondary",
                    disabled=index == 0,
                    help="Move player up",
                ):
                    _stage_players(_move_item(staged_players, index, -1))

            with row[5]:
                st.write(" ")
                st.write(" ")
                if st.button(
                    "↓",
                    key=f"g{gen}__move_player_down_{index}",
                    type="secondary",
                    disabled=index == len(players_source) - 1,
                    help="Move player down",
                ):
                    _stage_players(_move_item(staged_players, index, 1))

            with row[6]:
                st.write(" ")
                st.write(" ")
                if st.button(
                    "🗑️ Remove",
                    key=f"g{gen}__remove_player_{index}",
                    type="primary",
                    help="Remove this player",
                ):
                    _stage_players([player for idx, player in enumerate(staged_players) if idx != index])

            players_out.append(player_values)

    output["players"] = players_out
    return output


def _render_slide_list(config, gen):
    output = {}
    slides_out = []
    slides_source = config.get("slides", [])

    add_col, hint_col = st.columns([1, 5])
    with add_col:
        if st.button("➕ Add slide", key=f"g{gen}__add_slide_top", type="secondary"):
            _stage_slides(slides_source + [_new_slide()])
    with hint_col:
        st.caption("Use ↑ and ↓ to reorder slides.")

    if not slides_source:
        st.info("No slides yet. Add one to get started.")

    for index, slide_text in enumerate(slides_source):
        row = st.columns([1, 6, 0.75, 0.75, 1.4])

        with row[0]:
            st.write(" ")
            st.markdown(f"**Slide {index + 1}**")

        with row[1]:
            current_slide_text = st.text_input(
                "Slide text",
                value=slide_text,
                key=f"g{gen}__slide_{index}__text",
                label_visibility="collapsed",
            )

        staged_slides = slides_out + [current_slide_text] + slides_source[index + 1 :]

        with row[2]:
            if st.button(
                "↑",
                key=f"g{gen}__move_slide_up_{index}",
                type="secondary",
                disabled=index == 0,
                help="Move slide up",
            ):
                _stage_slides(_move_item(staged_slides, index, -1))

        with row[3]:
            if st.button(
                "↓",
                key=f"g{gen}__move_slide_down_{index}",
                type="secondary",
                disabled=index == len(slides_source) - 1,
                help="Move slide down",
            ):
                _stage_slides(_move_item(staged_slides, index, 1))

        with row[4]:
            if st.button(
                "🗑️ Remove",
                key=f"g{gen}__remove_slide_{index}",
                type="primary",
                help="Remove this slide",
            ):
                _stage_slides([slide for idx, slide in enumerate(staged_slides) if idx != index])

        slides_out.append(current_slide_text)

    output["slides"] = slides_out
    return output


def _render_regular_section(section_def, config, gen):
    output = {}
    section_key = section_def["section"]
    source = config.get(section_key, {})
    section_values = {}
    groups_out = {}
    groups_nested = section_def.get("groups_nested", True)
    first_group = True

    for field in section_def["fields"]:
        if field["type"] == "group":
            condition = field.get("condition")
            if condition and not condition(section_values):
                continue

            # Add breathing room between grouped setting cards inside tabs
            # without affecting slides or the scoreboard.
            if not first_group:
                st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
            first_group = False

            with st.container(border=True):
                st.markdown(field["group_label"])

                if field.get("description"):
                    st.caption(field["description"])

                group_key = field["group_key"]

                # If groups_nested is False, this section is only a visual UI
                # grouping. The actual config group lives at the root, e.g.
                # config["buttons"] instead of config["controls"]["buttons"].
                group_source = source.get(group_key, {}) if groups_nested else config.get(group_key, {})

                group_values = _render_field_grid(
                    field["fields"],
                    {},
                    group_source,
                    f"{section_key}__{group_key}",
                    gen,
                    lambda sub_field, group_key=group_key: (
                        [group_key, sub_field["key"]]
                        if not groups_nested
                        else [section_key, group_key, sub_field["key"]]
                    ),
                    max_columns=3,
                )

                groups_out[group_key] = group_values

        else:
            pair = _render_field(
                field,
                section_values,
                source,
                section_key,
                gen,
                [section_key, field["key"]],
            )
            if pair:
                section_values[pair[0]] = pair[1]

    if groups_nested:
        output[section_key] = {**section_values, **groups_out}
    else:
        output.update(groups_out)
        if section_values:
            output[section_key] = section_values

    return output


def _render_schema_section(section_def, config, gen):
    section_type = section_def["type"]

    if section_type == "player_list":
        return _render_player_list(section_def, config, gen)

    if section_type == "slide_list":
        return _render_slide_list(config, gen)

    return _render_regular_section(section_def, config, gen)


def render_schema_ui(schema, config, gen):
    """
    Walk *schema*, render every top-level settings section inside its own tab,
    and return a new config dict reflecting the current widget values.
    """
    output = {}
    tabs = st.tabs([section_def["label"] for section_def in schema])

    for tab, section_def in zip(tabs, schema):
        with tab:
            output.update(_render_schema_section(section_def, config, gen))

    return output


def render_settings_editor(text_slide_offset):
    inject_settings_editor_css()

    if "edit_draft" not in st.session_state:
        st.session_state.edit_draft = deepcopy(st.session_state.config)

    with st.container(key="settings_editor"):
        st.title("⚙️ Game Settings")

        st.subheader("Import config")
        uploaded = st.file_uploader(
            "Upload a config.json to pre-fill the form",
            type="json",
            label_visibility="collapsed",
        )

        if uploaded is not None:
            try:
                new_draft = load_config(uploaded.read())
                if new_draft != st.session_state.get("edit_draft"):
                    st.session_state.edit_draft = new_draft
                    st.session_state.form_generation += 1
                    st.rerun()
            except Exception as error:
                st.error(f"Could not parse uploaded file: {error}")

        if st.session_state.get("edit_draft") and uploaded is not None:
            st.success("Config loaded — review the settings below, then click Apply.")

        form_source = st.session_state.edit_draft
        gen = st.session_state.form_generation

        st.divider()
        cfg = render_schema_ui(CONFIG_SCHEMA, form_source, gen)
        st.divider()

        col_apply, col_download, col_cancel = st.columns([1, 1.2, 1])

        with col_apply:
            if st.button("✅ Apply", type="primary"):
                apply_config(load_config(cfg), text_slide_offset)
                st.session_state.pop("edit_draft", None)
                st.session_state.edit_mode = False
                st.rerun()

        with col_download:
            st.download_button(
                "⬇ Download config.json",
                data=json.dumps(cfg, indent=2),
                file_name="config.json",
                mime="application/json",
            )

        with col_cancel:
            if st.button("✕ Cancel", type="secondary"):
                st.session_state.pop("edit_draft", None)
                st.session_state.edit_mode = False
                st.rerun()

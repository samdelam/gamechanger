import json
from copy import deepcopy
import streamlit as st

class SettingsEngine:
    def __init__(self, default_config: dict):
        self.default_config = default_config

        if "config_runtime" not in st.session_state:
            st.session_state.config_runtime = deepcopy(default_config)

        if "config_draft" not in st.session_state:
            st.session_state.config_draft = deepcopy(default_config)
    
    def reset(self):
        st.session_state.config_runtime = deepcopy(self.default_config)
        st.session_state.config_draft = deepcopy(self.default_config)
    
    def runtime(self):
        return st.session_state.config_runtime

    def draft(self):
        return st.session_state.config_draft

    def open_editor(self):
        st.session_state.config_draft = deepcopy(
            st.session_state.config_runtime
        )

    def commit(self):
        st.session_state.config_runtime = deepcopy(
            st.session_state.config_draft
        )

    def to_json(self):
        return json.dumps(self.runtime(), indent=2)

    def load_json(self, raw: str):
        data = json.loads(raw)
        st.session_state.config_runtime = data
        st.session_state.config_draft = deepcopy(data)


def bind_checkbox(label, path, default=False):
    cfg = st.session_state.config_draft

    # navigate nested path
    ref = cfg
    for k in path[:-1]:
        ref = ref.setdefault(k, {})

    key = path[-1]

    if key not in ref:
        ref[key] = default

    widget_key = "cfg_" + "_".join(path)

    return st.checkbox(label, key=widget_key, value=ref[key])

def sync_widget(path, widget_key):
    cfg = st.session_state.config_draft

    ref = cfg
    for k in path[:-1]:
        ref = ref[k]

    ref[path[-1]] = st.session_state[widget_key]
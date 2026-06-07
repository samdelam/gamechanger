import base64
from pathlib import Path


# Project root is the folder where this Python file lives. Since the refactor
# keeps all .py files at the project root, asset paths are resolved relative to
# the app folder, not the current terminal working directory.
PROJECT_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
SOUNDS_DIR = ASSETS_DIR / "sounds"
MEDIA_DIR = ASSETS_DIR / "media"
CONFIG_FILE_PATH = PROJECT_ROOT / "config.json"

DSEG7_FONT_PATH = FONTS_DIR / "DSEG7Classic-Regular.ttf"
TRADE_GOTHIC_FONT_PATH = FONTS_DIR / "trade-gothic-lt-std-bold-condensed-no-20-5872def1d27d8.otf"

SLIDE_SOUND_PATH = SOUNDS_DIR / "slide.wav"
GAIN_POINT_SOUND_PATH = SOUNDS_DIR / "gain_point.wav"
LOSE_POINT_SOUND_PATH = SOUNDS_DIR / "lose_point.wav"


def require_asset(path, label="asset"):
    """Return a Path if it exists; otherwise raise a helpful error."""
    asset_path = Path(path)

    if not asset_path.exists():
        raise FileNotFoundError(
            f"Could not find {label}: {asset_path}\n"
            f"Expected project structure:\n"
            f"  {PROJECT_ROOT}\n"
            f"    assets/\n"
            f"      fonts/\n"
            f"        DSEG7Classic-Regular.ttf\n"
            f"        trade-gothic-lt-std-bold-condensed-no-20-5872def1d27d8.otf\n"
            f"      sounds/\n"
            f"        slide.wav\n"
            f"        gain_point.wav\n"
            f"        lose_point.wav\n"
            f"      media/\n"
            f"        cover.png"
        )

    return asset_path


def load_font(path):
    asset_path = require_asset(path, "font")
    with asset_path.open("rb") as file:
        return base64.b64encode(file.read()).decode()


def read_asset_bytes(path):
    asset_path = require_asset(path, "sound")
    with asset_path.open("rb") as file:
        return file.read()


def find_cover_image():
    for filename in ["cover.png", "cover.jpg", "cover.jpeg", "cover.webp"]:
        candidate = MEDIA_DIR / filename
        if candidate.exists():
            return candidate

    return None

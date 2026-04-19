from . import drawer, configuration_config
from tools import immutable_installer

def set_locale():
    locale_file = "/etc/locale.gen"

    locales = []

    # Read and extract valid locale names
    with open(locale_file, "r") as f:
        for line in f:
            stripped = line.strip()

            if not stripped:
                continue

            # Remove leading '#' for display
            clean = stripped.lstrip("# ").strip()
            parts = clean.split()

            # Only accept valid locale lines
            if len(parts) < 2:
                continue

            locale_name = parts[0]

            # Basic validation (avoid comments/header text)
            if "_" not in locale_name:
                continue

            locales.append(locale_name)

    locales = sorted(set(locales))  # remove duplicates

    # Handle selection
    def select_locale(loc):
        configuration_config._config.update({"system_locale": loc})
        drawer._pop()

    # Build menu
    drawer.push_menu([
        {
            "label": loc,
            "info": f"Locale: {loc}",
            "on_select": lambda l=loc: select_locale(l),
            "children": [],
        }
        for loc in locales
    ], title="Select System Locale")
import os
from . import drawer, immutable_os_config
from tools import immutable_installer
def set_timezone():
    zoneinfo_path = "/usr/share/zoneinfo"
    exclude = {"posix", "right", "Etc", "leaps"}

    areas = sorted([
        d for d in os.listdir(zoneinfo_path)
        if os.path.isdir(os.path.join(zoneinfo_path, d))
        and not d.startswith(".")
        and d not in exclude
    ])

    def pick_area():
        def pick_location(area):
            area_path = os.path.join(zoneinfo_path, area)
            locations = sorted([
                f for f in os.listdir(area_path)
                if os.path.isfile(os.path.join(area_path, f))
            ])

            def select_timezone(a, l):
                immutable_os_config._config["system"].update({"timezone": f"{a}/{l}"})
                drawer._pop()  # Exit location
                drawer._pop()  # Exit area

            drawer.push_menu([
                {
                    "label":     loc,
                    "info":      f"Timezone: {area}/{loc}",
                    "on_select": lambda a=area, l=loc: select_timezone(a, l),
                    "children":  [],
                }
                for loc in locations
            ], title=f"Timezone — {area}")

        drawer.push_menu([
            {
                "label":     area,
                "info":      f"Select location in {area}",
                "on_select": lambda a=area: pick_location(a),
                "children":  [],
            }
            for area in areas
        ], title="Timezone — Select Area")

    pick_area()
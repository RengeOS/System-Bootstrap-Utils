import curses

_COLOR_NORMAL   = 1
_COLOR_SELECTED = 2
_COLOR_TOPBAR   = 3
_COLOR_KEY      = 4
_COLOR_MARKED   = 5

_state = {
    "nav_stack":   [],
    "cur_items":   [],
    "cur_title":   "",
    "focus":       0,
    "scroll":      0,   # top visible item index (left panel)
    "right_scroll": 0,  # top visible line index (right panel)
    "app_title":   "",
    "marked":      set(),  # set of item labels that are marked
}


def _init_colors():
    """Initialise color pairs. Safe to call multiple times after initscr."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(_COLOR_NORMAL,   curses.COLOR_WHITE,  -1)
    curses.init_pair(_COLOR_SELECTED, curses.COLOR_BLACK,  curses.COLOR_GREEN)
    curses.init_pair(_COLOR_TOPBAR,   curses.COLOR_BLACK,  curses.COLOR_CYAN)
    curses.init_pair(_COLOR_KEY,      curses.COLOR_CYAN,   -1)
    curses.init_pair(_COLOR_MARKED,   curses.COLOR_YELLOW, -1)


def _resolve_info(item):
    """Resolve info to str or list. Calls it if callable."""
    info = item.get("info", "")
    return info() if callable(info) else info


def _safe_addstr(stdscr, y, x, text, attr=0):
    """Write text safely, clipping to screen bounds. Never raises."""
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h or x < 0 or x >= w:
        return
    max_len = w - x - 1
    if max_len <= 0:
        return
    try:
        stdscr.addstr(y, x, text[:max_len], attr)
    except curses.error:
        pass


def _draw_topbar(stdscr):
    """Draw a single-line top bar with the application title centered."""
    _, cols = stdscr.getmaxyx()
    padded  = _state["app_title"].center(cols - 1)
    _safe_addstr(stdscr, 0, 0, padded,
                 curses.color_pair(_COLOR_TOPBAR) | curses.A_BOLD)


def _draw_divider(stdscr, h):
    """Draw a vertical line separating the left and right panels."""
    _, cols = stdscr.getmaxyx()
    div_x   = cols * 3 // 10
    for y in range(1, h - 1):
        try:
            stdscr.addch(y, div_x, curses.ACS_VLINE,
                         curses.color_pair(_COLOR_NORMAL))
        except curses.error:
            pass


def _draw_left(stdscr, items, focus, scroll, h):
    """Render the navigable option list on the left panel with scrolling."""
    _, cols  = stdscr.getmaxyx()
    div_x    = cols * 3 // 10
    max_w    = max(div_x - 2, 1)
    visible  = h - 3   # rows available between topbar and bottom edge

    for row_idx in range(visible):
        item_idx = scroll + row_idx
        if item_idx >= len(items):
            break
        y     = row_idx + 2
        item  = items[item_idx]
        label = item["label"]

        # Build prefix: [*] if marked, [ ] if markable, empty otherwise
        is_markable = item.get("markable", False)
        is_marked   = label in _state["marked"]

        if is_markable:
            prefix = "[*] " if is_marked else "[ ] "
        else:
            prefix = ""

        display = (prefix + label)[:max_w]

        if item_idx == focus:
            attr = curses.color_pair(_COLOR_SELECTED) | curses.A_BOLD
            _safe_addstr(stdscr, y, 1, display.ljust(max_w), attr)
        elif is_marked:
            _safe_addstr(stdscr, y, 1, display,
                         curses.color_pair(_COLOR_MARKED) | curses.A_BOLD)
        else:
            _safe_addstr(stdscr, y, 1, display,
                         curses.color_pair(_COLOR_NORMAL))

    # Scroll indicator — show fraction when list is longer than visible area
    if len(items) > visible:
        indicator = f" {focus + 1}/{len(items)} "
        _safe_addstr(stdscr, h - 1, 1, indicator,
                     curses.color_pair(_COLOR_NORMAL))


# Right-panel line builder

def _build_info_lines(info, max_w):
    """
    Convert info (str or list of (key,value) tuples) into a flat list of
    (text, attr) pairs — one per screen line.  No curses calls here so the
    result can be sliced for scrolling.
    """
    lines = []  # list of (text, attr_key)  where attr_key is a string

    if isinstance(info, list):
        # Two-column table
        if not info:
            return lines
        key_w = max(len(str(k)) for k, _ in info)
        sep   = "  :  "

        for key, value in info:
            # Key column
            key_str = str(key).ljust(key_w)
            sep_str = sep
            val_str = str(value)
            val_max = max(max_w - key_w - len(sep), 1)

            # Word-wrap the value
            val_words = val_str.split()
            val_line  = ""
            first_val_line = True

            for word in val_words:
                if len(val_line) + len(word) + (1 if val_line else 0) > val_max:
                    if first_val_line:
                        lines.append((key_str + sep_str + val_line, "key"))
                        first_val_line = False
                    else:
                        lines.append((" " * (key_w + len(sep)) + val_line, "normal"))
                    val_line = word
                else:
                    val_line = (val_line + " " + word).strip() if val_line else word

            # Last (or only) line of this row
            if first_val_line:
                lines.append((key_str + sep_str + val_line, "key"))
            else:
                lines.append((" " * (key_w + len(sep)) + val_line, "normal"))

    else:
        # Plain text with newline / word-wrap support
        text = str(info)
        for paragraph in text.split("\n"):
            if not paragraph.strip():
                lines.append(("", "normal"))
                continue
            line = ""
            for word in paragraph.split():
                if len(line) + len(word) + (1 if line else 0) > max_w:
                    lines.append((line, "normal"))
                    line = word
                else:
                    line = (line + " " + word).strip() if line else word
            if line:
                lines.append((line, "normal"))

    return lines


def _draw_right(stdscr, item, h):
    """Render the right panel — title, divider, then scrollable info."""
    _, cols = stdscr.getmaxyx()
    div_x   = cols * 3 // 10
    start   = div_x + 2
    max_w   = max(cols - start - 1, 1)

    if item is None:
        return

    # Header (rows 2-3 are always visible, not scrolled)
    _safe_addstr(stdscr, 2, start, item["label"][:max_w],
                 curses.color_pair(_COLOR_NORMAL) | curses.A_BOLD)
    _safe_addstr(stdscr, 3, start, "-" * min(max_w, len(item["label"]) + 4),
                 curses.color_pair(_COLOR_NORMAL))

    info  = _resolve_info(item)
    lines = _build_info_lines(info, max_w)

    # Visible area for right panel content: rows 5 … h-2
    content_start_row = 5
    visible_rows      = max(h - content_start_row - 1, 1)
    right_scroll      = _state["right_scroll"]

    # Clamp scroll
    max_scroll = max(len(lines) - visible_rows, 0)
    right_scroll = max(0, min(right_scroll, max_scroll))
    _state["right_scroll"] = right_scroll

    attr_map = {
        "key":    curses.color_pair(_COLOR_KEY) | curses.A_BOLD,
        "normal": curses.color_pair(_COLOR_NORMAL),
    }

    for i in range(visible_rows):
        line_idx = right_scroll + i
        if line_idx >= len(lines):
            break
        text, attr_key = lines[line_idx]
        screen_row     = content_start_row + i

        # For "key" lines, render key part in cyan and rest in normal
        if attr_key == "key" and isinstance(info, list):
            # Find where the separator ends — everything before is key+sep
            key_w   = max(len(str(k)) for k, _ in info)
            sep     = "  :  "
            sep_end = key_w + len(sep)
            key_part = text[:sep_end]
            val_part = text[sep_end:]
            _safe_addstr(stdscr, screen_row, start, key_part,
                         curses.color_pair(_COLOR_KEY) | curses.A_BOLD)
            _safe_addstr(stdscr, screen_row, start + len(key_part), val_part,
                         curses.color_pair(_COLOR_NORMAL))
        else:
            _safe_addstr(stdscr, screen_row, start, text, attr_map.get(attr_key, 0))

    # Scroll indicator for right panel
    if len(lines) > visible_rows:
        pct        = int(100 * right_scroll / max(max_scroll, 1))
        indicator  = f" ↑↓ {pct}% ({right_scroll + 1}-{min(right_scroll + visible_rows, len(lines))}/{len(lines)}) "
        _safe_addstr(stdscr, h - 1, div_x + 2, indicator,
                     curses.color_pair(_COLOR_KEY))


_BACK_ITEM = {
    "label":    "<- Return",
    "info":     "Go back to the previous menu.",
    "children": [],
}


def _push(items, title):
    """Push current menu onto the stack and enter a submenu."""
    _state["nav_stack"].append((
        _state["cur_items"],
        _state["cur_title"],
        _state["focus"],
        _state["scroll"],
        _state["right_scroll"],
    ))
    _state["cur_items"]    = [_BACK_ITEM] + list(items)
    _state["cur_title"]    = title
    _state["focus"]        = 0
    _state["scroll"]       = 0
    _state["right_scroll"] = 0


def _pop():
    """Pop the nav stack and restore the previous menu level."""
    if _state["nav_stack"]:
        items, title, focus, scroll, right_scroll = _state["nav_stack"].pop()
        _state["cur_items"]    = items
        _state["cur_title"]    = title
        _state["focus"]        = focus
        _state["scroll"]       = scroll
        _state["right_scroll"] = right_scroll


def _clamp_scroll(h):
    """Adjust left scroll so the focused item is always visible."""
    focus   = _state["focus"]
    scroll  = _state["scroll"]
    visible = h - 3

    if focus < scroll:
        scroll = focus
    elif focus >= scroll + visible:
        scroll = focus - visible + 1

    _state["scroll"] = max(0, scroll)


def _loop(stdscr):
    """Core curses event loop."""
    _init_colors()
    curses.curs_set(0)
    stdscr.keypad(True)

    while True:
        h, _ = stdscr.getmaxyx()
        _clamp_scroll(h)

        stdscr.erase()

        items  = _state["cur_items"]
        focus  = _state["focus"]
        scroll = _state["scroll"]
        cur    = items[focus] if items else None

        _draw_topbar(stdscr)
        _draw_divider(stdscr, h)
        _draw_left(stdscr, items, focus, scroll, h)
        _draw_right(stdscr, cur, h)
        stdscr.refresh()

        key = stdscr.getch()

        # Navigation (left panel)
        if key == curses.KEY_UP:
            _state["focus"]        = max(0, focus - 1)
            _state["right_scroll"] = 0   # reset right scroll on item change

        elif key == curses.KEY_DOWN:
            _state["focus"]        = min(len(items) - 1, focus + 1)
            _state["right_scroll"] = 0

        # Right-panel scrolling
        elif key == ord("-"):           # scroll right panel up one line
            _state["right_scroll"] = max(0, _state["right_scroll"] - 1)

        elif key == ord("+"):           # scroll right panel down one line
            _state["right_scroll"] += 1

        # Mark / unmark with Space
        elif key == ord(" "):
            if cur is not None and cur is not _BACK_ITEM and cur.get("markable", False):
                label = cur["label"]
                if label in _state["marked"]:
                    _state["marked"].discard(label)
                else:
                    _state["marked"].add(label)
                # Notify via on_mark callback if present
                if callable(cur.get("on_mark")):
                    cur["on_mark"](label, label in _state["marked"])

        # Enter / select
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            if cur is None:
                continue

            if cur is _BACK_ITEM:
                if _state["nav_stack"]:
                    _pop()
                else:
                    break

            else:
                if cur.get("children"):
                    _push(cur["children"], cur["label"])

                if callable(cur.get("on_select")):
                    try:
                        curses.endwin()
                    except Exception:
                        pass

                    exit_code = None
                    try:
                        cur["on_select"]()
                    except KeyboardInterrupt:
                        pass
                    except SystemExit as e:
                        exit_code = e.code

                    if exit_code is not None:
                        raise SystemExit(exit_code)

                    try:
                        stdscr = curses.initscr()
                        _init_colors()
                        curses.noecho()
                        curses.cbreak()
                        curses.curs_set(0)
                        stdscr.keypad(True)
                        stdscr.clearok(True)
                    except Exception:
                        pass

        # Quit
        elif key in (ord("q"), ord("Q")):
            break


def run_menu(menu_data, title="Menu"):
    """
    Launch the interactive split-panel menu.

    Parameters
    ----------
    menu_data : list[dict]
        label     (str)                    left panel label              [required]
        info      (str | list | callable)  right panel content           [optional]
                    str                    plain text, \\n supported
                    list of (key, value)   two-column table like cfdisk
                    callable               zero-arg function returning str or list
        on_select (callable)               called on ENTER               [optional]
        on_mark   (callable(label, state)) called when Space toggles mark [optional]
        children  (list)                   nested submenu items          [optional]
        markable  (bool)                   True → Space toggles [*] mark [optional]

    title : str
        Application title shown in the top bar.

    Keybindings
    -----------
        ↑ / ↓    move focus in left panel
        Enter    select / enter submenu
        Space    toggle mark on markable items
        +        scroll right panel down one line
        -        scroll right panel up one line
        q / Q    quit
    """
    _state["cur_items"]    = list(menu_data)
    _state["cur_title"]    = title
    _state["app_title"]    = title
    _state["focus"]        = 0
    _state["scroll"]       = 0
    _state["right_scroll"] = 0
    _state["nav_stack"]    = []
    _state["marked"]       = set()

    stdscr = curses.initscr()
    try:
        curses.noecho()
        curses.cbreak()
        _loop(stdscr)
    except SystemExit:
        try:
            curses.echo()
            curses.nocbreak()
            curses.endwin()
        except Exception:
            pass
        raise
    except Exception:
        try:
            curses.echo()
            curses.nocbreak()
            curses.endwin()
        except Exception:
            pass
        raise
    else:
        try:
            curses.echo()
            curses.nocbreak()
            curses.endwin()
        except Exception:
            pass


def get_marked():
    """Return a frozenset of labels that are currently marked."""
    return frozenset(_state["marked"])


def push_menu(menu_data, title=""):
    """
    Navigate into a new menu level from within an on_select callback.
    The user can return to the previous menu with <- Return as usual.

    Example
    -------
        def set_timezone():
            drawer.push_menu([
                {"label": "UTC", "markable": True, "info": "...", "on_select": lambda: ...},
            ], title="Select Timezone")
    """
    _push(list(menu_data), title)
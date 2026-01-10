#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Translation and text sizing system with integrated tr()-extractor UI.

Features:
- Translation with locale management (tr() / _() syntax)
- Dynamic text sizing for UI elements
- Flet-based editor for translation files
- Support for placeholders {name}
- Automatic placeholder validation
- Undo/Redo functionality

Usage:
    from translator import TranslationSystem

    # Option 1: Local alias (recommended)
    ts = TranslationSystem("de_DE")
    _ = ts.tr
    print(_("Hello {name}").format(name="World"))

    # Option 2: Global installation
    ts = TranslationSystem("de_DE")
    ts.install()
    print(_("Hello"))
"""

import sys
import os
import json
import re
import warnings
from typing import Dict, List, Tuple, Optional

import flet as ft
import locale

# Pillow optional for text measurement
try:
    from PIL import ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

__version__ = "2.0.0"
__author__ = "Your Name"


class TranslationSystem:
    """
    Complete translation and text measurement system.

    Provides:
    - Locale-based translations with placeholder support
    - Text measurement for dynamic font sizing
    - GUI editor for translation files
    """

    def __init__(self, locale_code: Optional[str] = None):
        """
        Initialize the translation system.

        Args:
            locale_code: Optional locale to set immediately (e.g., "de_DE", "en_US")
        """
        # Translation / Locale
        self._current_locale: Optional[str] = None
        self._translation_cache: Dict[str, str] = {}
        self._placeholder_pattern = re.compile(r"\{[^{}]*\}")
        self._fallback_locale: Optional[str] = None

        # Text measurement
        self._last_text: Optional[str] = None
        self._last_width: Optional[int] = None
        self._last_height: Optional[int] = None
        self._normal_fontsize: int = 20
        self._last_newsize: Optional[int] = None
        self._font_cache: Dict[int, 'ImageFont'] = {}

        # Set locale if provided
        if locale_code:
            self.set_locale(locale_code)

    # =========================================================
    #   TEXT MEASUREMENT
    # =========================================================

    def _load_font(self, size: int) -> 'ImageFont':
        """Load or retrieve cached font at specified size."""
        if size in self._font_cache:
            return self._font_cache[size]

        if not PIL_AVAILABLE:
            raise RuntimeError(
                "PIL/Pillow is required for text measurement. "
                "Install with: pip install Pillow"
            )

        base = os.path.dirname(__file__)
        font_path = os.path.join(base, "assets", "fonts", "Roboto-Regular.ttf")

        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, size)
        else:
            font = ImageFont.load_default()

        self._font_cache[size] = font
        return font

    def _measure(self, text: str, size: int) -> Tuple[int, int]:
        """Measure text dimensions at given font size."""
        font = self._load_font(size)
        try:
            left, top, right, bottom = font.getbbox(text)
            return right - left, bottom - top
        except AttributeError:
            # Fallback for older Pillow versions
            return font.getsize(text)

    def store_text_metrics(self, text: str, size: Optional[int] = None) -> str:
        """
        Store text metrics for later retrieval.

        Args:
            text: Text to measure
            size: Font size (defaults to normal_fontsize)

        Returns:
            The input text (for chaining)
        """
        if size is None:
            size = self._normal_fontsize
        self._last_text = text
        self._last_width, self._last_height = self._measure(text, size)
        return text

    def get_width(self) -> int:
        """Get width of last measured text."""
        return self._last_width or self._normal_fontsize

    def get_height(self) -> int:
        """Get height of last measured text."""
        return self._last_height or self._normal_fontsize

    def resize_text(self, text: str, target_width: int, ref_size: Optional[int] = None) -> int:
        """
        Calculate font size to fit text within target width.

        Args:
            text: Text to size
            target_width: Target width in pixels
            ref_size: Reference font size (defaults to normal_fontsize)

        Returns:
            Calculated font size
        """
        if ref_size is None:
            ref_size = self._normal_fontsize

        w_ref, _ = self._measure(text, ref_size)
        w_ref = w_ref or ref_size

        scale = target_width / w_ref
        new_size = int(ref_size * scale)

        # Don't scale up beyond reference size (only scale down to fit)
        if new_size > ref_size:
            new_size = ref_size
        self._last_newsize = new_size
        return new_size

    def get_last_font_size(self) -> int:
        """Get the last calculated font size from resize_text()."""
        return self._last_newsize or self._normal_fontsize

    def tr_size(self) -> int:
        """Alias for get_last_font_size() for backward compatibility."""
        return self.get_last_font_size()

    # =========================================================
    #   LOCALE / TRANSLATION
    # =========================================================

    def extract_placeholders(self, text: str) -> List[str]:
        """
        Extract all placeholders from text.

        Args:
            text: Text to parse

        Returns:
            List of placeholders (e.g., ["{name}", "{count}"])
        """
        return self._placeholder_pattern.findall(text or "")

    def list_locales(self) -> List[str]:
        """
        List all available locale codes.

        Returns:
            Sorted list of locale codes (e.g., ["de_DE", "en_US"])
        """
        # Get directory - prefer __file__ over sys.argv[0] for reliability
        if '__file__' in globals():
            app_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Get app name from calling script
        app_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

        locales_dir = os.path.join(app_dir, "assets", "locales")
        if not os.path.isdir(locales_dir):
            return []

        result = []
        prefix = app_name + "_"

        for filename in os.listdir(locales_dir):
            if filename.startswith(prefix) and filename.endswith(".json"):
                code = filename[len(prefix):-5]
                result.append(code)

        return sorted(result)

    def set_locale(self, locale_code: str, fallback: Optional[str] = None) -> None:
        """
        Set the current locale and load translations.

        Args:
            locale_code: Locale to set (e.g., "de_DE")
            fallback: Optional fallback locale if translation is missing
        """
        self._current_locale = locale_code
        self._fallback_locale = fallback
        self._load_locale_for_session()

    def get_locale(self) -> Optional[str]:
        """Get the current locale code."""
        return self._current_locale

    def _load_locale_for_session(self) -> None:
        """Load translation data for current locale from ALL matching JSON files."""
        if not self._current_locale:
            self._translation_cache = {}
            return

        # Get directory - prefer __file__ over sys.argv[0] for reliability
        if '__file__' in globals():
            app_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        locales_dir = os.path.join(app_dir, "assets", "locales")

        if not os.path.isdir(locales_dir):
            self._translation_cache = {}
            return

        # Find ALL *_{locale_code}.json files
        pattern = f"*_{self._current_locale}.json"
        self._translation_cache = {}

        try:
            for filename in os.listdir(locales_dir):
                if filename.endswith(f"_{self._current_locale}.json"):
                    json_path = os.path.join(locales_dir, filename)

                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            data = json.load(f)

                            # Merge into cache (later files overwrite earlier)
                            if isinstance(data, dict):
                                self._translation_cache.update(data)
                            # Empty dict {} is OK, just skip

                    except (json.JSONDecodeError, IOError) as e:
                        # Log warning but continue with other files
                        warnings.warn(f"Failed to load {filename}: {e}")
                        continue

        except OSError as e:
            warnings.warn(f"Failed to read locales directory: {e}")
            self._translation_cache = {}

    def tr(self, text: str, fontsize: int = 20) -> str:
        """
        Translate text and prepare for dynamic sizing.

        Args:
            text: Text to translate
            fontsize: Reference font size for measurement

        Returns:
            Translated text with placeholders intact
        """
        if not isinstance(text, str):
            return text

        # Get translation or use original
        translated = self._translation_cache.get(text, text)

        # Validate placeholders
        expected = self.extract_placeholders(text)
        current = self.extract_placeholders(translated)

        # Add missing placeholders
        for ph in expected:
            if ph not in current:
                translated += " " + ph

        # Store metrics and calculate resize
        self.store_text_metrics(text, fontsize)
        self.resize_text(translated, self.get_width(), fontsize)

        # Return translated string (user will call .format() themselves if needed)
        return translated

    # Alias for gettext compatibility
    def _(self, text: str, fontsize: int = 20) -> str:
        """Alias for tr() - gettext-style."""
        return self.tr(text, fontsize)

    def install(self, warn_on_override: bool = True) -> None:
        """
        Make _() globally available in builtins (gettext-style).

        WARNING: This modifies builtins and may conflict with other code!
        Preferred: Use local alias `_ = ts.tr` instead.

        Args:
            warn_on_override: Warn if _ already exists in builtins
        """
        import builtins

        if hasattr(builtins, '_') and warn_on_override:
            warnings.warn(
                "Overwriting existing '_' in builtins. "
                "This may cause conflicts with other libraries. "
                "Consider using local alias `_ = ts.tr` instead.",
                RuntimeWarning,
                stacklevel=2
            )

        builtins._ = self.tr

    def uninstall(self) -> None:
        """Remove _() from builtins if installed."""
        import builtins
        if hasattr(builtins, '_'):
            delattr(builtins, '_')

    # =========================================================
    #   UI / EXTRACTOR
    # =========================================================

    def run_tr_extractor_ui(self) -> None:

        def get_system_locale() -> str:
            lang, enc = locale.getlocale()
            return lang or "en_US"

        placeholder_pattern = re.compile(r"\{[^{}]*\}")

        def ui_extract_placeholders(text: str):
            return placeholder_pattern.findall(text or "")

        def extract_tr_strings(pyfile: str, locale_code: str):
            pattern = re.compile(r'(?:tr|_)\(\s*[\'"](.+?)[\'"]\s*(?:,.*?)?\)')
            base = os.path.basename(pyfile)
            name_no_ext = os.path.splitext(base)[0]

            project_root = os.path.dirname(pyfile)
            out_dir = os.path.join(project_root, "assets", "locales")
            os.makedirs(out_dir, exist_ok=True)

            json_file = os.path.join(out_dir, f"{name_no_ext}_{locale_code}.json")

            with open(pyfile, "r", encoding="utf-8") as f:
                content = f.read()

            found = set(pattern.findall(content))

            if os.path.exists(json_file):
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}

            added = 0
            for s in found:
                if s not in data:
                    data[s] = s
                    added += 1

            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return json_file, added, len(found), data

        def ui(page: ft.Page):
            page.title = "tr() / _() Extractor & Editor"
            page.window.width = 1200
            page.window.height = 800

            system_locale = get_system_locale()
            selected_pyfile = {"path": None}
            current_json_file = {"path": None}
            original_data = {}
            undo_stack = []
            redo_stack = []

            warning_text = ft.Text("", color=ft.Colors.ORANGE, size=14, weight=ft.FontWeight.BOLD)

            search_field = ft.TextField(
                label="Search / Suche",
                on_change=lambda e: rebuild_editor(),
                expand=True
            )

            sort_dropdown = ft.Dropdown(
                label="Sort / Sortierung",
                value="original",
                options=[
                    ft.dropdown.Option("original"),
                    ft.dropdown.Option("alphabetisch"),
                ],
                width=200,
            )
            sort_dropdown.on_change = lambda e: rebuild_editor()

            locale_dropdown = ft.Dropdown(
                label="Locale",
                value=system_locale,
                options=[
                    ft.dropdown.Option("en_US"),
                    ft.dropdown.Option("en_GB"),
                    ft.dropdown.Option("de_DE"),
                    ft.dropdown.Option("fr_FR"),
                    ft.dropdown.Option("es_ES"),
                    ft.dropdown.Option("it_IT"),
                    ft.dropdown.Option("ja_JP"),
                    ft.dropdown.Option("zh_CN"),
                ],
                width=220,
            )

            result_text = ft.Text("", selectable=True)
            stats_text = ft.Text("", size=12, color=ft.Colors.BLUE_GREY)

            editor_rows = ft.ListView(spacing=12,scroll=ft.ScrollMode.ALWAYS) #height=int(page.height * 0.6), width=page.width - 40,

            def get_current_data():
                parsed = {}
                for control in editor_rows.controls:
                    # Unterscheide: TextField direkt vs Column
                    if isinstance(control, ft.TextField):
                        # Kurze Labels: key ist im label
                        key = control.label
                        value = control.value
                    elif isinstance(control, ft.Column):
                        # Lange Labels: key ist im Text, value im TextField
                        key = control.controls[0].value
                        value = control.controls[1].value
                    else:
                        continue
                    parsed[key] = value
                return parsed

            def load_data_into_editor(data):
                nonlocal original_data
                original_data = dict(data)
                rebuild_editor()

            def push_undo():
                undo_stack.append(get_current_data())
                redo_stack.clear()

            def undo(e):
                if not undo_stack:
                    return
                redo_stack.append(get_current_data())
                data = undo_stack.pop()
                load_data_into_editor(data)

            def redo(e):
                if not redo_stack:
                    return
                undo_stack.append(get_current_data())
                data = redo_stack.pop()
                load_data_into_editor(data)

            def update_stats():
                if not original_data:
                    stats_text.value = ""
                    return

                total = len(original_data)
                translated = sum(1 for k, v in original_data.items() if v != k)
                percent = (translated / total * 100) if total > 0 else 0

                stats_text.value = f"📊 {translated}/{total} translated ({percent:.1f}%)"
                page.update()

            def update_warning_banner():
                errors = 0
                for control in editor_rows.controls:
                    # Unterscheide: TextField direkt vs Column
                    if isinstance(control, ft.TextField):
                        # Kurze Labels: key ist im label
                        key = control.label
                        value = control.value
                    elif isinstance(control, ft.Column):
                        # Lange Labels: key ist im Text, value im TextField
                        key = control.controls[0].value
                        value = control.controls[1].value
                    else:
                        continue

                    expected = ui_extract_placeholders(key)
                    current = ui_extract_placeholders(value)

                    for ph in expected:
                        if ph not in current:
                            errors += 1
                            break

                warning_text.value = (
                    f"⚠️ Warning: {errors} entries with missing placeholders."
                    if errors > 0 else ""
                )
                page.update()

            def on_value_change(e, k, textfield):
                push_undo()
                expected_inner = ui_extract_placeholders(k)
                current_inner = ui_extract_placeholders(textfield.value)
                missing_inner = [ph for ph in expected_inner if ph not in current_inner]
                textfield.bgcolor = ft.Colors.ORANGE_100 if missing_inner else None
                update_warning_banner()
                update_stats()

            def rebuild_editor():
                if not original_data:
                    editor_rows.controls.clear()
                    page.update()
                    return

                editor_rows.controls.clear()

                query = search_field.value.lower().strip() if search_field.value else ""

                items = list(original_data.items())
                if sort_dropdown.value == "alphabetisch":
                    items.sort(key=lambda x: x[0].lower())

                for key, value in items:
                    if query and query not in key.lower() and query not in (value or "").lower():
                        continue

                    expected = ui_extract_placeholders(key)
                    current = ui_extract_placeholders(value)
                    missing = [ph for ph in expected if ph not in current]

                    bg = ft.Colors.ORANGE_100 if missing else None

                    # Unterscheide kurze und lange Labels
                    if len(key) <= 40:
                        # Kurze Labels: als TextField-Label
                        control = ft.TextField(
                            label=key,
                            value=value,
                            multiline=True,
                            min_lines=1,
                            max_lines=5,
                            bgcolor=bg,
                        )
                        control.on_change = lambda e, k=key, textfield=control: on_value_change(e, k, textfield)
                        editor_rows.controls.append(control)
                    else:
                        # Lange Labels: separates Text() + TextField
                        tf = ft.TextField(
                            value=value,
                            multiline=True,
                            min_lines=1,
                            max_lines=5,
                            bgcolor=bg,
                            expand=True
                        )
                        tf.on_change = lambda e, k=key, textfield=tf: on_value_change(e, k, textfield)

                        editor_rows.controls.append(
                            ft.Column(
                                [
                                    ft.Text(key, size=10, selectable=True),
                                    tf,
                                ],
                                spacing=2,
                                expand=True,
                            )
                        )

                update_warning_banner()
                update_stats()
                page.update()

            def save_json(e):
                if not current_json_file["path"]:
                    return

                parsed = {}
                for control in editor_rows.controls:
                    # Unterscheide: TextField direkt vs Column
                    if isinstance(control, ft.TextField):
                        # Kurze Labels: key ist im label
                        key = control.label
                        value = control.value
                    elif isinstance(control, ft.Column):
                        # Lange Labels: key ist im Text, value im TextField
                        key = control.controls[0].value
                        value = control.controls[1].value
                    else:
                        continue  # Sollte nicht vorkommen

                    if "\n" not in key:
                        value = value.replace("\r\n", " ").replace("\n", " ")
                        value = " ".join(value.split())

                    expected = ui_extract_placeholders(key)
                    current = ui_extract_placeholders(value)

                    if expected:
                        current_set = set(current)
                        for ph in expected:
                            if ph not in current_set:
                                if value and not value.endswith(" "):
                                    value += " "
                                value += ph
                                current_set.add(ph)

                    parsed[key] = value

                try:
                    with open(current_json_file["path"], "w", encoding="utf-8") as f:
                        json.dump(parsed, f, ensure_ascii=False, indent=2)

                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("✅ Saved successfully!"),
                        bgcolor=ft.Colors.GREEN,
                    )
                    page.snack_bar.open = True
                except IOError as ex:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"❌ Save failed: {ex}"),
                        bgcolor=ft.Colors.RED,
                    )
                    page.snack_bar.open = True

                page.update()

            undo_button = ft.Button("↶ Undo", on_click=undo, disabled=True)
            redo_button = ft.Button("↷ Redo", on_click=redo, disabled=True)
            save_button = ft.Button("💾 Save", on_click=save_json, disabled=True)

            def update_button_states():
                undo_button.disabled = len(undo_stack) == 0
                redo_button.disabled = len(redo_stack) == 0
                save_button.disabled = current_json_file["path"] is None
                page.update()

            def update_for_locale_change(e):
                # Auto-Save vor Wechsel
                if current_json_file["path"]:
                    save_json(None)

                if not selected_pyfile["path"]:
                    return

                pyfile = selected_pyfile["path"]
                loc_code = locale_dropdown.value

                try:
                    out_file, added, total, data = extract_tr_strings(pyfile, loc_code)

                    current_json_file["path"] = out_file

                    result_text.value = (
                        f"📄 File: {out_file}\n"
                        f"🔍 Found strings: {total}\n"
                        f"➕ Newly added: {added}"
                    )

                    load_data_into_editor(data)
                    undo_stack.clear()
                    redo_stack.clear()
                    update_button_states()
                except Exception as ex:
                    result_text.value = f"❌ Error: {ex}"

                page.update()

            locale_dropdown.on_change = update_for_locale_change

            async def open_picker(e=None):
                files = await ft.FilePicker().pick_files(
                    allow_multiple=False,
                    allowed_extensions=["py"]
                )

                if not files:
                    return

                selected_pyfile["path"] = files[0].path
                update_for_locale_change(None)

            select_button = ft.Button(
                "📂 Select Python File",
                on_click=open_picker
            )

            # ---------------------------------------------------------

            def on_resize(e):
                editor_rows.height = int(page.height * 0.6)
                editor_rows.width = page.width - 40
                rebuild_editor()
                page.update()

            page.on_resize = on_resize

            page.add(
                ft.Container(
                    content=ft.Column(
                        expand=True,  # ← WICHTIG
                        controls=[
                            ft.Text("tr() / _() Extractor & Editor", size=24, weight=ft.FontWeight.BOLD),
                            warning_text,
                            ft.Row([
                                locale_dropdown,
                                select_button,
                            ]),
                            result_text,
                            stats_text,
                            ft.Divider(),
                            ft.Row([search_field, sort_dropdown]),
                            ft.Row([undo_button, redo_button, save_button]),
                            editor_rows,
                        ],
                    ),
                    padding=20,
                )
            )

        ft.app(target=ui)


def main(args=None):
    """Example usage and UI launcher."""
    ts = TranslationSystem()
    ts.run_tr_extractor_ui()


if __name__ == '__main__':
    main(sys.argv)
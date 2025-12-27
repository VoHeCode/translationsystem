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

        base = os.path.dirname(__file__)
        font_path = os.path.join(base, "assets", "fonts", "Roboto-Regular.ttf")

        if PIL_AVAILABLE and os.path.exists(font_path):
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
        app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
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
        """Load translation data for current locale."""
        if not self._current_locale:
            self._translation_cache = {}
            return

        app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        app_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

        json_path = os.path.join(
            app_dir, "assets", "locales", f"{app_name}_{self._current_locale}.json"
        )

        if not os.path.exists(json_path):
            self._translation_cache = {}
            return

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self._translation_cache = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            warnings.warn(f"Failed to load locale {self._current_locale}: {e}")
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

        # Try to format, return raw if fails
        try:
            return translated.format()
        except (KeyError, ValueError):
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
        """
        Launch the Flet-based translation editor UI.

        Provides:
        - Extract tr() and _() calls from Python files
        - Edit translations with placeholder validation
        - Undo/Redo support
        - Search and sort functionality
        """
        import flet as ft
        import locale

        def get_system_locale() -> str:
            """Get system locale or default to en_US."""
            lang, enc = locale.getlocale()
            if not lang:
                return "en_US"
            return lang

        placeholder_pattern = re.compile(r"\{[^{}]*\}")

        def ui_extract_placeholders(text: str) -> List[str]:
            """Extract placeholders from text."""
            return placeholder_pattern.findall(text or "")

        def extract_tr_strings(pyfile: str, locale_code: str) -> Tuple[str, int, int, Dict[str, str]]:
            """
            Extract tr() and _() calls from Python file.

            Args:
                pyfile: Path to Python source file
                locale_code: Target locale code

            Returns:
                Tuple of (json_file_path, added_count, total_count, translation_dict)
            """
            # Match both tr() and _() calls
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

            # Load existing translations
            if os.path.exists(json_file):
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}

            # Add new strings
            added = 0
            for s in found:
                if s not in data:
                    data[s] = s
                    added += 1

            # Save updated file
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return json_file, added, len(found), data

        def ui(page: ft.Page) -> None:
            """Main UI function for Flet."""
            page.title = "tr() / _() Extractor & Editor"
            page.window.width = 1200
            page.window.height = 800

            system_locale = get_system_locale()
            selected_pyfile = {"path": None}
            current_json_file = {"path": None}
            original_data = {}
            undo_stack = []
            redo_stack = []

            # UI Components
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
                on_change=lambda e: rebuild_editor()
            )

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
            save_status = ft.Text("")
            stats_text = ft.Text("", size=12, color=ft.Colors.BLUE_GREY)

            editor_rows = ft.Column(scroll="auto", expand=True)

            def get_current_data() -> Dict[str, str]:
                """Extract current data from editor."""
                parsed = {}
                for row in editor_rows.controls:
                    key = row.controls[0].value
                    tf = row.controls[1]
                    parsed[key] = tf.value
                return parsed

            def load_data_into_editor(data: Dict[str, str]) -> None:
                """Load translation data into editor."""
                nonlocal original_data
                original_data = dict(data)
                rebuild_editor()

            def push_undo() -> None:
                """Save current state to undo stack."""
                undo_stack.append(get_current_data())
                redo_stack.clear()

            def undo(e) -> None:
                """Undo last change."""
                if not undo_stack:
                    return
                redo_stack.append(get_current_data())
                data = undo_stack.pop()
                load_data_into_editor(data)

            def redo(e) -> None:
                """Redo last undone change."""
                if not redo_stack:
                    return
                undo_stack.append(get_current_data())
                data = redo_stack.pop()
                load_data_into_editor(data)

            def update_stats() -> None:
                """Update translation statistics."""
                if not original_data:
                    stats_text.value = ""
                    return

                total = len(original_data)
                translated = sum(1 for k, v in original_data.items() if v != k)
                percent = (translated / total * 100) if total > 0 else 0

                stats_text.value = f"📊 {translated}/{total} translated ({percent:.1f}%)"
                page.update()

            def update_warning_banner() -> None:
                """Check for missing placeholders and update warning."""
                errors = 0
                for row in editor_rows.controls:
                    key = row.controls[0].value
                    tf = row.controls[1]
                    value = tf.value

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

            def on_value_change(e, k: str, textfield: ft.TextField) -> None:
                """Handle text field changes."""
                push_undo()
                expected_inner = ui_extract_placeholders(k)
                current_inner = ui_extract_placeholders(textfield.value)
                missing_inner = [ph for ph in expected_inner if ph not in current_inner]
                textfield.bgcolor = ft.Colors.ORANGE_100 if missing_inner else None
                update_warning_banner()
                update_stats()

            def rebuild_editor() -> None:
                """Rebuild editor with current filter/sort settings."""
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
                    # Filter by search query
                    if query and query not in key.lower() and query not in (value or "").lower():
                        continue

                    # Check for missing placeholders
                    expected = ui_extract_placeholders(key)
                    current = ui_extract_placeholders(value)
                    missing = [ph for ph in expected if ph not in current]

                    bg = ft.Colors.ORANGE_100 if missing else None

                    # Create multiline text field
                    tf = ft.TextField(
                        value=value,
                        expand=True,
                        multiline=True,
                        min_lines=1,
                        max_lines=5,
                        bgcolor=bg,
                    )

                    tf.on_change = lambda e, k=key, textfield=tf: on_value_change(e, k, textfield)

                    editor_rows.controls.append(
                        ft.Row(
                            [
                                ft.Text(key, width=400, selectable=True),
                                tf,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    )

                update_warning_banner()
                update_stats()
                page.update()

            def save_json(e) -> None:
                """Save translations to JSON file."""
                if not current_json_file["path"]:
                    return

                parsed = {}
                for row in editor_rows.controls:
                    key = row.controls[0].value
                    tf = row.controls[1]
                    value = tf.value

                    # Remove line breaks if original has none
                    if "\n" not in key:
                        value = value.replace("\r\n", " ").replace("\n", " ")
                        value = " ".join(value.split())

                    # Ensure all placeholders are present
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

                    save_status.value = "✅ Saved successfully!"
                    save_status.color = ft.Colors.GREEN
                except IOError as ex:
                    save_status.value = f"❌ Save failed: {ex}"
                    save_status.color = ft.Colors.RED

                page.update()

            # Buttons
            undo_button = ft.ElevatedButton("↶ Undo", on_click=undo, disabled=True)
            redo_button = ft.ElevatedButton("↷ Redo", on_click=redo, disabled=True)
            save_button = ft.ElevatedButton("💾 Save", on_click=save_json, disabled=True)

            def update_button_states() -> None:
                """Update undo/redo button states."""
                undo_button.disabled = len(undo_stack) == 0
                redo_button.disabled = len(redo_stack) == 0
                save_button.disabled = current_json_file["path"] is None
                page.update()

            def update_for_locale_change(e) -> None:
                """Handle locale selection change."""
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
                    save_status.value = ""
                    undo_stack.clear()
                    redo_stack.clear()
                    update_button_states()
                except Exception as ex:
                    result_text.value = f"❌ Error: {ex}"

                page.update()

            locale_dropdown.on_change = update_for_locale_change

            def on_file_picked(e: ft.FilePickerResultEvent) -> None:
                """Handle file selection."""
                if not e.files:
                    return
                selected_pyfile["path"] = e.files[0].path
                update_for_locale_change(None)

            picker = ft.FilePicker(on_result=on_file_picked)
            page.overlay.append(picker)

            # Build UI
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text("tr() / _() Extractor & Editor", size=24, weight=ft.FontWeight.BOLD),
                        warning_text,
                        ft.Row([
                            locale_dropdown,
                            ft.ElevatedButton(
                                "📂 Select Python File",
                                on_click=lambda _: picker.pick_files(
                                    allowed_extensions=["py"],
                                    allow_multiple=False
                                )
                            ),
                        ]),
                        result_text,
                        stats_text,
                        ft.Divider(),
                        ft.Row([search_field, sort_dropdown]),
                        ft.Row([undo_button, redo_button, save_button]),
                        editor_rows,
                        save_status,
                    ]),
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

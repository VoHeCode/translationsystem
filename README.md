# TranslationSystem v2.0

Complete translation and text sizing system for Python applications with GUI editor.

## ✨ Features

### Core Translation
- ✅ Locale-based translations (JSON files)
- ✅ Support for `tr()` and `_()` syntax (gettext-compatible)
- ✅ Placeholder validation `{name}`, `{count}`, etc.
- ✅ Automatic placeholder preservation
- ✅ Multi-line string support
- ✅ Fallback locale support

### Text Measurement
- ✅ Dynamic font sizing based on text width
- ✅ Pillow-based text measurement (optional)
- ✅ Font caching for performance

### GUI Editor (Flet)
- ✅ Extract `tr()` and `_()` calls from Python files
- ✅ Side-by-side original/translation editing
- ✅ Placeholder validation with visual warnings
- ✅ Search and filter functionality
- ✅ Sort alphabetically or keep original order
- ✅ Undo/Redo support
- ✅ Translation statistics (% complete)
- ✅ Auto-save with error handling

## 🚀 Quick Start

### Installation

```bash
pip install flet pillow
```

### Basic Usage

```python
from src.translator import TranslationSystem

# Option 1: Local alias (RECOMMENDED)
ts = TranslationSystem("de_DE")
_ = ts.tr

print(_("Hello World"))
print(_("Welcome {name}").format(name="Alice"))

# Option 2: Direct usage
ts = TranslationSystem("de_DE")
print(ts.tr("Hello World"))

# Option 3: Global installation (use with caution)
ts = TranslationSystem("de_DE")
ts.install()  # Makes _() available globally
print(_("Hello World"))
ts.uninstall()  # Clean up when done
```

### Launch GUI Editor

```bash
python demo.py --ui
```

Or programmatically:

```python
from src.translator import TranslationSystem

ts = TranslationSystem()
ts.run_tr_extractor_ui()
```

## 📁 File Structure

```
your_project/
├── demo.py                      # Your main application
├── translator.py                # TranslationSystem module
└── assets/
    ├── fonts/
    │   └── Roboto-Regular.ttf  # Optional for text measurement
    └── locales/
        ├── demo_de_DE.json     # German translations
        ├── demo_en_US.json     # English translations
        └── demo_fr_FR.json     # French translations
```

## 📝 Translation File Format

JSON files in `assets/locales/` follow this naming convention:
`{script_name}_{locale_code}.json`

Example `demo_de_DE.json`:

```json
{
  "Hello World": "Hallo Welt",
  "Welcome {name}": "Willkommen {name}",
  "Settings": "Einstellungen",
  "Multi-line\nText": "Mehrzeiliger\nText"
}
```

## 🎨 API Reference

### TranslationSystem Class

#### Initialization

```python
ts = TranslationSystem(locale_code=None)
```

**Parameters:**
- `locale_code` (str, optional): Locale to set immediately (e.g., "de_DE")

#### Translation Methods

##### `tr(text, fontsize=20)` / `_(text, fontsize=20)`

Translate text and prepare for dynamic sizing.

```python
translated = ts.tr("Hello World")
translated = ts._("Hello World")  # Same as tr()
```

**Parameters:**
- `text` (str): Text to translate
- `fontsize` (int): Reference font size for measurement

**Returns:** Translated string with placeholders intact

#### Scaling Methods

##### `tr_size()`

Returns the font size so that the translated word has the same width as the original word.

```python
translated = ts.tr("Hello World",20)
newsize = ts.tr_size() 
```

**Parameters:**

**Returns:** fontsize as int

##### `set_locale(locale_code, fallback=None)`

Set the current locale and load translations.

```python
ts.set_locale("de_DE")
ts.set_locale("de_DE", fallback="en_US")
```

**Parameters:**
- `locale_code` (str): Locale to activate
- `fallback` (str, optional): Fallback locale if translation missing

##### `get_locale()`

Get the current locale code.

```python
current = ts.get_locale()  # Returns "de_DE"
```

##### `list_locales()`

List all available locale codes.

```python
locales = ts.list_locales()  # Returns ["de_DE", "en_US", "fr_FR"]
```

##### `install(warn_on_override=True)`

Make `_()` globally available (gettext-style).

**⚠️ Warning:** Modifies builtins! Use local alias instead.

```python
ts.install()           # Install with warning
ts.install(False)      # Install without warning
```

##### `uninstall()`

Remove `_()` from builtins.

```python
ts.uninstall()
```

#### Text Measurement Methods

##### `store_text_metrics(text, size=None)`

Store text dimensions for later retrieval.

```python
ts.store_text_metrics("Button Label", 20)
width = ts.get_width()
height = ts.get_height()
```

##### `resize_text(text, target_width, ref_size=None)`

Calculate font size to fit text within target width.

```python
new_size = ts.resize_text("Long Button Label", target_width=200, ref_size=20)
```

**Returns:** Calculated font size in points

##### `get_width()` / `get_height()`

Get dimensions of last measured text.

```python
width = ts.get_width()   # In pixels
height = ts.get_height()  # In pixels
```

##### `get_last_font_size()` / `tr_size()`

Get last calculated font size from `resize_text()`.

```python
size = ts.get_last_font_size()
size = ts.tr_size()  # Alias
```

#### Utility Methods

##### `extract_placeholders(text)`

Extract all placeholders from text.

```python
placeholders = ts.extract_placeholders("Hello {name}, you have {count} messages")
# Returns: ["{name}", "{count}"]
```

##### `run_tr_extractor_ui()`

Launch the Flet-based translation editor GUI.

```python
ts.run_tr_extractor_ui()
```

## 🎯 Best Practices

### 1. Use Local Alias (Recommended)

```python
from src.translator import TranslationSystem

ts = TranslationSystem("de_DE")
_ = ts.tr  # Local alias - clean and safe

print(_("Hello"))
```

**Why?**
- ✅ No global namespace pollution
- ✅ Works well in modules and libraries
- ✅ No conflicts with other code
- ✅ Explicit and clear

### 2. Initialize Once per Module

```python
# config.py
from src.translator import TranslationSystem

ts = TranslationSystem("de_DE")
_ = ts.tr

# main.py
from config import _

print(_("Hello"))
```

### 3. Handle Placeholders Correctly

```python
# ✅ GOOD: Use named placeholders
message = _("Hello {name}, you have {count} messages")
print(message.format(name="Alice", count=5))

# ❌ BAD: Positional placeholders harder to translate
message = _("Hello {}, you have {} messages")  # Confusing for translators
```

### 4. Keep Strings Atomic

```python
# ✅ GOOD: Complete sentences
print(_("Are you sure you want to delete this file?"))

# ❌ BAD: Fragmented strings
print(_("Are you sure") + " " + _("you want to delete") + " " + _("this file?"))
# Context lost, hard to translate properly
```

### 5. Use Multi-line for Long Text

```python
# ✅ GOOD: Natural line breaks
help_text = _("""
Welcome to the application!

This is a comprehensive guide to help you
get started with all the features.
""")

# ❌ BAD: Very long single-line strings
help_text = _("Welcome to the application! This is a comprehensive guide...")
```

## 🔧 Advanced Features

### Fallback Locale

```python
ts = TranslationSystem()
ts.set_locale("de_CH", fallback="de_DE")
# Falls back to German if Swiss German translation missing
```

### Dynamic Locale Switching

```python
ts = TranslationSystem()
_ = ts.tr

# Switch between locales
ts.set_locale("en_US")
print(_("Settings"))  # "Settings"

ts.set_locale("de_DE")
print(_("Settings"))  # "Einstellungen"

ts.set_locale("fr_FR")
print(_("Settings"))  # "Paramètres"
```

### Text Measurement for UI

```python
ts = TranslationSystem("de_DE")

# Translate button label
label = ts.tr("Click here to continue", fontsize=16)

# Get recommended font size to fit width
button_width = 150
new_size = ts.resize_text(label, button_width, ref_size=16)

print(f"Use font size {new_size}pt to fit {button_width}px width")

# or use it this way (recommended) flet sample code:

# default fontsize of the UI you create
FONTSIZE = 20
# Translate text at 20pt, then use calculated size for button
page.theme = ft.Theme(
    font_family="Roboto",
    text_theme=ft.TextTheme(
        body_medium=ft.TextStyle(size=FONTSIZE)
    )
)

# Translate the string "Settings" the actual Fontsize ist given
text = ts.tr("Settings", FONTSIZE)
# asize gets back a new fontsize for the translated string
asize = ts.tr_size()
# that mean a Word "Settings" 8 Letter long in 20px fontsize
# translated to "Setze Einstellung" 17 Letter long 
# give us a ts.tr_size() of 9px for the new fontsize 
# so it fit's in the same place! (A Button will not grow )
#


page.add(
  ft.ElevatedButton(text, 
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=ts.tr_size()))
                    ),
  ft.ElevatedButton(_("Exit",FONTSIZE),
                    on_click=exit_app,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=ts.tr_size()))
                    )
)

```

## 📋 GUI Editor Workflow

1. **Open Python file** - Click "Select Python File"
2. **Choose locale** - Select target language from dropdown
3. **Extract strings** - Automatically finds all `tr()` and `_()` calls
4. **Edit translations** - Side-by-side editor with:
   - Original text (left, read-only)
   - Translation field (right, editable)
   - Visual warning for missing placeholders (orange background)
5. **Search/Filter** - Find specific strings quickly
6. **Sort** - Alphabetically or keep source order
7. **Undo/Redo** - Safe editing with history
8. **Save** - Export to JSON file

### Editor Features

- **Placeholder Validation**: Missing placeholders highlighted in orange
- **Warning Banner**: Shows count of problematic translations
- **Statistics**: Shows translation progress (e.g., "45/100 translated (45%)")
- **Multi-line Support**: Word-wrap for long translations
- **Auto-cleanup**: Removes line breaks from single-line strings on save

## 🐛 Troubleshooting

### Translations Not Loading

**Problem:** `tr()` returns original English text

**Solutions:**
1. Check locale code: `print(ts.get_locale())`
2. Verify file exists: `assets/locales/{script}_de_DE.json`
3. Check JSON syntax (use editor UI to avoid errors)
4. Call `ts.set_locale()` before using `tr()`

### Placeholder Warnings

**Problem:** Orange background in editor

**Solution:** Missing placeholders will be auto-added on save, but fix manually for better quality:

```json
// Before (missing {name})
"Hello {name}": "Hallo"

// After (fixed)
"Hello {name}": "Hallo {name}"
```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'flet'`

**Solution:**
```bash
pip install flet
```

### Text Measurement Not Working

**Problem:** Width/height always return default values

**Solution:** Install Pillow and add font file:
```bash
pip install pillow
```

Add `Roboto-Regular.ttf` to `assets/fonts/`

## 🆕 Version 2.0 Improvements

### API Changes
- ✅ `tr_init()` → `set_locale()` (more intuitive)
- ✅ `locale_code` parameter in `__init__()`
- ✅ `install()` / `uninstall()` methods
- ✅ `get_locale()` method
- ✅ `_()` as alias for `tr()`

### New Features
- ✅ Warning system for `install()` (prevents conflicts)
- ✅ Both `tr()` and `_()` extraction in UI
- ✅ Translation statistics in editor
- ✅ Improved error handling
- ✅ Better type hints
- ✅ Comprehensive docstrings
- ✅ Fallback locale support

### UI Improvements
- ✅ Better visual feedback
- ✅ File picker filter (only .py files)
- ✅ Improved button states
- ✅ Statistics display
- ✅ Better error messages
- ✅ Larger window size (1200x800)

### Code Quality
- ✅ Type hints throughout
- ✅ Comprehensive documentation
- ✅ Better error handling
- ✅ Warnings for potential issues
- ✅ More Pythonic API

## 📄 License

Your license here.

## 👥 Contributing

Contributions welcome! Please:
1. Use type hints
2. Add docstrings
3. Test with multiple locales
4. Update README for new features

## 📞 Support

For issues or questions, please open an issue on GitHub.

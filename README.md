# TranslationSystem v2.0

Complete translation system for Python applications with integrated GUI editor for managing multilingual content.

Due to changes from flet 0.2x.x to flet >0.79.0, I had to adjust this as well. Therefore, it is currently not (or no longer) backwards compatible.
## ✨ Features

### Core Translation
- ✅ Locale-based translations stored in JSON files
- ✅ Support for both `tr()` and `_()` syntax (gettext-compatible)
- ✅ Automatic placeholder validation `{name}`, `{count}`, etc.
- ✅ Automatic placeholder preservation in translations
- ✅ Multi-line string support
- ✅ Fallback locale support
- ✅ Dynamic font sizing to fit translated text in the same space

### GUI Editor (Flet-based)
- ✅ Extract all `tr()` and `_()` calls from Python source files
- ✅ Side-by-side editor: original text vs. translation
- ✅ Visual placeholder validation with warnings
- ✅ Search and filter functionality
- ✅ Alphabetical sorting or original order
- ✅ Undo/Redo support
- ✅ Translation progress statistics
- ✅ Auto-save with comprehensive error handling

## 🚀 Quick Start

### Installation

```bash
pip install flet pillow
```

### Basic Usage

```python
from translator import TranslationSystem

# Initialize with locale
ts = TranslationSystem("de_DE")
_ = ts.tr  # Create local alias (recommended)

# Simple translation
print(_("Hello World"))

# Translation with placeholders
greeting = _("Welcome {name}, you have {count} new messages")
print(greeting.format(name="Alice", count=5))

# Dynamic font sizing for UI elements
text = _("Settings", fontsize=20)
adjusted_size = ts.tr_size()  # Returns font size to fit translated text
```

### Launch Translation Editor

```python
from translator import TranslationSystem

ts = TranslationSystem()
ts.run_tr_extractor_ui()
```

This opens a GUI where you can:
1. Select your Python file
2. Choose target locale
3. Edit translations side-by-side
4. Save to JSON automatically

## 📁 File Structure

Your project should follow this structure:

```
your_project/
├── your_app.py              # Your main application
├── translator.py            # TranslationSystem module
└── assets/
    ├── fonts/
    │   └── Roboto-Regular.ttf  # Optional for text measurement
    └── locales/
        ├── your_app_de_DE.json     # German translations
        ├── your_app_en_US.json     # English translations
        └── your_app_fr_FR.json     # French translations
```

**Naming Convention:**
Translation files are named: `{script_name}_{locale_code}.json`

Example: If your script is `demo.py`, translations are stored as:
- `demo_de_DE.json` (German)
- `demo_en_US.json` (English)
- `demo_fr_FR.json` (French)

## 📝 Translation File Format

Translation files are simple JSON dictionaries mapping original text to translations.

**Example:** `demo_de_DE.json`

```json
{
  "Hello World": "Hallo Welt",
  "Welcome {name}": "Willkommen {name}",
  "Settings": "Einstellungen",
  "You have {count} new messages": "Sie haben {count} neue Nachrichten",
  "Multi-line\nText example": "Mehrzeiliger\nText Beispiel"
}
```

**Important Rules:**
- Preserve all placeholders like `{name}`, `{count}` in translations
- Keep line breaks (`\n`) if present in original
- Use UTF-8 encoding (automatic with the editor)

## 🎯 API Reference

### Initialization

#### `TranslationSystem(locale_code=None)`

Creates a new translation system instance.

```python
# Initialize without locale (set later)
ts = TranslationSystem()

# Initialize with locale
ts = TranslationSystem("de_DE")
```

**Parameters:**
- `locale_code` (str, optional): Initial locale (e.g., "de_DE", "en_US", "fr_FR")

**Returns:** TranslationSystem instance

---

### Translation Methods

#### `tr(text, fontsize=20)`

Main translation method. Translates text and prepares font size calculation for UI elements.

```python
# Simple translation
translated = ts.tr("Hello World")

# Translation with font size specification
button_text = ts.tr("Click here", fontsize=16)
optimal_size = ts.tr_size()  # Get calculated font size
```

**Parameters:**
- `text` (str): Text to translate
- `fontsize` (int, default=20): Reference font size for measurement

**Returns:** Translated string with placeholders preserved

**Notes:**
- If translation is missing, returns original text
- Missing placeholders are automatically appended (with warning)
- Call `tr_size()` after this to get adjusted font size

---

#### `_(text, fontsize=20)`

Alias for `tr()` - provides gettext-style syntax.

```python
# Both are identical
text1 = ts.tr("Hello")
text2 = ts._("Hello")

# With local alias (recommended)
_ = ts.tr
print(_("Welcome"))
```

**Parameters:** Same as `tr()`

**Returns:** Same as `tr()`

---

### Locale Management

#### `set_locale(locale_code, fallback=None)`

Set the active locale and load corresponding translations.

```python
# Set locale
ts.set_locale("de_DE")

# Set locale with fallback
ts.set_locale("de_CH", fallback="de_DE")
# If Swiss German translation missing, falls back to standard German
```

**Parameters:**
- `locale_code` (str): Locale to activate (e.g., "de_DE")
- `fallback` (str, optional): Fallback locale if translation missing

**Returns:** None

**Effect:** Loads translation file `{script}_de_DE.json` into cache

---

#### `get_locale()`

Returns the currently active locale code.

```python
current = ts.get_locale()
print(f"Current locale: {current}")  # "de_DE"
```

**Parameters:** None

**Returns:** str - Current locale code (e.g., "de_DE") or None if not set

---

#### `list_locales()`

Lists all available locale codes by scanning the `assets/locales/` directory.

```python
available = ts.list_locales()
print(f"Available languages: {available}")
# ["de_DE", "en_GB", "en_US", "fr_FR"]
```

**Parameters:** None

**Returns:** List[str] - Sorted list of available locale codes

**Notes:**
- Only lists locales for which JSON files exist
- Scans `assets/locales/{script}_{locale}.json` files

---

### Font Sizing

#### `tr_size()`

Returns the calculated font size for the last translated text. This ensures translated text fits in the same space as the original.

```python
# Translate with reference font size
text = ts.tr("Settings", fontsize=20)

# Get adjusted font size for translated text
new_size = ts.tr_size()

# Use in UI
button = Button(text=text, font_size=new_size)
```

**Parameters:** None

**Returns:** int - Font size in points

**How it works:**
1. `tr()` measures original text at reference size
2. Measures translated text at same size
3. Calculates scaling factor
4. `tr_size()` returns adjusted size (only scales down, never up)

**Example:**
```
Original: "Settings" (8 characters) at 20px
Translated: "Einstellungen" (13 characters) at 20px
tr_size() returns: ~12px (to fit same width)
```

---

### Global Installation

#### `install(warn_on_override=True)`

Makes `_()` globally available by adding it to Python's builtins. This allows using `_()` without importing in every file.

```python
ts = TranslationSystem("de_DE")
ts.install()

# Now _() is available everywhere without import
print(_("Hello"))

# Later, clean up
ts.uninstall()
```

**Parameters:**
- `warn_on_override` (bool, default=True): Show warning if `_` already exists in builtins

**Returns:** None

**⚠️ Warning:**
- Modifies global namespace (can conflict with other libraries)
- Not recommended for libraries/packages
- **Recommended alternative:** Use local alias `_ = ts.tr`

---

#### `uninstall()`

Removes `_()` from builtins if it was installed.

```python
ts.install()
print(_("Hello"))  # Works

ts.uninstall()
print(_("Hello"))  # NameError: name '_' is not defined
```

**Parameters:** None

**Returns:** None

---

### Translation Editor

#### `run_tr_extractor_ui()`

Launches the Flet-based GUI editor for managing translations.

```python
from translator import TranslationSystem

ts = TranslationSystem()
ts.run_tr_extractor_ui()  # Opens GUI window
```

**Parameters:** None

**Returns:** None (blocks until window is closed)

**Features:**
- **File Selection:** Pick any Python file to extract strings from
- **Locale Selection:** Choose target language
- **Automatic Extraction:** Finds all `tr()` and `_()` calls
- **Side-by-Side Editor:** Original (left) vs Translation (right)
- **Placeholder Validation:** Visual warnings for missing placeholders
- **Search/Filter:** Find specific strings quickly
- **Sort Options:** Alphabetically or original order
- **Undo/Redo:** Full editing history
- **Statistics:** Shows translation progress (e.g., "45/100 translated (45%)")
- **Auto-Save:** Saves to `assets/locales/{script}_{locale}.json`

**Workflow:**
1. Click "Select Python File"
2. Choose locale from dropdown
3. Edit translations in right column
4. Missing placeholders highlighted in orange
5. Click "Save" to export JSON
6. Run your app to see translations

**Requirements:**
- `flet` package installed
- Write permissions in project directory

---

## 💡 Usage Examples

### Example 1: Simple Command Line App

```python
#!/usr/bin/env python3
import sys
from translator import TranslationSystem

# Initialize
ts = TranslationSystem()
ts.set_locale("de_DE")
_ = ts.tr

def main():
    print(_("Welcome to the application!"))
    print(_("Current locale: {locale}").format(locale=ts.get_locale()))
    
    name = input(_("Enter your name: "))
    print(_("Hello {name}!").format(name=name))

if __name__ == '__main__':
    main()
```

### Example 2: Flet App with Dynamic Font Sizing

```python
#!/usr/bin/env python3
import flet as ft
from translator import TranslationSystem

ts = TranslationSystem("de_DE")
_ = ts.tr

def main(page: ft.Page):
    page.title = _("My Application")
    
    # Define default font size
    FONTSIZE = 20
    
    # Configure theme
    page.theme = ft.Theme(
        font_family="Roboto",
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(size=FONTSIZE)
        )
    )
    
    # Translate and auto-size buttons
    settings_text = ts.tr("Settings", FONTSIZE)
    settings_size = ts.tr_size()
    
    exit_text = ts.tr("Exit", FONTSIZE)
    exit_size = ts.tr_size()
    
    page.add(
        ft.ElevatedButton(
            settings_text,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=settings_size)
            )
        ),
        ft.ElevatedButton(
            exit_text,
            on_click=lambda _: page.window.close(),
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=exit_size)
            )
        )
    )

ft.app(target=main)
```

### Example 3: Dynamic Locale Switching

```python
from translator import TranslationSystem

ts = TranslationSystem()
_ = ts.tr

# Get available locales
locales = ts.list_locales()
print(f"Available: {locales}")  # ['de_DE', 'en_US', 'fr_FR']

# Switch between locales
for locale in locales:
    ts.set_locale(locale)
    print(f"{locale}: {_('Hello World')}")

# Output:
# de_DE: Hallo Welt
# en_US: Hello World
# fr_FR: Bonjour le monde
```

### Example 4: First-Time Setup with Editor

```python
#!/usr/bin/env python3
import sys
from translator import TranslationSystem

ts = TranslationSystem()

# Uncomment these lines once to create translation files
# ts.run_tr_extractor_ui()
# sys.exit(0)

# After creating translations, use them
ts.set_locale("de_DE")
_ = ts.tr

def main():
    print(_("This is my application"))
    print(_("Processing {count} items...").format(count=42))

if __name__ == '__main__':
    main()
```

**Workflow:**
1. Write code with `_()` calls
2. Uncomment `run_tr_extractor_ui()` and `exit()`
3. Run script → GUI opens
4. Create translations for each locale
5. Comment out GUI lines again
6. Run normally with translations

---

## 🎨 Best Practices

### 1. Use Local Alias (Recommended)

```python
# ✅ GOOD: Local alias
from translator import TranslationSystem
ts = TranslationSystem("de_DE")
_ = ts.tr

print(_("Hello"))
```

**Why?**
- No global namespace pollution
- Works in modules and libraries
- No conflicts with other code
- Explicit and clear

```python
# ❌ AVOID: Global installation
ts = TranslationSystem("de_DE")
ts.install()  # Modifies builtins
print(_("Hello"))
```

---

### 2. Initialize Once per Module

```python
# config.py
from translator import TranslationSystem

ts = TranslationSystem("de_DE")
_ = ts.tr

# main.py
from config import _, ts

print(_("Hello"))
print(f"Current locale: {ts.get_locale()}")
```

---

### 3. Use Named Placeholders

```python
# ✅ GOOD: Named placeholders (clear for translators)
message = _("Hello {name}, you have {count} messages")
print(message.format(name="Alice", count=5))

# ❌ BAD: Positional placeholders (confusing context)
message = _("Hello {}, you have {} messages")
print(message.format("Alice", 5))
```

**Why named is better:**
- Translators know what each placeholder means
- Different languages may need different word order
- Prevents translation errors

---

### 4. Keep Strings Atomic

```python
# ✅ GOOD: Complete sentences
print(_("Are you sure you want to delete this file?"))

# ❌ BAD: Fragmented strings
print(_("Are you sure") + " " + 
      _("you want to delete") + " " + 
      _("this file?"))
```

**Why atomic is better:**
- Context is preserved
- Translators can adjust entire sentence structure
- Different languages have different grammar rules

---

### 5. Provide Context for Ambiguous Words

```python
# ✅ GOOD: Context included
save_button = _("Save file")
save_money = _("Save 20% discount")

# ❌ BAD: Same word, different meanings
save_button = _("Save")  # Save file? Save money? Save settings?
save_money = _("Save")   # Ambiguous for translators
```

---

### 6. Handle Multi-line Text Properly

```python
# ✅ GOOD: Natural line breaks
help_text = _("""
Welcome to the application!

This guide will help you understand
all features and get started quickly.
""")

# ✅ ALSO GOOD: Explicit line breaks
help_text = _("Line 1\nLine 2\nLine 3")

# ❌ BAD: Very long single-line (hard to edit)
help_text = _("Welcome to the application! This is a comprehensive guide to help you understand all features...")
```

---

### 7. Don't Translate Variables or Code

```python
# ✅ GOOD: Only translate user-facing text
filename = "data.txt"
print(_("Loading file: {filename}").format(filename=filename))

# ❌ BAD: Translating variable names
filename = _("data.txt")  # Don't translate filenames!
print(_("Loading file: {filename}").format(filename=filename))
```

---

## 🔧 Advanced Features

### Fallback Locale Chain

When a translation is missing, the system can fall back to another locale:

```python
ts = TranslationSystem()

# Swiss German → Standard German → English
ts.set_locale("de_CH", fallback="de_DE")

# If "de_CH" translation missing, tries "de_DE"
# If "de_DE" also missing, returns original English
```

---

### Dynamic Locale Selection

Allow users to change language at runtime:

```python
import flet as ft
from translator import TranslationSystem

ts = TranslationSystem()

def main(page: ft.Page):
    _ = ts.tr
    
    def change_locale(e):
        ts.set_locale(e.control.value)
        update_ui()
    
    def update_ui():
        # Rebuild UI with new translations
        page.clean()
        page.add(
            ft.Dropdown(
                label=_("Language"),
                options=[ft.dropdown.Option(loc) for loc in ts.list_locales()],
                on_change=change_locale
            ),
            ft.Text(_("Hello World"))
        )
        page.update()
    
    update_ui()

ft.app(target=main)
```

---

### Font Size Calculation for Responsive UI

Ensure buttons don't grow when translated:

```python
import flet as ft
from translator import TranslationSystem

ts = TranslationSystem("de_DE")

def create_fixed_button(text, fontsize=20):
    """Creates button with fixed width using adjusted font size."""
    translated = ts.tr(text, fontsize)
    adjusted_size = ts.tr_size()
    
    return ft.ElevatedButton(
        translated,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=adjusted_size)
        )
    )

def main(page: ft.Page):
    page.add(
        create_fixed_button("Settings"),
        create_fixed_button("Configuration"),
        create_fixed_button("Exit")
    )

ft.app(target=main)
```

**Result:**
- "Settings" (8 chars) → "Einstellungen" (13 chars)
- Font size automatically reduced to fit same space
- UI layout remains consistent across languages

---

## 🛠️ GUI Editor Detailed Guide

### Opening the Editor

```python
from translator import TranslationSystem

ts = TranslationSystem()
ts.run_tr_extractor_ui()
```

### Editor Interface

```
┌─────────────────────────────────────────────────────────┐
│ tr() / _() Extractor & Editor                           │
├─────────────────────────────────────────────────────────┤
│ ⚠️ Warning: 3 entries with missing placeholders         │
├─────────────────────────────────────────────────────────┤
│ [Locale: de_DE ▼]  [📂 Select Python File]             │
├─────────────────────────────────────────────────────────┤
│ 📄 File: demo_de_DE.json                                │
│ 🔍 Found strings: 25                                    │
│ ➕ Newly added: 5                                       │
│ 📊 18/25 translated (72.0%)                             │
├─────────────────────────────────────────────────────────┤
│ [Search...                ] [Sort: Original      ▼]     │
│ [↶ Undo] [↷ Redo] [💾 Save]                            │
├─────────────────────────────────────────────────────────┤
│ Original                    │ Translation               │
│ Hello World                 │ [Hallo Welt           ]   │
│ Welcome {name}              │ [Willkommen {name}    ]   │
│ Settings                    │ [Einstellungen        ]   │
│ You have {count} messages   │ [Sie haben Nachrichten]   │ ← Orange (missing {count})
├─────────────────────────────────────────────────────────┤
│ ✅ Saved successfully!                                  │
└─────────────────────────────────────────────────────────┘
```

### Step-by-Step Workflow

**1. Select Python File**
- Click "📂 Select Python File"
- Choose your `.py` file
- Editor extracts all `tr()` and `_()` calls

**2. Choose Locale**
- Select language from dropdown (e.g., "de_DE")
- Loads existing translations or creates new file

**3. Edit Translations**
- Left column: Original text (read-only)
- Right column: Translation (editable)
- Type or paste translations

**4. Validate Placeholders**
- Missing placeholders → Orange background
- Warning banner shows count
- Fix manually or auto-append on save

**5. Use Search/Filter**
- Type in search box
- Filters by original OR translation
- Case-insensitive

**6. Sort Entries**
- "Original": Keep source code order
- "Alphabetically": Sort by original text

**7. Undo/Redo**
- Click "↶ Undo" to revert
- Click "↷ Redo" to restore
- Full history until save

**8. Save**
- Click "💾 Save"
- Writes to `assets/locales/{script}_{locale}.json`
- Success/error message shown

---

### Editor Features in Detail

#### Placeholder Validation

The editor automatically detects missing placeholders:

```
Original:     "Hello {name}, you have {count} messages"
Translation:  "Hallo {name}"  ← Missing {count}
Result:       Orange background + warning
```

On save, missing placeholders are automatically appended:
```
Before save: "Hallo {name}"
After save:  "Hallo {name} {count}"
```

**Recommendation:** Fix manually for better quality.

---

#### Translation Statistics

Shows progress in real-time:

```
📊 18/25 translated (72.0%)
```

**Calculation:**
- Total: Number of unique strings
- Translated: Strings where translation ≠ original
- Percentage: (translated / total) × 100

---

#### Multi-line Text Support

The editor handles multi-line strings automatically:

```python
# In your code
long_text = _("""
This is a long help text
that spans multiple lines.
""")

# In editor
Original:     "This is a long help text\nthat spans multiple lines."
Translation:  [Multi-line text field with word wrap]
```

---

#### Search and Filter

Search matches both original and translation:

```
Search: "message"

Matches:
- "You have new messages" → "Sie haben neue Nachrichten"
- "Message sent" → "Nachricht gesendet"
- "Error: Invalid message format" → "Fehler: Ungültiges Nachrichtenformat"
```

---

## 🐛 Troubleshooting

### Problem: Translations Not Loading

**Symptom:** `tr()` returns original English text

**Diagnostics:**
```python
print(f"Current locale: {ts.get_locale()}")  # Should show "de_DE"
print(f"Available locales: {ts.list_locales()}")  # Should include "de_DE"
```

**Solutions:**

1. **Check locale is set:**
```python
ts.set_locale("de_DE")  # Don't forget this!
```

2. **Verify file exists:**
```bash
ls assets/locales/
# Should show: your_script_de_DE.json
```

3. **Check JSON syntax:**
```python
import json
with open("assets/locales/your_script_de_DE.json") as f:
    data = json.load(f)  # Should not throw error
```

4. **Verify naming convention:**
```
Script: demo.py
Locale file: demo_de_DE.json  ← Must match script name
```

---

### Problem: Missing Placeholders Warning

**Symptom:** Orange background in editor

**Example:**
```json
"Hello {name}": "Hallo"  ← Missing {name}
```

**Solution 1: Manual Fix (Recommended)**
```json
"Hello {name}": "Hallo {name}"
```

**Solution 2: Auto-Fix on Save**
- Editor automatically appends missing placeholders
- Result: `"Hallo {name}"`
- But manual placement is better for quality

---

### Problem: Module Import Errors

**Symptom:** 
```
ModuleNotFoundError: No module named 'flet'
ModuleNotFoundError: No module named 'PIL'
```

**Solution:**
```bash
pip install flet pillow
```

---

### Problem: Font Sizing Not Working

**Symptom:** `tr_size()` always returns default value (20)

**Diagnostics:**
```python
print(ts.tr("Settings", 20))
print(ts.tr_size())  # Returns 20 instead of calculated value
```

**Solution 1: Install Pillow**
```bash
pip install pillow
```

**Solution 2: Add Font File**
```bash
mkdir -p assets/fonts
# Copy Roboto-Regular.ttf to assets/fonts/
```

**Solution 3: Use Default Font**
If no custom font needed, Pillow will use default font automatically.

---

### Problem: JSON Encoding Errors

**Symptom:** 
```
UnicodeEncodeError when saving translations
```

**Solution:**
The editor uses UTF-8 automatically, but verify:

```python
import json
data = {"Hello": "Grüß Gott"}
with open("test.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
```

---

### Problem: Locale File Not Found

**Symptom:**
```python
ts.set_locale("de_DE")
# Translations don't work
```

**Debug:**
```python
import os
app_name = "your_script"
locale = "de_DE"
expected = f"assets/locales/{app_name}_{locale}.json"
print(f"Looking for: {expected}")
print(f"Exists: {os.path.exists(expected)}")
```

**Solution:**
1. Create file using GUI editor
2. Or create manually:
```bash
mkdir -p assets/locales
echo '{"Hello": "Hallo"}' > assets/locales/your_script_de_DE.json
```

---

## 📋 Common Locale Codes

| Code | Language | Region |
|------|----------|--------|
| `de_DE` | German | Germany |
| `de_AT` | German | Austria |
| `de_CH` | German | Switzerland |
| `en_US` | English | United States |
| `en_GB` | English | United Kingdom |
| `fr_FR` | French | France |
| `es_ES` | Spanish | Spain |
| `it_IT` | Italian | Italy |
| `pt_BR` | Portuguese | Brazil |
| `ja_JP` | Japanese | Japan |
| `zh_CN` | Chinese | China (Simplified) |
| `zh_TW` | Chinese | Taiwan (Traditional) |
| `ru_RU` | Russian | Russia |
| `ar_SA` | Arabic | Saudi Arabia |

---

## 🆕 What's New in v2.0

### API Changes
- ✅ `set_locale()` replaces old `tr_init()` (more intuitive)
- ✅ `locale_code` parameter in `__init__()` for immediate setup
- ✅ `install()` / `uninstall()` methods for global `_()` access
- ✅ `get_locale()` to query current locale
- ✅ `list_locales()` to discover available languages
- ✅ `_()` as official alias for `tr()`

### New Features
- ✅ Warning system for `install()` to prevent conflicts
- ✅ Improved placeholder validation with visual feedback
- ✅ Translation progress statistics
- ✅ Enhanced error handling throughout
- ✅ Fallback locale support
- ✅ Better type hints for IDE support

### UI Improvements
- ✅ Statistics display (translation completion %)
- ✅ Better visual feedback (orange for errors)
- ✅ File picker filters (.py files only)
- ✅ Improved button states (disabled when appropriate)
- ✅ Better error messages


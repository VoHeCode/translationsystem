# Translation Extractor UI - Complete Guide

## Overview

The `run_tr_extractor_ui()` method launches a graphical user interface (GUI) for extracting, editing, and managing translation strings in your Python applications.

## Method Signature

```python
def run_tr_extractor_ui(self) -> None:
    """Launch the translation editor GUI."""
```

## What It Does

The Translation Extractor UI is a Flet-based graphical application that:

1. **Scans Python source files** for translation calls (`tr()` and `_()`)
2. **Extracts all translatable strings** automatically
3. **Creates/updates JSON translation files** in the correct format
4. **Provides a side-by-side editor** for original text and translations
5. **Validates placeholders** (e.g., `{name}`, `{count}`) to prevent errors
6. **Supports multiple locales** (languages)
7. **Offers search and filter** capabilities
8. **Includes undo/redo** for safe editing

## Features

### Automatic String Extraction

- Finds all `tr("text")` and `_("text")` calls in your Python code
- Supports both single and double quotes
- Handles strings with optional fontsize parameter: `tr("text", 16)`
- Adds new strings to existing translation files without overwriting

### Side-by-Side Editor

- **Left column:** Original English text (read-only)
- **Right column:** Translation (editable, multiline with word wrap)
- **Color coding:** Orange background highlights missing placeholders

### Placeholder Validation

- Automatically detects placeholders like `{name}`, `{count}`, `{date}`
- Warns when placeholders are missing in translations
- Auto-appends missing placeholders when saving
- Shows warning banner with count of problematic entries

### Translation Management

- **Search:** Filter strings by content
- **Sort:** Alphabetically or keep original order
- **Statistics:** Shows progress (e.g., "45/100 translated (45%)")
- **Undo/Redo:** Safe editing with full history

### File Handling

- Creates directory structure automatically: `assets/locales/`
- Naming convention: `{scriptname}_{locale}.json`
- Preserves existing translations when re-scanning
- Handles line breaks correctly (preserves for multiline, removes for single-line)

## Use Cases

### Use Case 1: Starting a New Project

**Scenario:** You've written your app in English and want to add German translations.

**Steps:**

1. Write your Python code with translation calls:
   ```python
   # myapp.py
   from translator import TranslationSystem
   
   ts = TranslationSystem("de_DE")
   _ = ts.tr
   
   print(_("Welcome to my application"))
   print(_("User {name} has {count} messages"))
   ```

2. Launch the extractor:
   ```python
   ts = TranslationSystem()
   ts.run_tr_extractor_ui()
   ```

3. In the UI:
   - Click "Select Python File" → choose `myapp.py`
   - Select locale: `de_DE` (German)
   - The UI extracts all strings automatically
   - Edit translations in the right column:
     - "Welcome to my application" → "Willkommen in meiner Anwendung"
     - "User {name} has {count} messages" → "Benutzer {name} hat {count} Nachrichten"
   - Click "Save"

4. Result: `assets/locales/myapp_de_DE.json` is created with your translations

### Use Case 2: Adding a New Language

**Scenario:** Your app already has German translations, now you want French.

**Steps:**

1. Launch the extractor:
   ```python
   ts.run_tr_extractor_ui()
   ```

2. In the UI:
   - Select your Python file
   - **Change locale to `fr_FR`** (French)
   - All English strings appear again (empty translations)
   - Translate to French:
     - "Settings" → "Paramètres"
     - "Exit" → "Quitter"
   - Click "Save"

3. Result: New file `assets/locales/myapp_fr_FR.json` is created

### Use Case 3: Adding New Features to Existing App

**Scenario:** You've added new features with new strings to your app.

**Steps:**

1. Add new translation calls to your code:
   ```python
   print(_("New feature activated"))
   print(_("Download complete"))
   ```

2. Launch extractor and select your file + locale

3. The UI shows:
   - All old strings with their existing translations ✅
   - New strings with empty translations (need translation)

4. Translate only the new strings

5. Click "Save" → existing translations are preserved, new ones are added

### Use Case 4: Fixing Translation Errors

**Scenario:** You notice some translations are wrong or have missing placeholders.

**Steps:**

1. Launch extractor, select file and locale

2. Use **Search** to find specific strings:
   - Type "message" in search box
   - Only matching strings appear

3. Fix translations in the editor:
   - Orange background indicates missing placeholders
   - Add missing placeholders or correct text
   - Use Undo if you make a mistake

4. Click "Save"

### Use Case 5: Team Workflow

**Scenario:** Multiple translators working on different languages.

**Steps:**

**Developer:**
1. Writes code with `tr()` calls
2. Runs extractor to create `myapp_en_US.json` (base language)
3. Commits to Git

**German Translator:**
1. Pulls latest code
2. Runs extractor, selects `de_DE`
3. Translates all strings
4. Saves and commits `myapp_de_DE.json`

**French Translator:**
1. Pulls latest code
2. Runs extractor, selects `fr_FR`
3. Translates all strings
4. Saves and commits `myapp_fr_FR.json`

**Result:** Each translator works on their own JSON file without conflicts

### Use Case 6: Handling Complex Strings

**Scenario:** Working with strings that have multiple placeholders or line breaks.

**Example strings:**
```python
_("Hello {name}, you have {count} messages from {sender}")
_("Line 1\nLine 2\nLine 3")
```

**In the UI:**

1. **Placeholders:** The UI highlights if any placeholder is missing
   - Original: "Hello {name}, you have {count} messages"
   - Translation: "Hallo {name}, Sie haben {count} Nachrichten"
   - ✅ All placeholders present → no warning
   
2. **Line breaks:** Preserved for multiline originals
   - Original has `\n` → translation can also have line breaks
   - Editor shows multiline text field (word wrap enabled)
   - Saving preserves line breaks

## UI Components Explained

### Top Section

- **Warning Banner (orange):** Shows count of entries with missing placeholders
- **Locale Dropdown:** Select target language (de_DE, en_US, fr_FR, etc.)
- **Select Python File Button:** Opens file picker to choose source file

### Results Section

- **File path:** Shows location of created/updated JSON file
- **Found strings:** Total count of translatable strings in source
- **Newly added:** Count of strings added in this session

### Editor Section

- **Search Field:** Filter strings by content (searches both original and translation)
- **Sort Dropdown:** "original" (source order) or "alphabetisch" (A-Z)
- **Undo/Redo Buttons:** Navigate editing history
- **Save Button:** Write changes to JSON file

### Translation Grid

Each row shows:
- **Left:** Original text (fixed width 400px, read-only)
- **Right:** Translation text field (expandable, multiline, 1-5 lines, word wrap)

**Color coding:**
- White background: All placeholders present ✅
- Orange background: Missing placeholders ⚠️

### Bottom Section

- **Statistics:** Translation progress (e.g., "45/100 translated (45%)")
- **Save Status:** Confirmation message after saving

## File Output

### Location

```
your_project/
└── assets/
    └── locales/
        ├── myapp_de_DE.json
        ├── myapp_en_US.json
        └── myapp_fr_FR.json
```

### File Format

```json
{
  "Hello World": "Hallo Welt",
  "Settings": "Einstellungen",
  "User {name} has {count} messages": "Benutzer {name} hat {count} Nachrichten",
  "Multi-line\nText": "Mehrzeiliger\nText"
}
```

**Rules:**
- Keys: Original English strings (exactly as in code)
- Values: Translated strings
- Encoding: UTF-8 with `ensure_ascii=False`
- Formatting: Indented with 2 spaces
- Placeholders: Must match original (auto-added if missing)

## Technical Details

### Supported Patterns

The extractor recognizes these patterns in your Python code:

```python
tr('text')                    ✅
tr("text")                    ✅
tr('text', 16)               ✅
tr("text", fontsize=20)      ✅
_('text')                    ✅
_("text")                    ✅
_("text", 16)                ✅
```

**Regex pattern:**
```python
r'(?:tr|_)\(\s*[\'"](.+?)[\'"]\s*(?:,.*?)?\)'
```

### Placeholder Handling

**Extraction:**
```python
pattern = r"\{[^{}]*\}"
```

**Validation:**
- Extracts all `{...}` from original string
- Checks if all are present in translation
- Marks translation as invalid if any missing
- Auto-appends missing placeholders when saving

**Example:**
```
Original:    "Hello {name}, you have {count} messages"
Translation: "Hallo {name}"  # Missing {count}!
→ Orange background in UI
→ On save: auto-adds " {count}" at the end
```

### Line Break Handling

**Single-line strings (no `\n` in original):**
```python
# Original
"This is a long text"

# Translation (user types with line breaks for readability)
"Das ist ein
langer Text"

# Saved as (line breaks removed):
"Das ist ein langer Text"
```

**Multi-line strings (`\n` in original):**
```python
# Original
"Line 1\nLine 2"

# Translation (line breaks preserved)
"Zeile 1\nZeile 2"

# Saved as (line breaks kept):
"Zeile 1\nZeile 2"
```

## Limitations & Notes

### Cannot Be Called from Flet App

```python
# ❌ WRONG - nested ft.app() calls
def main(page: ft.Page):
    ts.run_tr_extractor_ui()  # Will crash!

ft.app(target=main)

# ✅ CORRECT - separate script
ts = TranslationSystem()
ts.run_tr_extractor_ui()
```

**Reason:** The method calls `ft.app()` internally, which can't run inside another Flet application.

**Solution:** Run the extractor as a standalone script or from your main code before launching your app.

### Blocking Execution

```python
ts.run_tr_extractor_ui()  # Blocks here until UI is closed
print("This runs after closing the UI")
```

The method doesn't return until the user closes the GUI window.

### File Overwrite Behavior

- **Existing translations:** Preserved ✅
- **New strings:** Added with original text as default
- **Removed strings:** Kept in JSON (not automatically deleted)
- **Modified originals:** Creates new entry (old one remains)

### Locale Detection

Default locale is detected from system:
```python
import locale
lang, enc = locale.getlocale()  # e.g., ('de_DE', 'UTF-8')
```

Can be overridden in the UI dropdown.

## Best Practices

### 1. Run Early and Often

Extract translations frequently during development:
- After adding new features
- Before sending to translators
- Before releasing new versions

### 2. Use Descriptive Strings

```python
# ❌ Bad (hard to translate without context)
_("OK")
_("Cancel")

# ✅ Good (clear context)
_("Confirm deletion")
_("Cancel operation")
```

### 3. Keep Placeholders Clear

```python
# ❌ Bad (confusing)
_("User {} has {} messages")  # Which is which?

# ✅ Good (self-documenting)
_("User {name} has {count} messages")
```

### 4. Use Complete Sentences

```python
# ❌ Bad (fragments)
_("Are you sure") + " " + _("you want to delete") + "?"

# ✅ Good (complete)
_("Are you sure you want to delete this file?")
```

### 5. Test All Locales

After translating:
```python
for locale in ["de_DE", "en_US", "fr_FR"]:
    ts.set_locale(locale)
    print(ts.tr("Settings"))  # Verify it works
```

## Troubleshooting

### "File not found" when running app

**Problem:** Translation JSON file doesn't exist

**Solution:** Run the extractor to create it, or create manually

### Strings not extracted

**Problem:** Pattern doesn't match your code style

**Check:**
- Are you using `tr()` or `_()`?
- Are strings in quotes? `tr('text')` not `tr(variable)`
- Is there a typo? `tr("text", 16)` works, `tr("text" 16)` doesn't

### Placeholder warnings persist

**Problem:** Typo in placeholder name

**Example:**
```python
Original:    "Hello {name}"
Translation: "Hallo {naem}"  # Typo!
```

**Solution:** Fix the typo - must match exactly: `{name}` = `{name}`

### Can't find my Python file

**Problem:** File picker doesn't show your file

**Solution:** 
- Check file extension is `.py`
- Navigate to correct directory
- PyCharm users: Use absolute path

### Changes not saved

**Problem:** Clicked wrong button or file permissions

**Solution:**
- Make sure you clicked "Save" button
- Check file permissions in `assets/locales/`
- Look for error message in UI

## Keyboard Shortcuts

- **Search:** Click in search field, type to filter
- **Tab:** Move between translation fields
- **Enter:** New line in multiline field
- **Ctrl+Z:** Undo (when clicking Undo button)

## Integration Examples

### Standalone Extractor Script

```python
# extract_translations.py
from translator import TranslationSystem

if __name__ == "__main__":
    ts = TranslationSystem()
    ts.run_tr_extractor_ui()
```

Run with:
```bash
python extract_translations.py
```

### With Command Line Arguments

```python
# myapp.py
import sys
from translator import TranslationSystem

if len(sys.argv) > 1 and sys.argv[1] == "--extract":
    ts = TranslationSystem()
    ts.run_tr_extractor_ui()
else:
    # Normal app code
    ts = TranslationSystem("de_DE")
    # ...
```

Run extractor:
```bash
python myapp.py --extract
```

Run app:
```bash
python myapp.py
```

## Summary

The Translation Extractor UI is a powerful tool that:

✅ Automates the tedious work of finding translatable strings  
✅ Prevents errors with placeholder validation  
✅ Supports team workflows with separate locale files  
✅ Provides an intuitive interface for translators  
✅ Maintains consistency across updates  

**When to use:**
- Starting a new project with internationalization
- Adding languages to existing projects
- Maintaining translations as code evolves
- Collaborating with translators

**When NOT to use:**
- From within a Flet application (use separate script)
- For runtime translation switching (use `set_locale()` instead)
- For automated CI/CD pipelines (consider command-line tools)

The UI complements the `TranslationSystem` class by handling the extraction and editing workflow, while your application code handles the runtime translation with `tr()` / `_()` calls.

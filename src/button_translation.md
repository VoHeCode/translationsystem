# tr_size() - Automatisches Font-Resizing

## Wie funktioniert's?

```python
ts = TranslationSystem("de_DE")

# 1. Original-Text übersetzen
text = ts.tr("Settings", 16)  # "Settings" → "Einstellungen"

# 2. Neue Fontgröße abrufen (damit gleiche Breite wie Original)
size = ts.tr_size()  # z.B. 11pt statt 16pt

# 3. In Flet verwenden
button = ft.ElevatedButton(text, style=ft.ButtonStyle(
    text_style=ft.TextStyle(size=size)))
```

## Was passiert intern?

1. `tr("Settings", 16)` misst "Settings" bei 16pt → z.B. 80px breit
2. Übersetzt zu "Einstellungen" (länger!)
3. Berechnet: Welche Fontgröße braucht "Einstellungen" für 80px? → 11pt
4. `tr_size()` gibt 11pt zurück

## Ergebnis

✅ Übersetzter Text hat **gleiche Breite** wie Original
✅ UI-Elemente behalten ihre Größe
✅ Kein Text-Overflow in Buttons/Labels

## Beispiel: Button-Reihe

```python
def make_button(key):
    text = ts.tr(key, 16)
    return ft.ElevatedButton(text, style=ft.ButtonStyle(
        text_style=ft.TextStyle(size=ts.tr_size())))

# Alle Buttons haben gleiche Breite, egal welche Sprache!
page.add(ft.Row([
    make_button("Save"),     # "Speichern"
    make_button("Cancel"),   # "Abbrechen"
    make_button("OK"),       # "OK"
]))
```

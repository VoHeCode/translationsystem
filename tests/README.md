# Tests

## Installation

```bash
pip install pytest
```

## Tests ausführen

```bash
# Alle Tests
pytest

# Mit Ausgabe
pytest -v

# Nur eine Datei
pytest tests/test_translator.py

# Mit Coverage
pytest --cov=src
```

## Struktur

```
tests/
├── __init__.py           # Leere Package-Datei
└── test_translator.py    # Tests für TranslationSystem
```

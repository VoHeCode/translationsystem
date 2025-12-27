#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo file showing TranslationSystem usage.
This file demonstrates both tr() and _() syntax.
"""

import sys
from translator import TranslationSystem


# ============================================================
# Example 1: Local alias (RECOMMENDED)
# ============================================================
def demo_local_alias():
    """Recommended: Use local alias for _()."""
    ts = TranslationSystem("de_DE")
    _ = ts.tr  # Local alias - no global pollution!

    print("=== Demo 1: Local Alias ===")
    print(_("Hello World"))
    print(_("Welcome to the application"))
    print(_("User {name} has {count} messages").format(name="Alice", count=5))
    print()


# ============================================================
# Example 2: Global installation (use with caution)
# ============================================================
def demo_global_install():
    """Alternative: Global installation (with warning)."""
    ts = TranslationSystem("de_DE")
    ts.install()  # Makes _() available globally

    print("=== Demo 2: Global Install ===")
    print(_("Hello World"))
    print(_("This uses global _() function"))
    print()

    # Clean up
    ts.uninstall()


# ============================================================
# Example 3: Direct tr() usage
# ============================================================
def demo_direct_tr():
    """Using tr() directly without alias."""
    ts = TranslationSystem("de_DE")

    print("=== Demo 3: Direct tr() ===")
    print(ts.tr("Hello World"))
    print(ts.tr("Settings"))
    print(ts.tr("Exit"))
    print()


# ============================================================
# Example 4: Dynamic locale switching
# ============================================================
def demo_locale_switching():
    """Demonstrate locale switching."""
    ts = TranslationSystem()
    _ = ts.tr

    print("=== Demo 4: Locale Switching ===")

    # German
    ts.set_locale("de_DE")
    print(f"[de_DE] {_('Hello World')}")

    # English
    ts.set_locale("en_US")
    print(f"[en_US] {_('Hello World')}")

    # French
    ts.set_locale("fr_FR")
    print(f"[fr_FR] {_('Hello World')}")
    print()


# ============================================================
# Example 5: Text measurement and sizing
# ============================================================
def demo_text_sizing():
    """Demonstrate dynamic text sizing."""
    ts = TranslationSystem("de_DE")
    _ = ts.tr

    print("=== Demo 5: Text Sizing ===")

    # Measure text
    text = _("Button Label")
    print(f"Text: '{text}'")
    print(f"Width: {ts.get_width()}px")
    print(f"Height: {ts.get_height()}px")

    # Calculate font size to fit width
    target_width = 200
    new_size = ts.resize_text(text, target_width, ref_size=20)
    print(f"Font size to fit {target_width}px: {new_size}pt")
    print(f"Via tr_size(): {ts.tr_size()}pt")
    print()


# ============================================================
# Example 6: Multi-line strings
# ============================================================
def demo_multiline():
    """Demonstrate multi-line string handling."""
    ts = TranslationSystem("de_DE")
    _ = ts.tr

    print("=== Demo 6: Multi-line Strings ===")

    multiline = _("First line\nSecond line\nThird line")
    print(multiline)
    print()


# ============================================================
# Example 7: Placeholder validation
# ============================================================
def demo_placeholders():
    """Demonstrate placeholder handling."""
    ts = TranslationSystem("de_DE")
    _ = ts.tr

    print("=== Demo 7: Placeholders ===")

    # Extract placeholders
    text = "Hello {name}, you have {count} new messages"
    placeholders = ts.extract_placeholders(text)
    print(f"Text: '{text}'")
    print(f"Placeholders: {placeholders}")

    # Use translation
    translated = _("Hello {name}, you have {count} new messages")
    print(f"Translated: {translated.format(name='Bob', count=3)}")
    print()


# ============================================================
# Example 8: List available locales
# ============================================================
def demo_list_locales():
    """Show available locales."""
    ts = TranslationSystem()

    print("=== Demo 8: Available Locales ===")
    locales = ts.list_locales()
    print(f"Available locales: {locales}")
    print()


# ============================================================
# Main demo runner
# ============================================================
def main(args=None):
    """Run all demos or launch UI."""

    if args and len(args) > 1:
        if args[1] == "--ui" or args[1] == "-u":
            # Launch extractor UI
            ts = TranslationSystem()
            ts.run_tr_extractor_ui()
            return
        elif args[1] == "--help" or args[1] == "-h":
            print("Usage: python demo.py [--ui | --help]")
            print()
            print("Options:")
            print("  --ui, -u     Launch translation extractor UI")
            print("  --help, -h   Show this help message")
            print()
            print("Without arguments: Run all demos")
            return

    # Run all demos
    print("=" * 60)
    print("TranslationSystem Demo")
    print("=" * 60)
    print()

    demo_local_alias()
    demo_direct_tr()
    demo_locale_switching()
    demo_text_sizing()
    demo_multiline()
    demo_placeholders()
    demo_list_locales()

    # Skipping global install demo to avoid warnings
    # Uncomment to test:
    # demo_global_install()

    print("=" * 60)
    print("To launch the translation editor UI, run:")
    print("  python demo.py --ui")
    print("=" * 60)


if __name__ == '__main__':
    main(sys.argv)

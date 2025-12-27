#!/usr/bin/env python3
# *_* coding: utf-8 *_*
"""Minimal Flet Demo: tr() + tr_size() for auto-sized buttons"""
import flet as ft
from translator import TranslationSystem

ts = TranslationSystem("de_DE")
_ = ts.tr
# ts.run_tr_extractor_ui()# comment this after each settig
# exit() # comment this after each settig

def main(page: ft.Page):
    # Exit button handler
    def exit_app(e):
        page.window.close()

    print(ts.tr('This does nothing, but looks good'))
    print(_("This is also possible, with the code above."))
    FONTSIZE = 30
    # Translate text at 16pt, then use calculated size for button
    text = ts.tr("Settings", FONTSIZE)

    page.theme = ft.Theme(
        font_family="Roboto",
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(size=FONTSIZE)
        )
    )

        # Rest deines Codes...
    page.add(
        ft.ElevatedButton(text, style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=ts.tr_size()))),
        ft.ElevatedButton(_("Exit",FONTSIZE), on_click=exit_app, style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=ts.tr_size())))
    )


ft.app(target=main)
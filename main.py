import flet as ft
import os
from layout import create_appbar
from settings import Settings
from solitaire import Solitaire




def main(page: ft.Page):
    page.title = "Flet Solitaire"
    
    rules_md = ft.Markdown(
        """
    Klondike is played with a standard 52-card deck, without Jokers.

    The four foundations (light rectangles in the upper right of the figure) are built up by suit from Ace (low in this game) to King, and the tableau piles can be built down by alternate colors. Every face-up card in a partial pile, or a complete pile, can be moved, as a unit, to another tableau pile on the basis of its highest card. Any empty piles can be filled with a King, or a pile of cards with a King. The aim of the game is to build up four stacks of cards starting with Ace and ending with King, all of the same suit, on one of the four foundations, at which time the player would have won. There are different ways of dealing the remainder of the deck from the stock to the waste, which can be selected in the Settings:

    - Turning three cards at once to the waste, with no limit on passes through the deck.
    - Turning three cards at once to the waste, with three passes through the deck.
    - Turning one card at a time to the waste, with three passes through the deck.
    - Turning one card at a time to the waste, with no limit on passes through the deck.

    If the player can no longer make any meaningful moves, the game is considered lost.
        """
    )

    rules_dialog = ft.AlertDialog(
        title=ft.Text("Solitaire rules"),
        content=rules_md,
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    def show_rules(e):
        page.overlay.append(rules_dialog)
        rules_dialog.open = True
        page.update()

    def on_undo():
        if len(page.controls) > 0:
            solitaire_instance = page.controls[-1]
            if hasattr(solitaire_instance, 'undo'):
                solitaire_instance.undo()

    def on_new_game(settings):
        launch_game(settings, load_save=False)

    def launch_game(settings, load_save=False):
        page.controls.clear()
        
        create_appbar(page, settings, on_new_game, on_undo, show_main_menu)
        new_solitaire = Solitaire(settings, on_win, load_save=load_save)
        page.add(new_solitaire)
        page.update()

    def on_win():
        win_dialog = ft.AlertDialog(
            title=ft.Text("YOU WIN!"),
            on_dismiss=lambda e: show_main_menu(),
        )
        page.overlay.append(win_dialog)
        win_dialog.open = True
        page.update()
        print("You win")

    def show_main_menu():
        page.appbar = None
        page.controls.clear()
        
        has_save = os.path.exists("savegame.json")
        
        menu_controls = [
            ft.Text("Flet Solitaire", size=40, weight=ft.FontWeight.BOLD),
            ft.Container(height=30), # Spacer
            ft.FilledButton("New Game", on_click=lambda e: launch_game(Settings(), False), width=200, height=50),
        ]
        
        if has_save:
            menu_controls.append(
                ft.FilledButton("Continue Game", on_click=lambda e: launch_game(Settings(), True), width=200, height=50)
            )
            
        menu_controls.append(
            ft.FilledButton("Rules", on_click=show_rules, width=200, height=50)
        )
        
        menu_view = ft.Container(
            content=ft.Column(
                controls=menu_controls,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15
            ),
            alignment=ft.Alignment(0, 0),
            expand=True
        )
        
        page.add(menu_view)
        page.update()

    show_main_menu()

ft.run(main, assets_dir="assets")
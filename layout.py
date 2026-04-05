import flet as ft
from settings import SettingsDialog

def create_appbar(page, settings, on_new_game, on_undo, on_save, on_back_to_menu):
    def new_game_clicked(e):
        on_new_game(settings)

    def show_rules(e):
        page.overlay.append(rules_dialog)
        rules_dialog.open = True
        page.update()

    def show_settings(e):
        settings_dialog = SettingsDialog(settings, on_new_game)
        page.overlay.append(settings_dialog)
        settings_dialog.open = True
        page.update()

    score_text = ft.Text("Score: 0", weight=ft.FontWeight.BOLD, size=16)
    timer_text = ft.Text("Time: 00:00", weight=ft.FontWeight.BOLD, size=16)
    moves_text = ft.Text("Moves: 0", weight=ft.FontWeight.BOLD, size=16)

    appbar_title_row = ft.Row(
        controls=[
            ft.Text("Flet Solitaire", size=18),
            ft.Container(width=20), 
            score_text,
            ft.Container(width=10), 
            timer_text,
            ft.Container(width=10),
            moves_text  
        ],
        wrap=True
    )

    page.appbar = ft.AppBar(
        leading=ft.Image(src="/images/card.png"),
        leading_width=30,
        title=appbar_title_row,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.SAVE, on_click=lambda e: on_save(), tooltip="Save Game"),
            ft.IconButton(ft.Icons.UNDO, on_click=lambda e: on_undo(), tooltip="Undo Move"),
            ft.IconButton(ft.Icons.ADD_BOX, on_click=new_game_clicked, tooltip="New Game"),
            ft.IconButton(ft.Icons.MENU_BOOK, on_click=show_rules, tooltip="Rules"),
            ft.IconButton(ft.Icons.SETTINGS, on_click=show_settings, tooltip="Settings"),
            ft.IconButton(ft.Icons.HOME, on_click=lambda e: on_back_to_menu(), tooltip="Back to Menu"),
        ],
    )

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

    rules_content = ft.Container(
        content=ft.Column([rules_md], scroll=ft.ScrollMode.AUTO, tight=True)
    )

    rules_dialog = ft.AlertDialog(
        title=ft.Text("Solitaire rules"),
        content=rules_content,
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )
    
    return score_text, timer_text, moves_text
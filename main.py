import flet as ft
import os
import json
from layout import create_appbar
from settings import Settings, SettingsDialog
from solitaire import Solitaire

def main(page: ft.Page):
    page.title = "Flet Solitaire"
    
    page.scroll = "auto"
    
    app_settings = Settings()
    
    if os.path.exists("global_stats.json"):
        with open("global_stats.json", "r") as f:
            stats = json.load(f)
            app_settings.best_score = stats.get("best_score", 0)
            app_settings.best_time = stats.get("best_time", float('inf'))
            app_settings.least_moves = stats.get("least_moves", float('inf'))
    
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

    def on_menu_settings_applied(new_settings):
        nonlocal app_settings
        app_settings = new_settings

    def show_settings_from_menu(e):
        settings_dialog = SettingsDialog(app_settings, on_menu_settings_applied)
        page.overlay.append(settings_dialog)
        settings_dialog.open = True
        page.update()

    def on_undo():
        if len(page.controls) > 0:
            solitaire_instance = page.controls[-1]
            if hasattr(solitaire_instance, 'undo'):
                solitaire_instance.undo()

    def on_save():
        if len(page.controls) > 0:
            solitaire_instance = page.controls[-1]
            if hasattr(solitaire_instance, 'save_game'):
                solitaire_instance.save_game()
                page.snack_bar = ft.SnackBar(ft.Text("Game manually saved!"), duration=2000)
                page.snack_bar.open = True
                page.update()

    def on_new_game(settings):
        if len(page.controls) > 0 and isinstance(page.controls[-1], Solitaire):
            active_game = page.controls[-1]
            active_game.check_and_save_high_score(game_won=False)
            
        launch_game(settings, load_save=False)

    def launch_game(settings, load_save=False):
        page.controls.clear()
        
        score_text, timer_text, moves_text = create_appbar(page, settings, on_new_game, on_undo, on_save, show_main_menu)
        
        new_solitaire = Solitaire(settings, on_win, score_text, timer_text, moves_text, load_save=load_save)
        page.add(new_solitaire)
        page.update()

    def on_win():
        if os.path.exists("global_stats.json"):
            with open("global_stats.json", "r") as f:
                stats = json.load(f)
                app_settings.best_score = stats.get("best_score", 0)
                app_settings.best_time = stats.get("best_time", float('inf'))
                app_settings.least_moves = stats.get("least_moves", float('inf'))
                
        win_dialog = ft.AlertDialog(
            title=ft.Text("YOU WIN!"),
            on_dismiss=lambda e: show_main_menu(),
        )
        page.overlay.append(win_dialog)
        win_dialog.open = True
        page.update()

    def show_main_menu():
        if len(page.controls) > 0 and isinstance(page.controls[-1], Solitaire):
            active_game = page.controls[-1]
            active_game.check_and_save_high_score(game_won=False)
            active_game.is_running = False
            
        if os.path.exists("global_stats.json"):
            with open("global_stats.json", "r") as f:
                stats = json.load(f)
                app_settings.best_score = stats.get("best_score", 0)
                app_settings.best_time = stats.get("best_time", float('inf'))
                app_settings.least_moves = stats.get("least_moves", float('inf'))
            
        page.appbar = None
        page.controls.clear()
        
        has_save = os.path.exists("savegame.json")
        
        best_time_str = "--:--"
        if app_settings.best_time != float('inf'):
            mins, secs = divmod(app_settings.best_time, 60)
            best_time_str = f"{mins:02d}:{secs:02d}"

        least_moves_str = str(app_settings.least_moves) if app_settings.least_moves != float('inf') else "--"
            
        stats_display = ft.Row([
            ft.Text(f"High Score: {app_settings.best_score}", size=16, color=ft.Colors.GREY_400),
            ft.Text("|", size=16, color=ft.Colors.GREY_400),
            ft.Text(f"Fastest Time: {best_time_str}", size=16, color=ft.Colors.GREY_400),
            ft.Text("|", size=16, color=ft.Colors.GREY_400),
            ft.Text(f"Least Moves: {least_moves_str}", size=16, color=ft.Colors.GREY_400)
        ], alignment=ft.MainAxisAlignment.CENTER, wrap=True)
        
        menu_controls = [
            ft.Text("Flet Solitaire", size=40, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            stats_display,
            ft.Container(height=30), 
            ft.FilledButton("New Game", on_click=lambda e: launch_game(app_settings, False), width=250, height=50),
        ]
        
        if has_save:
            menu_controls.append(
                ft.FilledButton("Continue Game", on_click=lambda e: launch_game(app_settings, True), width=250, height=50)
            )
            
        menu_controls.extend([
            ft.FilledButton("Personalization & Settings", on_click=show_settings_from_menu, width=250, height=50),
            ft.FilledButton("Rules", on_click=show_rules, width=250, height=50)
        ])
        
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

ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=8080, assets_dir="assets")
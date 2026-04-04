import flet as ft


class Settings:
    def __init__(
        self, waste_size=3, deck_passes_allowed=1000, card_back="/images/card_back0.png", table_background=ft.Colors.GREEN_900, best_score=0, best_time=float('inf'), least_moves=float('inf')
    ):
        self.waste_size = waste_size
        self.deck_passes_allowed = deck_passes_allowed
        self.card_back = card_back
        self.table_background = table_background
        self.best_score = best_score
        self.best_time = best_time
        self.least_moves = least_moves


class SettingsDialog(ft.AlertDialog):
    def __init__(self, settings, on_settings_applied):
        super().__init__()
        self.on_settings_applied = on_settings_applied
        self.settings = settings
        self.modal = True
        self.title = ft.Text("Personalization & Settings")
        
        self.waste_size = ft.RadioGroup(
            value=self.settings.waste_size,
            content=ft.Row(
                controls=[
                    ft.Radio(value=1, label="One card"),
                    ft.Radio(value=3, label="Three cards"),
                ]
            ),
        )
        self.deck_passes_allowed = ft.RadioGroup(
            value=self.settings.deck_passes_allowed,
            content=ft.Row(
                controls=[
                    ft.Radio(value=3, label="Three"),
                    ft.Radio(value=1000, label="Unlimited"),
                ]
            ),
        )
        
        self.table_background = ft.RadioGroup(
            value=self.settings.table_background,
            content=ft.Column(
                controls=[
                    ft.Radio(value=ft.Colors.GREEN_900, label="Classic Felt"),
                    ft.Radio(value=ft.Colors.BROWN_800, label="Wood Table"),
                    ft.Radio(value=ft.Colors.BLUE_900, label="Casino Blue"),
                    ft.Radio(value=ft.Colors.GREY_900, label="Dark Mode"),
                ]
            )
        )

        self.generate_card_backs()

        self.content = ft.Column(
            controls=[
                ft.Text("Table Background:", weight=ft.FontWeight.BOLD),
                self.table_background,
                ft.Container(height=10),
                ft.Text("Card Back Design:", weight=ft.FontWeight.BOLD),
                ft.Row(controls=self.card_backs),
                ft.Divider(height=20, color=ft.Colors.WHITE24),
                ft.Text("Gameplay Rules", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Waste pile size:"),
                self.waste_size,
                ft.Text("Passes through the deck:"),
                self.deck_passes_allowed,
                ft.Container(height=10),
                ft.Checkbox(
                    label="Applying settings during a game will restart it.",
                    value=True,
                    disabled=True,
                ),
            ],
            tight=True,
        )
        self.actions = [
            ft.TextButton("Cancel", on_click=self.cancel),
            ft.FilledButton("Apply settings", on_click=self.apply_settings),
        ]

    def generate_card_backs(self):
        self.card_backs = []
        for i in range(4):
            is_selected = self.settings.card_back == f"/images/card_back{i}.png"
            border_style = ft.border.all(3, ft.Colors.BLUE) if is_selected else None
            
            card = ft.Container(
                width=70,
                height=100,
                content=ft.Image(src=f"/images/card_back{i}.png"),
                border_radius=ft.border_radius.all(6),
                on_click=self.choose_card_design,
                data=i,
                border=border_style
            )
            self.card_backs.append(card)
            
            if is_selected:
                self.selected_card = card

        if not hasattr(self, 'selected_card'):
            self.selected_card = self.card_backs[0]
            self.selected_card.border = ft.border.all(3, ft.Colors.BLUE)

    def choose_card_design(self, e):
        for card in self.card_backs:
            if card.data != e.control.data:
                card.border = None
        e.control.border = ft.border.all(3, ft.Colors.BLUE)
        self.selected_card = e.control
        self.update()

    def cancel(self, e):
        self.waste_size.value = self.settings.waste_size
        self.deck_passes_allowed.value = self.settings.deck_passes_allowed
        self.table_background.value = self.settings.table_background
        self.open = False
        self.update()

    def apply_settings(self, e):
        self.settings.waste_size = int(self.waste_size.value)
        self.settings.deck_passes_allowed = int(self.deck_passes_allowed.value)
        self.settings.card_back = self.selected_card.content.src
        self.settings.table_background = self.table_background.value
        self.on_settings_applied(self.settings)
        self.open = False
        self.update()
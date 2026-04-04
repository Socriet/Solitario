import random
import json
import os
import asyncio
import flet as ft
from card import Card
from slot import Slot


class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value


class Solitaire(ft.Stack):
    def __init__(self, settings, on_win, score_text, timer_text, load_save=False):
        super().__init__()
        self.width = 1000
        self.height = 500
        self.current_top = 0
        self.current_left = 0
        self.card_offset = 20
        self.settings = settings
        self.deck_passes_remaining = int(self.settings.deck_passes_allowed)
        self.controls = []
        self.on_win = on_win
        self.history = [] 
        self.load_save = load_save 
        
       
        self.score_text = score_text
        self.timer_text = timer_text
        self.score = 0
        self.elapsed_time = 0
        self.is_running = True

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()
        
        if self.load_save:
            self.load_game_state()
        else:
            self.deal_cards()
            
    
        self.page.run_task(self.update_timer)

    def will_unmount(self):
        self.is_running = False

    async def update_timer(self):
        while self.is_running:
            await asyncio.sleep(1)
            self.elapsed_time += 1
            self.update_ui_texts()

    def update_ui_texts(self):
        mins, secs = divmod(self.elapsed_time, 60)
        self.timer_text.value = f"Time: {mins:02d}:{secs:02d}"
        self.score_text.value = f"Score: {self.score}"
        self.timer_text.update()
        self.score_text.update()

    def add_score(self, points):
        self.score += points
        self.update_ui_texts()

    def save_game(self):
        state = {
            "settings": {
                "waste_size": self.settings.waste_size,
                "deck_passes_allowed": self.settings.deck_passes_allowed,
                "card_back": self.settings.card_back,
                "table_background": self.settings.table_background,
                "best_score": self.settings.best_score,
                "best_time": self.settings.best_time
            },
            "deck_passes_remaining": self.deck_passes_remaining,
            "score": self.score,
            "elapsed_time": self.elapsed_time,
            "slots": {
                "stock": [{"suite": c.suite.name, "rank": c.rank.name, "face_up": c.face_up} for c in self.stock.pile],
                "waste": [{"suite": c.suite.name, "rank": c.rank.name, "face_up": c.face_up} for c in self.waste.pile],
                "foundation": [[{"suite": c.suite.name, "rank": c.rank.name, "face_up": c.face_up} for c in f.pile] for f in self.foundation],
                "tableau": [[{"suite": c.suite.name, "rank": c.rank.name, "face_up": c.face_up} for c in t.pile] for t in self.tableau]
            }
        }
        with open("savegame.json", "w") as f:
            json.dump(state, f)

    def load_game_state(self):
        if not os.path.exists("savegame.json"):
            self.deal_cards()
            return

        with open("savegame.json", "r") as f:
            state = json.load(f)

        if "settings" in state:
            self.settings.waste_size = state["settings"].get("waste_size", 3)
            self.settings.deck_passes_allowed = state["settings"].get("deck_passes_allowed", 1000)
            self.settings.card_back = state["settings"].get("card_back", "/images/card_back0.png")
            
            bg_color = state["settings"].get("table_background", ft.Colors.GREEN_900)
            self.settings.table_background = bg_color
            self.bg.bgcolor = bg_color
            
            self.settings.best_score = state["settings"].get("best_score", 0)
            self.settings.best_time = state["settings"].get("best_time", float('inf'))

        self.deck_passes_remaining = state.get("deck_passes_remaining", 3)
        self.score = state.get("score", 0)
        self.elapsed_time = state.get("elapsed_time", 0)
        self.history = [] 

        def get_card(suite_name, rank_name):
            for c in self.cards:
                if c.suite.name == suite_name and c.rank.name == rank_name:
                    return c
            return None

        def restore_pile(card_data_list, slot):
            for c_data in card_data_list:
                card = get_card(c_data["suite"], c_data["rank"])
                if card:
                    card.place(slot)
                    card.content.content.src = self.settings.card_back
                    if c_data["face_up"]:
                        card.turn_face_up()
                    else:
                        card.turn_face_down()

        restore_pile(state["slots"]["stock"], self.stock)
        restore_pile(state["slots"]["waste"], self.waste)

        for i, f_data in enumerate(state["slots"]["foundation"]):
            restore_pile(f_data, self.foundation[i])

        for i, t_data in enumerate(state["slots"]["tableau"]):
            restore_pile(t_data, self.tableau[i])

        for card in self.stock.pile:
            card.visible = True
            
        for card in self.waste.pile:
            card.visible = False
            
        self.display_waste()
        self.update_ui_texts()
        self.update()

    def create_slots(self):
        self.bg = ft.Container(
            width=1000,
            height=500,
            bgcolor=self.settings.table_background,
            border_radius=10
        )
        self.controls.append(self.bg)

        self.stock = Slot(
            solitaire=self, slot_type="stock", top=10, left=10, border=ft.border.all(1, ft.Colors.WHITE38)
        )

        self.waste = Slot(
            solitaire=self, slot_type="waste", top=10, left=110, border=None
        )

        self.foundation = []
        x = 310
        for i in range(4):
            self.foundation.append(
                Slot(
                    solitaire=self,
                    slot_type="foundation",
                    top=10,
                    left=x,
                    border=ft.border.all(1, ft.Colors.WHITE38),
                )
            )
            x += 100

        self.tableau = []
        x = 10
        for i in range(7):
            self.tableau.append(
                Slot(
                    solitaire=self,
                    slot_type="tableau",
                    top=160,
                    left=x,
                    border=None,
                )
            )
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundation)
        self.controls.extend(self.tableau)
        self.update()

    def create_card_deck(self):
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                file_name = f"{rank.name}_{suite.name}.svg"
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))
        
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        self.update()

    def deal_cards(self):
        card_index = 0
        first_slot = 0
        while card_index <= 27:
            for slot_index in range(first_slot, len(self.tableau)):
                self.cards[card_index].place(self.tableau[slot_index])
                card_index += 1
            first_slot += 1

        for number in range(len(self.tableau)):
            self.tableau[number].get_top_card().turn_face_up()

        for i in range(28, len(self.cards)):
            self.cards[i].place(self.stock)
            
        self.save_game()

    def move_on_top(self, cards_to_drag):
        for card in cards_to_drag:
            self.controls.remove(card)
            self.controls.append(card)

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.slot.type == "tableau":
                card.top += i * self.card_offset
            card.left = self.current_left
            i += 1

    def display_waste(self):
        if self.settings.waste_size == 3:
            self.waste.fan_top_three()
        self.update()

    def restart_stock(self):
        self.waste.pile.reverse()
        while len(self.waste.pile) > 0:
            card = self.waste.pile[0]
            card.turn_face_down()
            card.place(self.stock)
        self.save_game() 
        self.update()

    def undo(self):
        if not self.history:
            return

        last_move = self.history.pop()
        move_type = last_move["type"]

        if move_type == "move":
            if last_move["flipped"]:
                last_move["flipped"].turn_face_down()

            for card in last_move["cards"]:
                card.place(last_move["source"])

            if last_move["source"].type == "waste" or last_move["dest"].type == "waste":
                self.display_waste()
                
            if last_move["dest"].type == "foundation":
                self.add_score(-10)

        elif move_type == "cycle_stock":
            for card in reversed(last_move["cycled_cards"]):
                card.turn_face_down()
                card.visible = True
                card.place(self.stock)

            for card in last_move["hidden_waste_cards"]:
                card.visible = True

            self.display_waste()

        elif move_type == "restart_stock":
            self.stock.pile.reverse()
            while len(self.stock.pile) > 0:
                card = self.stock.pile[0]
                card.turn_face_up()
                card.visible = False
                card.place(self.waste)
            
            self.deck_passes_remaining += 1
            self.display_waste()

        self.save_game() 
        self.update()

    def check_foundation_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.name == top_card.suite.name
                and current_card.rank.value - top_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "Ace"

    def check_tableau_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.color != top_card.suite.color
                and top_card.rank.value - current_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "King"
            
    def check_and_save_high_score(self, game_won=False):
        score_updated = False
        
        if self.score > self.settings.best_score:
            self.settings.best_score = self.score
            score_updated = True
            
       
        if game_won and self.elapsed_time < self.settings.best_time:
            self.settings.best_time = self.elapsed_time
            score_updated = True
            
        if score_updated:
            with open("global_stats.json", "w") as f:
                json.dump({"best_score": self.settings.best_score, "best_time": self.settings.best_time}, f)

    def check_if_you_won(self):
        cards_num = 0
        for slot in self.foundation:
            cards_num += len(slot.pile)
        if cards_num == 52:
            self.is_running = False 
            
           
            self.check_and_save_high_score(game_won=True)
                
            if os.path.exists("savegame.json"):
                os.remove("savegame.json")
            return True
        return False
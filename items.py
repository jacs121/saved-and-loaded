import random
from typing import Dict, List
from enum import Enum
from messages import show_message

class Item:
    """Base class for all items."""
    def __init__(self, name: str, description: str, rarity: float = 1.0):
        self.name = name
        self.description = description
        self.rarity = rarity  # Higher values = more common
        
    def use(self, game_state: Dict) -> Dict:
        """Use the item and return modified game state."""
        return game_state
    
    def can_use(self, game_state: Dict) -> bool:
        """Check if the item can be used in the current state."""
        return True

class Syringe(Item):
    """Gives you +1 health permanently."""
    def __init__(self):
        super().__init__("Syringe", "Gives you +1 health", 0.6)
    
    def use(self, game_state: Dict) -> Dict:
        current_player = game_state.get('shooting_side', 'player')
        
        if current_player == 'player':
            game_state['player_lives'] = game_state.get('player_lives', 1) + 1
            show_message('item', "Syringe Used", 
                        "*INJECT* The medicine flows through your veins. +1 Life!")
        else:
            game_state['dealer_lives'] = game_state.get('dealer_lives', 1) + 1
            show_message('item', "Syringe Used", 
                        "The dealer injects the syringe. +1 Life!")
        
        return game_state

class BrokenSyringe(Item):
    """Gives you +1 health for one turn."""
    def __init__(self):
        super().__init__("Broken Syringe", "Gives you +1 health for one turn", 0.7)
    
    def use(self, game_state: Dict) -> Dict:
        current_player = game_state.get('shooting_side', 'player')
        
        # Initialize temp health tracking if not exists
        if 'temp_health' not in game_state:
            game_state['temp_health'] = {'player': 0, 'dealer': 0, 'turns_left': {'player': 0, 'dealer': 0}}
        
        game_state['temp_health'][current_player] = 1
        game_state['temp_health']['turns_left'][current_player] = 1
        
        show_message('item', "Broken Syringe Used", 
                    "*CRACK* The broken syringe gives temporary strength. +1 Health for this turn!")
        
        return game_state

class PoisonedBear(Item):
    """Deals -1 health for two turns."""
    def __init__(self):
        super().__init__("Poisoned Bear", "Deals -1 health for two turns", 0.4)
    
    def use(self, game_state: Dict) -> Dict:
        current_player = game_state.get('shooting_side', 'player')
        target = 'dealer' if current_player == 'player' else 'player'
        
        # Initialize poison tracking if not exists
        if 'poison_damage' not in game_state:
            game_state['poison_damage'] = {'player': 0, 'dealer': 0, 'turns_left': {'player': 0, 'dealer': 0}}
        
        game_state['poison_damage'][target] = 1
        game_state['poison_damage']['turns_left'][target] = 2
        
        show_message('item', "Poisoned Bear Used", 
                    f"*DRIP* Poison coats the bullet. The {target} will take damage for 2 turns!")
        
        return game_state

class EmptyChamber(Item):
    """Force a reload of the current bullets."""
    def __init__(self):
        super().__init__("Empty Chamber", "Force a reload of the current bullets", 0.5)
    
    def use(self, game_state: Dict) -> Dict:
        # Clear the current chamber
        game_state['chamber_list'] = []
        game_state['chamber_index'] = 0
        game_state['force_reload'] = True
        
        show_message('item', "Empty Chamber Used", 
                    "*CLICK* *CLICK* The chamber empties completely. Forced reload!")
        
        return game_state

class SniperBullets(Item):
    """Adds a -2 health bullet in a random place in the chamber."""
    def __init__(self):
        super().__init__("Sniper Bullets", "Adds a -2 health bullet in a random place", 0.3)
    
    def use(self, game_state: Dict) -> Dict:
        chamber_list = game_state.get('chamber_list', [])
        chamber_index = game_state.get('chamber_index', 0)
        
        if chamber_index < len(chamber_list):
            # Add sniper bullet at random position in remaining chamber
            remaining_positions = len(chamber_list) - chamber_index
            if remaining_positions > 0:
                insert_position = chamber_index + random.randint(0, remaining_positions)
                chamber_list.insert(insert_position, 'SNIPER')
                
                show_message('item', "Sniper Bullets Used", 
                            "*LOAD* A high-caliber sniper bullet has been added to the chamber!")
                
                game_state['chamber_list'] = chamber_list
            else:
                show_message('item', "Sniper Bullets Used", 
                            "Chamber is empty! Cannot add sniper bullet.")
        else:
            show_message('item', "Sniper Bullets Used", 
                        "Chamber is empty! Cannot add sniper bullet.")
        
        return game_state
    
    def can_use(self, game_state: Dict) -> bool:
        chamber_list = game_state.get('chamber_list', [])
        chamber_index = game_state.get('chamber_index', 0)
        return chamber_index < len(chamber_list)

class ShinyCoin(Item):
    """Flip a coin. If you win, you get +1 health; if you lose, +1 health for the opponent."""
    def __init__(self):
        super().__init__("Shiny Coin", "Coin flip: Win = +1 health, Lose = opponent +1 health", 0.6)
    
    def use(self, game_state: Dict) -> Dict:
        current_player = game_state.get('shooting_side', 'player')
        opponent = 'dealer' if current_player == 'player' else 'player'
        
        # Flip coin (50/50 chance)
        coin_result = random.choice([True, False])
        
        if coin_result:
            # Player wins
            game_state[f'{current_player}_lives'] = game_state.get(f'{current_player}_lives', 1) + 2
            show_message('item', "Shiny Coin Used", 
                        "*FLIP* *CLINK* HEADS! Lady luck smiles upon you. +1 Life!")
        else:
            # Player loses
            game_state[f'{opponent}_lives'] = game_state.get(f'{opponent}_lives', 1) + 2
            show_message('item', "Shiny Coin Used", 
                        f"*FLIP* *CLINK* TAILS! The coin betrays you. {opponent.title()} gains +1 Life!")
        
        return game_state

class BloodyCoin(Item):
    """Flip a coin. If you win, -1 health for the opponent; if you lose, -1 health for you."""
    def __init__(self):
        super().__init__("Bloody Coin", "Coin flip: Win = opponent -1 health, Lose = you -1 health", 0.4)
    
    def use(self, game_state: Dict) -> Dict:
        current_player = game_state.get('shooting_side', 'player')
        opponent = 'dealer' if current_player == 'player' else 'player'
        
        # Flip coin (50/50 chance)
        coin_result = random.choice([True, False])
        
        if coin_result:
            # Player wins - opponent takes damage
            current_lives = game_state.get(f'{opponent}_lives', 1)
            game_state[f'{opponent}_lives'] = max(0, current_lives - 2)
            show_message('item', "Bloody Coin Used", 
                        f"*FLIP* *SPLAT* HEADS! The bloody coin claims its victim. {opponent.title()} loses 1 Life!")
        else:
            # Player loses - they take damage
            current_lives = game_state.get(f'{current_player}_lives', 1)
            game_state[f'{current_player}_lives'] = max(0, current_lives - 2)
            show_message('item', "Bloody Coin Used", 
                        "*FLIP* *SPLAT* TAILS! The coin thirsts for YOUR blood. You lose 1 Life!")
        return game_state


class AVAILABLE_ITEMS(Enum):
    Syringe = Syringe
    BrokenSyringe = BrokenSyringe
    PoisonedBear = PoisonedBear
    EmptyChamber = EmptyChamber
    ShinyCoin = ShinyCoin
    BloodyCoin = BloodyCoin

def get_random_items(count: int = 2) -> List[Item]:
    """Get random items based on rarity weights."""
    items = []
    for _ in range(count):
        # Create weighted choices based on rarity
        weights = [item_class.value().rarity for item_class in list(AVAILABLE_ITEMS)]
        item_class = random.choices(list(AVAILABLE_ITEMS), weights=weights)[0].value()
        items.append(item_class)

    return items

def show_items(items: List[Item]) -> None:
    """Display available items to the player."""
    if not items:
        show_message('item', "Items", "No items available.")
        return
    
    item_text = "Available Items:\n\n"
    for i, item in enumerate(items, 1):
        item_text += f"{i}. {item.name}\n   {item.description}\n\n"
    
    show_message('item', "Your Items", item_text.strip())

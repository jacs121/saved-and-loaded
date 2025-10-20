import os
import prompt_toolkit.shortcuts.dialogs as dialogs
import sys
from typing import Dict, List
from style import STYLES
from manager import *
from application import *
from messages import TUTORIAL, TUTORIAL_ITEMS, MESSAGES, show_stats
from items import AVAILABLE_ITEMS, get_random_items, Item, show_items

def end_game(player_name: str, game_state: dict[str]) -> bool:
    """Ask the player if they want to play again."""
    if game_state["player_lives"] <= 0:
        show_message('game_over', "Save-And-Loaded: Game Over", random.choice(MESSAGES["player_dies_by_poison" if game_state['poison_damage']['turns_left']["player"] > 0 else "game_over"]))
    if game_state["dealer_lives"] <= 0:
        show_message('play_again', "Save-And-Loaded: You Won", random.choice(MESSAGES["dealer_dies_by_poison" if game_state['poison_damage']['turns_left']["dealer"] > 0 else "player_wins"]))

    restart =  dialogs.yes_no_dialog(
        style=STYLES['play_again'],
        title="Saved-And-Loaded: restart?",
        text=random.choice(MESSAGES['play_again_prompt']).format(name=player_name.upper()),
        yes_text="Play Again",
        no_text="Quit",
    )
    restart.cursor = CursorShape.UNDERLINE
    restart = restart.run()
    
    if restart:
        restart_game()
    sys.exit()

def restart_game():
    """Restart the game."""
    os.execv(sys.executable, [sys.executable] + sys.argv)

def use_item_menu(items: List[Item], game_state: Dict) -> Tuple[List[Item], Dict]:
    """Show item usage menu and handle item usage."""
    if not items:
        show_message('item', "Items", "No items can be used right now.")
        return items, game_state
    
    # Filter usable items
    usable_items = [item for item in items if item.can_use(game_state)]
    
    if not usable_items:
        show_message('item', "Items", "No items can be used right now.")
        return items, game_state
    
    # Create button list
    buttons = [(f"{item.name}", i) for i, item in enumerate(usable_items)]
    buttons.append(("SHOOT", "shoot"))
    
    choice = fixed_button_dialog(
        style=STYLES['item'],
        title="Saved-And-Loaded: Use an Item?",
        text="Choose an item to use before shooting:",
        buttons=buttons
    ).run()
    
    if choice == "shoot":
        return items, game_state
    
    # Use the selected item
    if isinstance(choice, int) and 0 <= choice < len(usable_items):
        selected_item = usable_items[choice]
        game_state = selected_item.use(game_state)
        if type(selected_item) == AVAILABLE_ITEMS.PoisonedBear:
            random.choice(MESSAGES["dealer_used_"+str(type(selected_item))])
        items.remove(selected_item)  # Remove used item
    
    return items, game_state

def main():
    """Main game function."""
    try:
        # Show start options
        while True:
            start_options = fixed_button_dialog(
                style=STYLES['default'],
                title="Saved-And-Loaded",
                buttons=[
                    ("START", "S"),
                    ("TUTORIAL", "T"),
                    ("QUIT", "Q")
                ]
            ).run()

            if start_options == "Q":
                sys.exit()
            elif start_options == "T":
                show_message('default', "Saved-And-Loaded: (1) how to play", TUTORIAL)
                show_message('default', "Saved-And-Loaded: (2) available items", TUTORIAL_ITEMS)
            else:
                break

        player_name = uppercaseDialogInput(
            title="Saved-And-Loaded: write your name",
            text=random.choice(MESSAGES['name_prompt']),
            style=STYLES["default"]
        )

        # Get chamber count
        chambers = dialogs.input_dialog(
            style=STYLES["default"],
            title="Saved-And-Loaded: set chamber amount (3-16)",
            text=random.choice(MESSAGES['chamber_prompt']),
            validator=IntegerValidator(3, 16)
        )
        chambers.cursor = CursorShape.UNDERLINE
        chambers = int(chambers.run())

        # Get lives count
        player_lives = dealer_lives = dialogs.input_dialog(
            style=STYLES["default"],
            title="Saved-And-Loaded: set amount of lives (1-16)",
            text=random.choice(MESSAGES['lives_prompt']),
            validator=IntegerValidator(1, 16)
        )
        player_lives.cursor = CursorShape.UNDERLINE
        player_lives = int(player_lives.run())

        shooting_side = "player"
        player_items: list[Item] = []
        dealer_items: list[Item] = []
        
        # Game state for item effects
        game_state = {
            'player_lives': player_lives,
            'dealer_lives': dealer_lives,
            'shooting_side': shooting_side,
            'chamber_list': [],
            'chamber_index': 0,
            'double_damage': False,
            'extra_turn': False,
        }

        # Main game loop
        while True:
            # Create and shuffle chamber list (or reload if forced)
            if game_state.get('force_reload', False):
                game_state['force_reload'] = False
                show_message('default', "Force Reload", "Chamber forced to reload!")
            
            live_count = max(1, chambers // 2 + random.randint(-1, 2))
            live_count = min(live_count, chambers)  # Ensure we don't exceed chamber count
            chamber_list = [True] * live_count + [False] * (chambers - live_count)
            random.shuffle(chamber_list)
            
            # Update game state
            game_state['chamber_list'] = chamber_list
            game_state['chamber_index'] = 0
            
            show_bullets_loaded(chamber_list)
            chamber_index = 0
            
            while chamber_index < len(chamber_list):
                # Process poison damage and temporary health effects
                game_state = process_poison_damage(game_state)
                game_state = process_temp_health(game_state)
                
                # Update lives from poison damage
                player_lives = game_state['player_lives']
                dealer_lives = game_state['dealer_lives']
                
                # Check for game over due to poison
                if player_lives <= 0 or dealer_lives <= 0:
                    end_game(player_name, game_state)
                
                bullet_in_chamber = chamber_list[chamber_index]

                # Update game state
                game_state['shooting_side'] = shooting_side
                game_state['chamber_index'] = chamber_index
                game_state['player_lives'] = player_lives
                game_state['dealer_lives'] = dealer_lives
                
                if shooting_side == "player":
                    # Show and use player items
                    if player_items:
                        show_items(player_items)
                        player_items, game_state = use_item_menu(player_items, game_state)
                        
                        # Update lives from game state (in case cigarette was used)
                        player_lives = game_state['player_lives']
                        dealer_lives = game_state['dealer_lives']
                        
                        # Update chamber list (in case beer was used)
                        chamber_list = game_state['chamber_list']
                        chamber_index = game_state['chamber_index']
                        
                        # Check if chamber is now empty or force reload triggered
                        if chamber_index >= len(chamber_list) or game_state.get('force_reload', False):
                            break
                        
                        bullet_in_chamber = chamber_list[chamber_index]
                    
                    # Player's turn
                    shooting = fixed_button_dialog(
                        style=STYLES['default'],
                        title="Saved-And-Loaded: your turn",
                        text=random.choice(MESSAGES['player_turn']),
                        buttons=[("Shoot Yourself", "player"), ("Shoot Dealer", "dealer"), ("Quit", "quit")]
                    ).run()
                    
                    if shooting == "player":
                        # Player shoots themselves
                        show_message('default', "Saved-And-Loaded: your turn", 
                                    "action: (SHOOT YOURSELF)\n" + random.choice(MESSAGES['shoot_self']))
                        
                        player_lives, game_over = handle_player_shot_self(bullet_in_chamber, player_lives, game_state)
                        if game_over:
                            end_game(player_name, game_state)
                    else:
                        # Player shoots dealer
                        show_message('default', "Saved-And-Loaded: your turn", 
                                    "action: (SHOOT THE DEALER)\n" + random.choice(MESSAGES['shoot_dealer']))
                        
                        dealer_lives, game_over = handle_player_shot_dealer(bullet_in_chamber, dealer_lives, game_state)
                        if game_over:
                            end_game(player_name, game_state)
                else:
                    # Dealer uses items (simplified AI)
                    if dealer_items:
                        usable_dealer_items = [item for item in dealer_items if item.can_use(game_state)]
                        if usable_dealer_items and random.random() < 0.6:  # 60% chance to use item
                            selected_item = random.choice(usable_dealer_items)
                            game_state = selected_item.use(game_state)
                            dealer_items.remove(selected_item)
                            
                            # Update from game state
                            player_lives = game_state['player_lives']
                            dealer_lives = game_state['dealer_lives']
                            chamber_list = game_state['chamber_list']
                            chamber_index = game_state['chamber_index']
                            
                            # Check if chamber is now empty or force reload triggered
                            if chamber_index >= len(chamber_list) or game_state.get('force_reload', False):
                                break
                            
                            bullet_in_chamber = chamber_list[chamber_index]
                    
                    # Dealer's turn
                    show_message('default', "Saved-And-Loaded: dealer's turn", 
                                random.choice(MESSAGES['dealer_turn']))
                    
                    # Calculate dealer strategy based on bullet types
                    live_count = sum(1 for bullet in chamber_list if bullet is True)
                    blank_count = sum(1 for bullet in chamber_list if bullet is False)
                    sniper_count = sum(2 for bullet in chamber_list if bullet == 'SNIPER')
                    
                    # Dealer AI: more likely to shoot opponent if more dangerous bullets (live/sniper)
                    dangerous_bullets = live_count + sniper_count
                    total_bullets = len(chamber_list)
                    
                    shooting = weighted_choice({
                        "player": (dangerous_bullets / total_bullets if total_bullets > 0 else 0) + random.random() * 0.5,
                        "dealer": (blank_count / total_bullets if total_bullets > 0 else 0) + random.random() * 0.5
                    })
                    
                    if shooting == "dealer":
                        # Dealer shoots themselves
                        show_message('default', "Saved-And-Loaded: dealer's turn", 
                                    "action: (SHOOTS HIMSELF)\n" + random.choice(MESSAGES['dealer_shoot_self']))
                        
                        dealer_lives, game_over = handle_dealer_shot_self(bullet_in_chamber, dealer_lives, game_state)
                        if game_over:
                            if end_game(player_name, "player"):
                                restart_game()
                            sys.exit()
                    else:
                        # Dealer shoots player
                        show_message('default', "Saved-And-Loaded: dealer's turn", 
                                    "action: (SHOOTS YOU)\n" + random.choice(MESSAGES['dealer_shoots_player']))
                        
                        player_lives, game_over = handle_dealer_shot_player(bullet_in_chamber, player_lives, game_state)
                        if game_over:
                            if end_game(player_name, "dealer"):
                                restart_game()
                            sys.exit()
                
                # Show stats after each turn
                show_stats("Saved-And-Loaded: health left", player_lives, dealer_lives, player_name)
                game_state["dealer_lives"] = dealer_lives
                game_state["player_lives"] = player_lives
            
                bullet_causes_switch = (bullet_in_chamber is True or bullet_in_chamber == 'SNIPER')
                if shooting_side != shooting or bullet_causes_switch:
                    shooting_side = "dealer" if shooting_side == "player" else "player"
            
                chamber_index += 1

            # Reloading message after chamber is empty
            show_message('default', "Saved-And-Loaded: " + ("your" if shooting_side == "player" else "dealers") + " turn", 
                        "action: (RELOADING)\n" + random.choice(MESSAGES['reloading']))
            
            # Give random items to both players
            new_player_items = get_random_items(random.randint(1, 3))
            new_dealer_items = get_random_items(random.randint(1, 3))
            
            player_items.extend(new_player_items)
            dealer_items.extend(new_dealer_items)
            
            if new_player_items:
                item_names = [item.name for item in new_player_items]
                show_message('item', "Saved-And-Loaded: you found an item", 
                    f"You found: {', '.join(item_names)}\n> {random.choice(MESSAGES["player_found_item"])}"
                )

            if new_dealer_items:
                item_names = [item.name for item in new_player_items]
                show_message('item', "Saved-And-Loaded: the dealer found an item",
                    random.choice(MESSAGES["dealer_found_item"])
                )
            

    except Exception as e:
        show_message('default', "Error", f"An error occurred: {str(e)}\nARGUMENTS: {e.args}")
        if dialogs.yes_no_dialog(
            style=STYLES['default'],
            title="Error",
            text="Would you like to restart the game?"
        ).run():
            restart_game()

if __name__ == "__main__":
    main()

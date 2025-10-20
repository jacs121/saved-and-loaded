import random
from typing import List, Tuple, Dict, Union
from messages import MESSAGES, show_message

def weighted_choice(choices: Dict[str, float]) -> str:
    """Make a weighted random choice from a dictionary of choices with weights."""
    total = sum(choices.values())
    r = random.uniform(0, total)
    upto = 0
    for choice, weight in choices.items():
        if upto + weight >= r:
            return choice
        upto += weight
    return list(choices.keys())[0]  # Fallback

def show_bullets_loaded(chamber_list: List[Union[bool, str]]) -> None:
    """Show the bullets loaded in the chamber."""
    live_count = sum(1 for bullet in chamber_list if bullet is True)
    blank_count = sum(1 for bullet in chamber_list if bullet is False)
    sniper_count = sum(1 for bullet in chamber_list if bullet == 'SNIPER')
    
    if sniper_count > 0:
        show_message('stats', "Save-And-Loaded: bullets loaded",
            "   LIVE    |    BLANK   |   SNIPER   \n"
            f"{str(live_count).center(10)} | {str(blank_count).center(11)} | {str(sniper_count).center(11)}"
        )
    else:
        show_message('stats', "Save-And-Loaded: bullets loaded",
            "   LIVE    |    BLANK   \n"
            f"{str(live_count).center(10)} | {str(blank_count).center(11)}"
        )

def process_poison_damage(game_state: Dict) -> Dict:
    """Process poison damage over time effects."""
    if 'poison_damage' not in game_state:
        return game_state
    
    poison_data = game_state['poison_damage']
    
    for player in ['player', 'dealer']:
        if poison_data['turns_left'][player] > 0:
            # Apply poison damage
            damage = poison_data[player]
            current_lives = game_state.get(f'{player}_lives', 1)
            game_state[f'{player}_lives'] = max(0, current_lives - damage)
            
            show_message('item', f"Save-And-Loaded: Poisoned {player.title()}", 
                        f"*BURN* The poison courses through veins. -{damage} Life!")
            
            # Decrease turns remaining
            poison_data['turns_left'][player] -= 1
            
            # Clean up if poison effect is over
            if poison_data['turns_left'][player] <= 0:
                poison_data[player] = 0
    
    return game_state

def process_temp_health(game_state: Dict) -> Dict:
    """Process temporary health effects."""
    if 'temp_health' not in game_state:
        return game_state
    
    temp_data = game_state['temp_health']
    
    for player in ['player', 'dealer']:
        if temp_data['turns_left'][player] > 0:
            # Decrease turns remaining
            temp_data['turns_left'][player] -= 1
            
            # Remove temp health if expired
            if temp_data['turns_left'][player] <= 0:
                temp_data[player] = 0
                show_message('item', f"Temporary Health Expired - {player.title()}", 
                            "The temporary strength fades away.")
    
    return game_state

def get_effective_health(player: str, game_state: Dict) -> int:
    """Get effective health including temporary health."""
    base_health = game_state.get(f'{player}_lives', 1)
    temp_health = 0
    
    if 'temp_health' in game_state:
        temp_health = game_state['temp_health'].get(player, 0)
    
    return base_health + temp_health

def apply_item_effects(bullet_type: Union[bool, str], damage: int, game_state: Dict, target: str) -> Tuple[Union[bool, str], int]:
    """Apply item effects and determine final damage."""
    # Handle sniper bullets
    if bullet_type == 'SNIPER':
        damage = 2
        show_message('live', "SNIPER BULLET!", 
                    "**BANG** The sniper bullet tears through! DOUBLE DAMAGE!")
        return bullet_type, damage
    
    # For regular bullets, check if it's live
    is_live = bullet_type is True
    
    # Apply double damage effect (from saw - not implemented in new items but keeping for compatibility)
    if game_state.get('double_damage', False) and is_live:
        damage *= 2
        game_state['double_damage'] = False
        show_message('item', "Double Damage!", "The sawed-off barrel deals DOUBLE DAMAGE!")
    
    # Apply shield protection (not implemented in new items but keeping for compatibility)
    shield_key = f'{target}_shield'
    if is_live and game_state.get(shield_key, False):
        bullet_type = False  # Block the live bullet, make it act like blank
        game_state[shield_key] = False
        show_message('item', "Shield Protection!", "Your shield blocks the live bullet!")
    
    return bullet_type, damage

def handle_player_shot_self(bullet_type: Union[bool, str], player_lives: int, game_state: Dict) -> Tuple[int, bool]:
    """Handle when the player shoots themselves."""
    bullet_type, damage = apply_item_effects(bullet_type, 1, game_state, 'player')
    
    # Check effective health including temporary health
    effective_health = get_effective_health('player', game_state)
    
    if bullet_type is True or bullet_type == 'SNIPER':
        # Apply damage to effective health first
        if effective_health > damage:
            # Damage can be absorbed
            temp_health = game_state.get('temp_health', {}).get('player', 0)
            if temp_health > 0:
                # Reduce temp health first
                absorbed_by_temp = min(damage, temp_health)
                game_state.setdefault('temp_health', {})['player'] = temp_health - absorbed_by_temp
                remaining_damage = damage - absorbed_by_temp
                player_lives -= remaining_damage
            else:
                player_lives -= damage
        else:
            player_lives -= damage
        
        if player_lives <= 0:
            show_message('game_over', "Save-And-Loaded", random.choice(MESSAGES['game_over']))
            return player_lives, True
        else:
            bullet_name = "SNIPER" if bullet_type == 'SNIPER' else "LIVE"
            if damage > 1:
                show_message('live', "Save-And-Loaded: your turn", 
                            f"bullet: ({bullet_name} - {damage} DAMAGE)\n" + random.choice(MESSAGES['live_hit_player_from']))
            else:
                show_message('live', "Save-And-Loaded: your turn", 
                            f"bullet: ({bullet_name})\n" + random.choice(MESSAGES['live_hit_player_from']))
    else:
        show_message('blank', "Save-And-Loaded: your turn", 
                    "bullet: (BLANK)\n" + random.choice(MESSAGES['blank_player']))
    
    return player_lives, False

def handle_player_shot_dealer(bullet_type: Union[bool, str], dealer_lives: int, game_state: Dict) -> Tuple[int, bool]:
    """Handle when the player shoots the dealer."""
    bullet_type, damage = apply_item_effects(bullet_type, 1, game_state, 'dealer')
    
    # Check effective health including temporary health
    effective_health = get_effective_health('dealer', game_state)
    
    if bullet_type is True or bullet_type == 'SNIPER':
        # Apply damage to effective health first
        if effective_health > damage:
            # Damage can be absorbed
            temp_health = game_state.get('temp_health', {}).get('dealer', 0)
            if temp_health > 0:
                # Reduce temp health first
                absorbed_by_temp = min(damage, temp_health)
                game_state.setdefault('temp_health', {})['dealer'] = temp_health - absorbed_by_temp
                remaining_damage = damage - absorbed_by_temp
                dealer_lives -= remaining_damage
            else:
                dealer_lives -= damage
        else:
            dealer_lives -= damage
        
        if dealer_lives <= 0:
            show_message('play_again', "Save-And-Loaded", random.choice(MESSAGES['player_wins']))
            return dealer_lives, True
        else:
            bullet_name = "SNIPER" if bullet_type == 'SNIPER' else "LIVE"
            if damage > 1:
                show_message('live', "Save-And-Loaded: your turn", 
                            f"bullet: ({bullet_name} - {damage} DAMAGE)\n" + random.choice(MESSAGES['live_hit_dealer']))
            else:
                show_message('live', "Save-And-Loaded: your turn", 
                            f"bullet: ({bullet_name})\n" + random.choice(MESSAGES['live_hit_dealer']))
    else:
        show_message('blank', "Save-And-Loaded: your turn", 
                    "bullet: (BLANK)\n" + random.choice(MESSAGES['blank_dealer']))
    
    return dealer_lives, False

def handle_dealer_shot_self(bullet_type: Union[bool, str], dealer_lives: int, game_state: Dict) -> Tuple[int, bool]:
    """Handle when the dealer shoots themselves."""
    bullet_type, damage = apply_item_effects(bullet_type, 1, game_state, 'dealer')
    
    # Check effective health including temporary health
    effective_health = get_effective_health('dealer', game_state)
    
    if bullet_type is True or bullet_type == 'SNIPER':
        # Apply damage to effective health first
        if effective_health > damage:
            # Damage can be absorbed
            temp_health = game_state.get('temp_health', {}).get('dealer', 0)
            if temp_health > 0:
                # Reduce temp health first
                absorbed_by_temp = min(damage, temp_health)
                game_state.setdefault('temp_health', {})['dealer'] = temp_health - absorbed_by_temp
                remaining_damage = damage - absorbed_by_temp
                dealer_lives -= remaining_damage
            else:
                dealer_lives -= damage
        else:
            dealer_lives -= damage
        
        if dealer_lives <= 0:
            show_message('play_again', "Save-And-Loaded", random.choice(MESSAGES['player_wins']))
            return dealer_lives, True
        else:
            bullet_name = "SNIPER" if bullet_type == 'SNIPER' else "LIVE"
            if damage > 1:
                show_message('live', "Save-And-Loaded: dealer's turn", 
                            f"bullet: ({bullet_name} - {damage} DAMAGE)\n" + random.choice(MESSAGES['live_hit_dealer_self']))
            else:
                show_message('live', "Save-And-Loaded: dealer's turn", 
                            f"bullet: ({bullet_name})\n" + random.choice(MESSAGES['live_hit_dealer_self']))
    else:
        show_message('blank', "Save-And-Loaded: dealer's turn", 
                    "bullet: (BLANK)\n" + random.choice(MESSAGES['blank_dealer_self']))
    
    return dealer_lives, False

def handle_dealer_shot_player(bullet_type: Union[bool, str], player_lives: int, game_state: Dict) -> Tuple[int, bool]:
    """Handle when the dealer shoots the player."""
    bullet_type, damage = apply_item_effects(bullet_type, 1, game_state, 'player')
    
    # Check effective health including temporary health
    effective_health = get_effective_health('player', game_state)
    
    if bullet_type is True or bullet_type == 'SNIPER':
        # Apply damage to effective health first
        if effective_health > damage:
            # Damage can be absorbed
            temp_health = game_state.get('temp_health', {}).get('player', 0)
            if temp_health > 0:
                # Reduce temp health first
                absorbed_by_temp = min(damage, temp_health)
                game_state.setdefault('temp_health', {})['player'] = temp_health - absorbed_by_temp
                remaining_damage = damage - absorbed_by_temp
                player_lives -= remaining_damage
            else:
                player_lives -= damage
        else:
            player_lives -= damage
        
        if player_lives <= 0:
            show_message('game_over', "Save-And-Loaded", random.choice(MESSAGES['game_over']))
            return player_lives, True
        else:
            bullet_name = "SNIPER" if bullet_type == 'SNIPER' else "LIVE"
            if damage > 1:
                show_message('live', "Save-And-Loaded: dealer's turn", 
                            f"bullet: ({bullet_name} - {damage} DAMAGE)\n" + random.choice(MESSAGES['live_hit_player_dealer']))
            else:
                show_message('live', "Save-And-Loaded: dealer's turn", 
                            f"bullet: ({bullet_name})\n" + random.choice(MESSAGES['live_hit_player_dealer']))
    else:
        show_message('blank', "Save-And-Loaded: dealer's turn", 
                    "bullet: (BLANK)\n" + random.choice(MESSAGES['blank_player_dealer']))
    
    return player_lives, False

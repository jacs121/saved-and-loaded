import prompt_toolkit.shortcuts.dialogs as dialogs
from prompt_toolkit.cursor_shapes import CursorShape
from style import STYLES

TUTORIAL = """this game is all about strategy.
    Saved-And-Loaded: a gun with random amount of blank and live bullets (blank=empty bullet, live=dangers bullet) is passed through the player and the dealer,
    each time one of them can shoot their opponent or them selfs. if they shoot them self and it's blank they go again,
    otherwise if it's live the side that got shot losses one life and the cycle continues

    other game elements:
    - the title of the rectangle above contains the name and the state of the game
    - at the end of a turn the health of you and the dealer is shown
    - if the chamber is empty a new random chamber is loaded
    - the chamber is shown each time it's reloaded before it's randomized (including at the start)
"""

TUTORIAL_ITEMS = """
Between reloads, both players receive random items, Items can be used before shooting to gain advantages
- Items include:
    SYRINGE: Gives you +1 health permanently
    BROkEN SYRINGE: Gives you +1 health for one turn only
    POISON BEAR: Deals -1 health to opponent for two turns
    EMPTY CHAMBER: Forces a reload of the current bullets
    SNIPER BULLETS: Adds a -2 health bullet in a random place in the chamber
    SHINY COIN: Coin flip: Win = +1 health, Lose = opponent +1 health
    BLOODY COIN: Coin flip: Win and the opponent loses -1 health, Lose and you loses -1 health
"""

# Dialog message collections
MESSAGES = {
    'chamber_prompt': [
        "Choose your fate: how many chambers will whisper your death?",
        "More chambers, more chances... or is it more suffering?",
        "Spin the wheel of pain. How many bullets shall we hide?",
        "Ah, setting the stage. Pick your poison.",
        "Numbers, chambers, bullets. Choose wisely."
    ],
    'invalid_input': [
        "Tsk-tsk. That's not how the game works.",
        "The chamber rejects your foolish offering.",
        "The chamber rejects your foolish mistake.",
        "Even chaos has rules. Pick a valid number.",
        "If you can't count, you can't die properly.",
        "Numbers out of bounds... the gun refuses to play."
    ],
    'lives_prompt': [
        "How many chances would you like before fate stops pretending to be kind?",
        "Pick your lifelines. They won't save you, but they'll delay the inevitable.",
        "How many breaths do you think you're worth?",
        "Choose your endurance. Death is patient.",
        "Stack the odds however you want. The chamber doesn't care.",
        "Three? Five? Ten? Name your limit. I'll enjoy breaking it.",
        "Set your life count. I'll be counting down."
    ],
    'player_turn': [
        "Step up, little spark. The chamber is eager.",
        "Your turn. Make it count... or don't.",
        "The spotlight's on you. Squeeze or spin?",
        "Hope your hands aren't shaking. The gun hates cowards.",
        "Do you feel lucky... or just empty inside?"
    ],
    'shoot_self': [
        "Ah, turning inward. self-loathing meets bravery.",
        "Let's see if you hate yourself enough.",
        "You play with yourself-dangerously.",
        "Facing your own barrel. How poetic.",
        "Spin. Aim. Regret."
    ],
    'game_over': [
        "Lights out. No encore.",
        "And that's all for you. Beautiful mess.",
        "Boom. One less burden on this table.",
        "Dead. Like the rest. Like the rest will be.",
        "your shots where prosigually generated.",
        "and this is the end of this round, time for another?",
        "unfortunate, well bring in the next subject.",
        "more luck next time, oh wait...",
        "guess who's not getting rich tonight.",
        "here, I let you free from this mortal coil.",
        "Got anything more to say, {name}?",
        "You gave it all... and it took it."
    ],
    'play_again_prompt': [
        "Reset the suffering. Next round begins.",
        "Clean the blood. Spin again.",
        "A new chance to die spectacularly.",
        "Round two... or is it twenty?",
        "We begin again. Death's still watching.",
    ],
    'live_hit_player_from': [
        "Took a hit, but you're still twitching.",
        "One step closer to the void.",
        "The chamber clipped you. Still breathing?",
        "Life slips through your fingers... tick, tick.",
        "You bleed, but you're not done. Yet."
    ],
    'blank_player': [
        "Click. Nothing. Tension rises.",
        "Empty. The chamber teased you.",
        "The bullet hid... but it remembers.",
        "Safe... for now.",
        "The gun spared you. But it knows."
    ],
    'shoot_dealer': [
        "Let's see if fate's on your side... or just playing a trick.",
        "Even the chamber hesitates when you aim at me.",
        "So, we turn the tables now? Fine. Let's dance.",
        "A dangerous gamble... but aren't we all gamblers here?",
        "Shooting the host? How rude.",
        "I see you've chosen violence. Excellent.",
        "you want to see if gods bleed?",
        "The last one who tried that... isn't here to warn you."
    ],
    'player_wins': [
        "You survived... somehow.",
        "The chamber is empty, and you are not.",
        "Winner? Maybe. But the scars remain.",
        "You outlived your odds. Congratulations, monster.",
        "Victory tastes like gunpowder and guilt."
    ],
    'live_hit_dealer': [
        "You really pulled the trigger on me? rude.",
        "You shot me? I was starting to like you...",
        "Clever. Brutal. I respect that.",
        "you really thought that'd work out for you?",
        "Blood. Pain. Betrayal. Delicious.",
        "I bleed, but the game goes on.",
        "you'll regret that. I never die quietly.",
        "So that's how it is, then?",
        "Lucky shot. Let's see if it stays that way.",
        "finally, some fun."
    ],
    'blank_dealer': [
        "Click. Did you really think it'd be that easy?",
        "Hah! You missed - but not because you aimed wrong.",
        "Empty. Just like your chances.",
        "The gun loves me. Try again.",
        "You pulled the trigger... and fate laughed.",
        "That was cute. Now sit back down.",
        "The chamber spared me. You won't be so lucky.",
        "Still here. Still smiling.",
        "Boom? No. Just disappointment.",
        "Even your rebellion misfires."
    ],
    'dealer_turn': [
        "Let's see... pain or mercy?",
        "who deserves the barrel more today?",
        "Choices, choices. I do love a dilemma.",
        "Who dies next... myself, or my little guest?",
        "The chamber whispers. I listen.",
        "Should I end you... or tempt fate myself?",
        "Flip a coin? Or follow the scent of fear?",
        "I wonder what hurts more, pulling the trigger or waiting for it?",
        "The odds shift like shadows. Who will bleed?",
        "Eenie... meenie... miney...",
        "My turn to tempt god.",
        "Death likes surprises, and so do I.",
        "The trigger itches... So who would it be"
    ],
    'dealer_shoot_self': [
        "I'll take this one. Pain sharpens the senses.",
        "Let's see if I'm still charming.",
        "The chamber and I go way back.",
        "No fun unless I bleed too, right?",
        "Let me taste the odds, I'm igor.",
        "My turn to dance with death.",
        "Either I win... or it gets interesting."
    ],
    'live_hit_dealer_self': [
        "Agh! Beautiful pain.",
        "ha! how I've waited for this.",
        "well, I deserved that.",
        "Even I'm not immune to fate's bite... or am I.",
        "Mmm... pain keeps me awake.",
        "and the barrel bites back. Good.",
        "See? I play fair, I also bleed.",
        "Ouch... that one stung. Delicious.",
        "Even the I gambles with death.",
        "And there it is... sweet old consequence."
    ],
    'blank_dealer_self': [
        "Click. Still breathing.",
        "The gun knows better then to hurt ME.",
        "Not today.",
        "still my turn, I guess.",
        "The chamber winked at me, cute.",
        "Luck favors the fearless, so what are you.",
        "Empty. How disappointing.",
        "Empty. How fortunate.",
        "No bang... but plenty of suspense.",
        "No bang... and no boom...",
        "I'm still here. That's what matters.",
        "It flinched... I didn't.",
        "see, the gun and I are old friends.",
        "Saved by chance. Or maybe fate wants more blood.",
        "The chamber sighed... and let's me go.",
        "I live... and so do my games."
    ],
    'dealer_shoots_player': [
        "I've made up my mind. Let's see what's inside that skull of yours.",
        "You talk too much. Let's fix that.",
        "You looked the wrong way. Look at the barrel.",
        "I chose you. The chamber agreed.",
        "Smile! You're the lucky target.",
        "Don't worry. It'll be over fast and loud.",
        "I flipped a coin. You lost.",
        "It's nothing personal. Actually, it kind of is."
    ],
    'live_hit_player_dealer': [
        "Boom. Right where it hurts.",
        "Ooh, that one made a mess.",
        "The gun chose you. Be honored.",
        "Oops. Did that hurt?",
        "I never miss when it matters, trust me.",
        "Bang. The game shall end soon.",
        "Pain suits you nicely.",
        "You looked better with a whole right there.",
        "No mercy for you today.",
        "I warned you. wear those consequence correctly.",
        "A direct hit. And you looked so hopeful.",
        "You're not dying, just losing once more.",
        "The chamber was hungry. feed it until it's satisfied.",
        "You screamed better than the last one.",
        "Good night, little star.",
        "Good night, little one."
    ],
    'blank_player_dealer': [
        "Click. Lucky little shit.",
        "smart cookie...",
        "Tsk. I really thought that was the one.",
        "Guess the gun likes you... for now.",
        "Not yet. But you feel it",
        "I was hoping for more blood.",
        "The chamber spared you... barre-ly.",
        "Another chance. Don't waste it.",
        "The bullet blinked. You should thank it.",
        "The bullet blinked. But you shouldn't.",
        "Missed? don't waste your shot kid",
        "Another chance. You better savor it.",
        "I could've sworn that... oh well.",
        "I almost felt sorry for you. Almost.",
        "I pulled. It clicked. But no bullet.",
        "hah, blank just like your life."
    ],
    'reloading': [
        "No more shots... how tragic. Let's stir the pot again.",
        "The drum's empty. Time to wind it up once more.",
        "Click. Click. Click. Boring. Let's start a louder song.",
        "Fate took a nap - let's wake her up.",
        "No more bullets? Don't worry. I'm always ready to reload.",
        "We ran out of luck. Let's refill the chamber with regret.",
        "The gun's thirsty again. Shall we oblige?"
    ],
    'name_prompt': [
        "and you are?",
        "another one bits the dust I see.",
        "don't worry, it will end soon.",
        "so just sign here, here, and here.",
        "more victims for today.",
        "well, well, what mess are you in to be here?",
    ],
    'player_found_item': [
        "The barrel whispers gifts.",
        "Fate offers you tools. Use them wisely.",
        "The chamber rewards the bold again.",
        "Something glints in the darkness I see.",
        "now, now, be carful with those.",
        "don't hoard it, that is no fun."
    ],
    'dealer_found_item': [
        "woo, this will hurt.",
        "don't worry I'll be quicker now.",
        "nicely done fate.",
        "look at that, lucky me."
    ],
    'poison_damaged_player': [
        "Lets see when will the venom take its toll.",
        "Pain spreads like wildfire you know.",
        "The poison claims another piece.",
        "can you see how many fingers am I holding? good.",
        "don't worry I can wait for your death.",
    ],
    'poison_damaged_dealer': [
        "Lets see when will the venom take its toll on me.",
        "Pain spreads like wildfire",
        "The poison will claims another piece.",
    ],
    'temp_health_gained': [
        "the more goes up, the more it falls.",
        "A fleeting boost of vitality... but not for long.",
        "The enhancement won't last long enough for you.",
        "that syringe is as dirty as you.",
        "running will get you nowhere.",
    ],
    'sniper_added': [
        "High-caliber has joined the game, go say hi won't you.",
        "The sniper's gift: precision and pain.",
        "this bullet is meant to kill professionals, but it will do fine for you.",
        "aha, Death's favorite ammunition."
        "oh I love this one."
        "now it gets more interesting."
    ],
    'dealer_dies_by_poison': [
        "poison will not be the death of me",
        "I'll be waiting...",
        "next time spare the drinks.",
        "poison hah, lame.",
    ],
    'player_dies_by_poison': [
        "3.. 2.. 1.. and.. DARK",
        "it's passed your bed time, NOW SLEEP",
        "poison is still a lame way to...",
        "sleepy head going to die soon",
        "at least it's not a bullet"
    ],
    # Dealer item usage messages
    'dealer_used_syringe': [
        "I do love a good pick-me-up. Care for some? No? Your loss.",
        "Fresh supplies. The night is young, and so am I.",
        "A little boost. Wouldn't want to tire before the real fun begins.",
        "Medicine tastes better when it's not yours.",
    ],
    'dealer_used_broken_syringe': [
        "Desperate times call for desperate measures.",
        "This one's on borrowed time. So are you.",
        "Half a dose is better than none... right?",
        "I'll take my chances. Will you?",
    ],
    'dealer_used_poisoned_bear': [
        "A gift from my friends. Consider it... slow torture.",
        "The venom's already spreading. Can you feel it?",
        "I do so love watching things deteriorate.",
        "This won't kill you immediately. I promise.",
        "This won't be painless. I promise you.",
    ],
    'dealer_used_empty_chamber': [
        "Boring. Let's shuffle things around.",
        "This game needs more chaos, don't you think?",
        "A reset. Just when things were getting interesting.",
        "The chamber breathes again. and sadly So do I.",
    ],
    'dealer_used_sniper_bullets': [
        "This one's special. Care to say goodbye to your insides?",
        "Sniper rounds for special occasions. And this one is.",
        "I do so enjoy the sound of distant pain.",
        "Think fast little one... or don't.",
    ],
    'dealer_used_shiny_coin': [
        "Heads I win, tails you lose. Statistically speaking.",
        "A gamble? With me? How delightfully foolish.",
        "Let's see what fate thinks of your face.",
        "The coin knows who's leaving in a box.",
    ],
    'dealer_used_bloody_coin': [
        "Blood for the blood god! ...I mean, the coin.",
        "Heads you die, tails you die. Try not to think about it.",
        "The coin thirsts. And so do I.",
        "May the worse player win... Or lose.",
    ],
    # coin use
    'dealer_win_shiny_coin': [
        "Ooh... lucky me.",
        "And I'm not sharing.",
        "Well, well, well, look what I found.",
    ],
    'player_win_shiny_coin': [
        "Wait, you got it? let me take care of that mistake.",
        "That won't help you you know.",
        "Lady luck smiles upon you, that would be the first and last time."
        "good, one extra chance to kill you."
    ],
    'dealer_win_bloody_coin': [
        "Don't worry you shouldn't feel a thing",
        "lets see how you act without this one.",
        "oops, good your life.",
    ],
    'player_win_bloody_coin': [
        "evening the odds, are we?",
        "oh now Im gonna kill you.",
        "it's sad, you think thats gonna help you."
        "you f***!"
    ]
}

def show_message(style_name: str, title: str, text: str) -> None:
    """Show a message dialog with the specified style."""
    msg = dialogs.message_dialog(style=STYLES[style_name], title=title, text=text)
    msg.cursor = CursorShape.UNDERLINE
    msg = msg.run()


def show_stats(title: str, player_lives: int, dealer_lives: int, player_name: str) -> None:
    """Show the current game stats."""
    show_message('stats', title,
        f"   {player_name}    |    DEALER   \n"
        f"{str(player_lives).center(6+len(player_name))} | {str(dealer_lives).center(12)}"
    )
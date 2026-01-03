# Saved-And-Loaded

An enhanced Russian Roulette-style game with over 260 different dialog lines featuring unique strategic items that add depth and unpredictability to the classic gameplay.

## Unique Item System

### How Items Work

- **Random Distribution**: Between chamber reloads, both you and the dealer receive 1-3 random items
- **Strategic Usage**: Before each shooting decision, you can choose to use an item for tactical advantage
- **One-Time Use**: Items are consumed when used and cannot be reused
- **AI Opposition**: The dealer will also use items strategically against you
- **Other**: Temporary effects, damage over time, coin flips, and chamber manipulation

### Available Items

#### **Syringe** (Common - 0.6 rarity)

- **Effect**: Gives you +1 health permanently
- **Strategy**: Essential healing item for survival and recovery
- **Best Used**: When low on health or to build a health buffer

#### **Broken Syringe** (Common - 0.7 rarity)

- **Effect**: Gives you +1 health for one turn only
- **Strategy**: Temporary protection for risky plays, timing is crucial
- **Best Used**: Right before taking a dangerous shot at yourself

#### **Poison Bear** (Rare - 0.4 rarity)

- **Effect**: Deals -1 health to opponent for two turns
- **Strategy**: Delayed damage that can't be easily countered
- **Best Used**: Early in rounds to apply sustained pressure

#### **Empty Chamber** (Uncommon - 0.5 rarity)

- **Effect**: Forces a reload of the current bullets
- **Strategy**: Reset unfavorable chamber compositions instantly
- **Best Used**: When chamber has too many dangerous bullets

#### **Sniper Bullets** (Very Rare - 0.3 rarity)

- **Effect**: Adds a -2 health bullet in a random place in the chamber
- **Strategy**: Devastating damage potential, but affects both players
- **Best Used**: When you have health advantage and want high-risk/high-reward

#### **Shiny Coin** (Common - 0.6 rarity)

- **Effect**: Coin flip: Win = +1 health, Lose = opponent +1 health
- **Strategy**: Low-risk gamble with potentially beneficial outcomes
- **Best Used**: When you're ahead or need a small advantage

#### **Bloody Coin** (Rare - 0.4 rarity)

- **Effect**: Coin flip: Win and the opponent loses -1 health, Lose and you loses -1 health
- **Strategy**: High-risk gamble that can instantly change the game
- **Best Used**: In desperate situations or when you have health advantage

## Item Mechanics

### Temporary Health

- **Broken Syringe** provides temporary health that lasts for one turn
- Temporary health absorbs damage before real health
- Expires after one turn regardless of whether it's used

### Damage Over Time

- **Poison Tip** applies poison that deals damage for two consecutive turns
- Poison damage is applied at the start of each turn
- Cannot be prevented or healed, only waited out

### Special Bullets

- **Sniper Bullets** add high-damage bullets to the chamber
- Sniper bullets deal 2 damage instead of 1
- Chamber display shows SNIPER bullets separately from LIVE/BLANK

### Coin Mechanics

- **Shiny Coin** and **Bloody Coin** use true 50/50 random chance
- Results are immediate and cannot be influenced
- Adds pure chance element to strategic gameplay

## Game Files

### Project Files

- `main.py` - Original game implementation
- `manager.py` - Original game logic
- `application.py` - UI components
- `messages.py` - Original game messages
- `style.py` - Original styling
- `items.py` - Complete item system implementation
- `run.bat` - Opening the game in the console via batch

## How to Play

1. **Run via python/batch**:

   ```yaml
   python:
       py main.py
   batch:
       run.bat
   ```
2. **Setup**: write your name, then Choose chamber count and starting lives as usual
3. **Item Phase**:

   - After each reload, you'll receive random items
   - Before shooting, you can view and use your items
   - Choose "Skip Items" if you don't want to use any
4. **New Strategic Considerations**:

   - **Timing Items**: Broken Syringe and coin flips require careful timing
   - **Risk Management**: Bloody Coin and Sniper Bullets add high-risk elements
   - **Resource Planning**: Poison Tip and healing items for sustained gameplay
   - **Chamber Control**: Empty Chamber for tactical resets

## Advanced Strategies

### Health Management

- **Syringe**: Permanent healing for long-term survival
- **Broken Syringe**: Tactical temporary health for risky moves
- **Poison Tip**: Sustained pressure on opponent

### Risk/Reward Plays

- **Bloody Coin**: High-stakes gambling when desperate
- **Sniper Bullets**: Add devastating damage but dangerous for both
- **Shiny Coin**: Safe gambles for small advantages

### Chamber Manipulation

- **Empty Chamber**: Reset bad situations instantly
- **Sniper Bullets**: Add chaos and high damage potential

### Timing Strategies

1. **Early Game**: Use Poison Tip for sustained damage
2. **Mid Game**: Manipulate chamber with Empty Chamber
3. **Late Game**: Desperate coin flips and healing items

## Item Combinations

### The Poison Strategy

1. **Poison Tip** -> Apply early pressure
2. **Syringe** -> Heal while opponent takes damage
3. **Empty Chamber** -> Reset when chamber gets dangerous

### The Gambler's Edge

1. **Shiny Coin** -> Safe beneficial gamble
2. **Broken Syringe** -> Temporary protection
3. **Bloody Coin** -> High-stakes finish

### The Chaos Creator

1. **Sniper Bullets** -> Add high damage to chamber
2. **Empty Chamber** -> Reset if it backfires
3. **Syringe** -> Heal from potential sniper damage

## Common Mistakes

### Don't Do This

- Using Broken Syringe too early (wasted temporary health)
- Using Bloody Coin when you're already losing
- Adding Sniper Bullets when you're low on health
- Wasting Empty Chamber on favorable chambers

### Do This Instead

- Time Broken Syringe right before risky shots
- Use Bloody Coin when you have health advantage
- Save healing items for when you actually need them
- Use Empty Chamber strategically to avoid bad situations

## Technical Notes

- Items persist between rounds until used
- Poison damage and temporary health are tracked per player
- Sniper bullets are mixed randomly into chamber positions
- Coin flips use true randomness (50/50 chance)
- The dealer uses simplified AI for item usage

Enjoy the strategic depth and unpredictability of Saved-And-Loaded!

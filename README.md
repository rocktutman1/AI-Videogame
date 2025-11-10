# AI-Videogame

An **entirely AI-generated terminal RPG game** written in Python.  
Repository: https://github.com/rocktutman1/AI-Videogame

---

## 🎮 Features

- Created using AI tools for story, assets & code generation.  
- Terminal-based game: minimal external dependencies (just Python).  
- Narrative & mechanics fused: AI-designed arenas, enemies, items.  
- Retro grid/ASCII aesthetic for fast iteration and cross-platform play.

---

## ⚙️ Installation & Running

Clone the repo and run from the project root:  

>git clone https://github.com/rocktutman1/AI-Videogame.git
>
>cd AI-Videogame
>
>python3 clash_rpg2_fixed.py

## 🕹️ Controls

| Key | Action | Description |
|-----|---------|--------------|
| **w a s d** | Move | Navigate across the grid during exploration or combat |
| **Enter / Space** | Confirm / Interact | Select menu options, confirm choices, continue dialogue |
| **i** | Inventory | Opens inventory view to use or inspect items |
| **q** | Quit | Exits the game safely to terminal |
| **Esc** | Back | Cancels current menu or closes inventory |
| **Any key** | Continue | Advances dialogue, cutscenes, or transitions between zones |

**Tip:** During combat, movement and attacks are turn-based.  
When prompted, use the arrow keys to position, then confirm with **Enter**.  

## 💰 Progression

| Feature | Description |
|----------|--------------|
| **Leveling** | Gain EXP after each battle; leveling up increases HP, STR, AGI, and MAG. |
| **Gold** | Earned from victories; used to buy potions, weapons, and armor in shops. |
| **Shops** | Appear in safe zones; sell healing items, elixirs, and equipment. |
| **Loot System** | Enemies and arenas drop random loot such as swords, armor, or tomes. |
| **Story Flags** | Key items like the *Crown Key* or *Treasure Map* unlock secret arenas and alternate endings. |
| **Equipment** | Equipping items boosts stats (ATK from swords, DEF from armor). |
| **Endgame Path** | Progress through all arenas to reach *Dragon’s Peak* and possibly the *Hidden Throne*. |

---

## 🧭 Areas & Encounters

| Arena | Description | Common Enemies | Notable Loot |
|--------|--------------|----------------|---------------|
| **Goblin Forest** | A tangled wood filled with ambushing creatures. | Spear Goblin, Ghost, Skeleton Army, Witch | Elixir Bottle, Royal Sword, Leather Armor |
| **Royal Arena** | Gladiatorial pits where elite warriors duel for glory. | Mini P.E.K.K.A., Mega Minion, Valkyrie, Prince, Bowler | Magic Tome, Crown Key, Iron Sword |
| **Dark Valley** | Trap-ridden valley haunted by bandits and spirits. | Bandit, Trap Spike, Lumberjack, Royal Ghost, Archer Queen | Elixir Flask, Treasure Map, Steel Armor |
| **Desert Arena** | Scorching dunes hosting deadly one-on-one battles. | P.E.K.K.A., Mega Knight, Prince, Dark Prince, Electro Wizard | Royal Blade, Steel Armor, Magic Tome |
| **Dragon’s Peak** | Fiery mountain lair of the Baby Dragon — a crucial choice awaits. | Baby Dragon | Magic Tome |
| **Hidden Throne** *(Secret)* | Sealed royal chamber of the final tyrant; unlocked with key items. | Archer Queen, Mega Knight, Golem | Magic Tome, Dragon Scale |

**Progression Tip:**  
Use healing and mana items strategically — later arenas drastically increase enemy power.  
Keys and maps can change your story path and unlock hidden endings.
## 🧠 Technical Notes

| Aspect | Details |
|---------|----------|
| **Language** | Python 3 (no external dependencies beyond `curses`) |
| **UI System** | Built using `curses` for grid rendering, menus, color, and animations |
| **Code Structure** | Organized into sections: Player class, UI handler, Combat logic, Enemy AI, and Arena data |
| **AI Behavior** | Smarter opponents that move using pathfinding (BFS), taunt, and use specials like *charge*, *phase*, *summon*, or *slam* |
| **Combat Mechanics** | Turn-based dice roll system with animations and stat-based damage |
| **Data Handling** | Arenas, enemies, and items stored as Python dictionaries for easy modification |
| **Compatibility** | Runs in any terminal that supports `curses` (Linux, macOS, or Windows via `windows-curses`) |
| **Performance** | Lightweight, runs entirely in the terminal — no assets or installs required |

---

## 🏁 Endings

| Ending | Condition | Description |
|---------|------------|--------------|
| **Dragon Slayer Ending** | Defeat the Adult Dragon at *Dragon’s Peak* | You slay the dragon and are remembered as the Dragonslayer. |
| **Mercy Ending** | Spare the Dragon during the final encounter | You show compassion, forging peace between humankind and dragons. |
| **Liberator Ending** | Unlock *Hidden Throne* using the Crown Key & Map; defeat final tyrant | You free the realm from tyranny and restore light to the kingdom. |

Each ending features a cinematic text sequence and custom epilogue animation.  
Your choices — combat outcomes, item usage, and mercy — determine the finale.

---

## 📄 License

**MIT License**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  
- The Software is provided “as is,” without warranty of any kind.

---

**© 2025 rocktutman1 — AI-Videogame Project**  
Created with assistance from AI-generated assets, code, and design tools.  
Fan content inspired by *Clash Royale* under its fair-use/fan-art guidelines.

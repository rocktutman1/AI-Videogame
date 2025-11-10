#!/usr/bin/env python3
"""
clash_rpg_curses.py
Clash Royale–inspired terminal RPG with curses UI, smarter AI, ASCII zone art, dice roll animation, and text animations.
Run: python3 clash_rpg_curses.py
No external libs required beyond curses (install windows-curses on Windows).
"""

import curses
import random
import time
import sys
from copy import deepcopy
from collections import deque

# -------------------- Game data (Clash-like names) --------------------
CLASSES = {
    "Knight": {"Strength": 10, "Agility": 6, "Magic": 2, "hp": 48, "passive": "armor"},
    "Wizard": {"Strength": 4, "Agility": 6, "Magic": 12, "hp": 34, "passive": "arcane"},
    "Bandit": {"Strength": 7, "Agility": 10, "Magic": 3, "hp": 36, "passive": "swift"},
}

AREAS = [
    {
        "id": "goblin_forest",
        "name": "Goblin Forest",
        "desc": "A tangled wood where Spear Goblins and Ghosts lurk.",
        "encounters": ["spear_goblin", "ghost", "skeleton_army", "witch"],
        "loot": ["elixir_bottle", "royal_sword", "leather_armor"],
        "art": [
            r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⢠⢤⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠔⠒⠒⠲⠎⠀⠀⢹⡃⢀⣀⠀⠑⠃⠀⠈⢀⠔⠒⢢⠀⠀⠀⡖⠉⠉⠉⠒⢤⡀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠚⠙⠒⠒⠒⠤⡎⠀⠀⠀⠀⢀⣠⣴⣦⠀⠈⠘⣦⠑⠢⡀⠀⢰⠁⠀⠀⠀⠑⠰⠋⠁⠀⠀⠀⠀⠀⠈⢦⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⢰⠃⠀⣀⣀⡠⣞⣉⡀⡜⡟⣷⢟⠟⡀⣀⡸⠀⡎⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⣻⠀⠀⠀⠀",
            r"⢰⠂⠀⠀⠀⠀⠀⠀⠀⣗⠀⠀⢀⣀⣀⣀⣀⣀⣓⡞⢽⡚⣑⣛⡇⢸⣷⠓⢻⣟⡿⠻⣝⢢⠀⢇⣀⡀⠀⠀⠀⢈⠗⠒⢶⣶⣶⡾⠋⠉⠀⠀⠀⠀⠀",
            r"⠈⠉⠀⠀⠀⠀⠀⢀⠀⠈⠒⠊⠻⣷⣿⣚⡽⠃⠉⠀⠀⠙⠿⣌⠳⣼⡇⠀⣸⣟⡑⢄⠘⢸⢀⣾⠾⠥⣀⠤⠖⠁⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⢀⠀⠀",
            r"⠀⠀⠀⢰⢆⠀⢀⠏⡇⠀⡀⠀⠀⠀⣿⠉⠀⠀⠀⠀⠀⠀⠀⠈⢧⣸⡇⢐⡟⠀⠙⢎⢣⣿⣾⡷⠊⠉⠙⠢⠀⠀⠀⠀⠀⢸⡇⢀⠀⠀⠀⠀⠈⠣⡀",
            r"⠀⠀⠀⠘⡌⢣⣸⠀⣧⢺⢃⡤⢶⠆⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣟⠋⢀⠔⣒⣚⡋⠉⣡⠔⠋⠉⢰⡤⣇⠀⠀⠀⠀⢸⡇⡇⠀⠀⠀⠀⠀⠀⠸",
            r"⠀⠀⠀⠀⠑⢄⢹⡆⠁⠛⣁⠔⠁⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⣿⢠⡷⠋⠁⠀⠈⣿⡇⠀⠀⠀⠈⡇⠉⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠑⣦⡔⠋⠁⠀⠀⠀⣿⠀⠀⢠⡀⢰⣼⡇⠀⡀⠀⠀⣿⠀⠁⠀⠀⠀⠀⣿⣷⠀⠀⠀⠀⡇⠀⠀⢴⣤⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⢰⣿⡇⠀⠀⠀⠀⠀⣿⡀⠀⢨⣧⡿⠋⠀⠘⠛⠀⠀⣿⠀⠀⢀⠀⠀⠀⣿⣿⠀⠀⠀⠀⢲⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⢸⡧⡄⠀⠹⣇⡆⠀⠀⠀⠀⠀⣿⠀⢰⣏⠀⣿⣸⣿⣿⠀⠀⠀⠀⣼⠀⠀⠰⠗⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⢸⡇⣷⣛⣦⣿⢀⠈⠑⠀⢠⡆⣿⠐⢠⣟⠁⢸⠸⣿⣿⢱⣤⢀⠀⣼⠀⠀⢀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⢀⠀⠀⠀⢸⡇⠘⠫⣟⡇⠊⣣⠘⠛⣾⡆⢿⠀⠙⣿⢀⣘⡃⣿⣿⡏⠉⠒⠂⡿⠀⠰⣾⡄⠀⢸⡟⣽⣀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠸⣿⡇⠀⠘⣾⠀⠀⢸⡇⢸⣇⡙⠣⠀⣹⣇⠀⠈⠧⢀⣀⣀⡏⣸⣿⣇⢹⣿⡇⢴⣴⣄⣀⡀⢰⣿⡇⠀⢸⣇⢿⡿⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠓⠁⠈⠻⢷⠾⠦⠤⠬⣅⣹⣿⣖⣶⣲⣈⡥⠤⠶⡖⠛⠒⠛⠁⠉⠛⠮⠐⢛⡓⠒⢛⠚⠒⠒⠒⠛⣚⣫⡼⠿⠿⣯⠛⠤⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⡉⠉⠁⠀⠀⠘⠓⠀⠀⠀⠀⠀⣀⣞⡿⡉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣶⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀"
        ],
    },
    {
        "id": "royal_arena",
        "name": "Royal Arena",
        "desc": "Gladiatorial pits with Mini P.E.K.K.A. and Mega Minions.",
        "encounters": ["mini_pekka", "mega_minion", "valkyrie", "prince", "bowler", "dark_prince"],
        "loot": ["magic_tome", "crown_key", "iron_sword"],
        "art": [
            r"⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⠀⢀⣴⣾⣿⣿⠿⢿⣿⣿⠏⠉⠉⠹⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⠀⣴⣿⠟⢻⣿⠁⠀⠀⣿⣿⠀⠀⠀⠀⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀",
            r"⢰⣿⡇⠀⢸⣿⣀⣤⣤⣿⣿⣶⣶⣶⣶⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀",
            r"⢸⣿⣧⣴⣿⣿⣿⡿⣿⣿⣿⡟⠉⠉⢻⣿⣿⣿⢿⣿⣿⣷⣦⣄⠀⠀",
            r"⢸⣿⣿⠟⢻⣿⠃⠀⠀⣿⣿⠀⠀⠀⠀⣿⣿⠀⠀⠘⣿⡟⠙⣿⣷⡀",
            r"⢸⣿⡇⠀⢸⣿⠀⠀⠀⣿⣿⣀⣀⣀⣀⣿⣿⠀⠀⠀⣿⡇⠀⢸⣿⡇",
            r"⢸⣿⣧⣴⣾⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣼⣿⡇",
            r"⢸⣿⡿⠋⢹⣿⠋⠀⠈⣿⣿⠃⠀⠀⠘⣿⣿⠁⠀⠙⣿⡏⠙⢿⣿⡇",
            r"⢸⣿⣧⣤⣼⣿⣤⣤⣤⣿⣿⣤⣤⣤⣤⣿⣿⣤⣤⣤⣿⣧⣤⣼⣿⡇",
            r"⠈⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠁"
        ],
    },
    {
        "id": "dark_valley",
        "name": "Dark Valley",
        "desc": "Trap-filled valley: Bandit leaders and ambushes roam.",
        "encounters": ["bandit", "trap_spike", "lumberjack", "royal_ghost", "archer_queen"],
        "loot": ["elixir_flask", "treasure_map", "steel_armor"],
        "art": [
            r"⣤⣿⠗⣯⠇⣰⠁⠀⠀⢀⡼⠉⡲⡀⠀⠈⢳⢦⣈⣷⣴⠏⠢⡈⢳⢸⠀⠀⡠⠋⢳⣄⡀⠀⢄⡄⠘⣿⡄⠀⠘⠀⣇⣿⡐⠁⡀⠀⠁⠀⠑⢬⣿⡉⡿⢄⣿⢇⡱⢝⡄⠈⣿⡇⠑",
            r"⢿⡟⠉⠘⢠⠃⢀⢁⢠⢊⠄⠊⢀⠍⠣⣤⢃⠀⠉⢻⣿⠀⠀⠐⠘⣿⣠⠞⠀⢠⠁⠹⡍⠢⢜⡙⡄⣿⡧⡀⠀⣿⣞⠸⢣⡀⠇⡄⠀⠀⠀⠀⣟⢸⣧⠊⢉⠺⣆⠀⢇⠁⣼⡇⠀",
            r"⠀⠋⢂⣰⣃⡴⡞⣩⠫⡥⠒⠈⠈⣇⢠⢋⠳⣤⡀⠀⣿⡄⠀⠀⠠⣿⠁⠎⢠⠁⡀⠀⠙⣦⡀⠱⠈⢻⡇⢱⣔⡿⢀⡷⡏⢿⣸⠀⠀⠀⢄⢀⢻⢡⣩⣶⠁⠀⠈⠑⢾⣾⢹⣿⡀",
            r"⠱⣤⠞⡏⡅⠱⡞⢀⠀⢡⡀⠇⠀⢉⣯⠃⢠⠁⠙⢳⣿⣷⡀⠀⢸⣿⠢⣰⠃⡄⡇⢄⠈⡘⡙⣦⡴⢸⣿⢎⣸⠁⠀⣟⢣⢏⣻⡄⠀⠀⠘⡼⢸⠟⠔⢈⢆⠀⠀⠀⠈⣿⠀⢿⡇",
            r"⠋⠈⢳⣧⠇⣸⠵⠀⠈⠢⠵⣀⣠⢯⠉⢦⡀⡸⠀⠀⠘⢿⣷⠡⣸⡿⡦⠊⢲⢇⠣⠀⠀⠱⠱⣹⠻⣦⣿⡼⠻⡑⡜⢸⠇⠈⡟⣇⠐⠀⠀⡁⣹⠎⠀⠀⡈⢦⠤⠐⠉⠺⡇⣿⣿",
            r"⠀⠀⠀⣿⣳⠃⠀⠣⡀⠐⣀⣸⢁⡟⡀⠠⢿⣀⠀⢠⠐⠌⢿⣷⣾⣳⡗⢤⣎⡌⢙⠦⡀⠀⠀⠙⢆⠘⣿⠇⠀⢳⡉⢾⠀⣸⠚⡘⣾⢆⡜⢀⣿⢀⠀⡠⠔⠉⣧⠀⠀⠀⣹⣇⣿",
            r"⠀⠀⠀⣿⠷⡀⠀⠀⠙⢄⡶⢹⢣⠻⡜⠀⠇⡹⡄⡀⠀⠰⣼⣿⡿⠉⢳⡂⠏⡨⠙⢲⠺⠦⣢⠀⢄⢳⣿⢄⡔⠃⢣⢸⡜⠙⠀⢰⢙⣿⣴⢻⣧⠷⠊⠀⣴⡠⠈⢣⡀⡼⠫⣿⡇",
            r"⠀⠀⠀⣿⡄⢱⠀⡈⢀⡞⢿⢇⣾⠿⡈⣦⣰⢁⢿⢦⣀⢖⠫⣿⣧⠃⣼⡜⣴⡀⡠⠁⠀⠀⠈⠧⡀⣞⣿⠏⢆⣠⡈⣿⢱⣄⠴⣫⣿⣻⣬⣾⠉⣱⠀⠀⠜⢆⠀⢀⡝⢧⡑⢻⣗",
            r"⡄⠀⢡⡟⡐⢇⢣⣸⡟⠀⢸⡼⡁⢀⣿⣾⣹⡎⣸⣮⢿⣌⡼⣿⣇⡸⠚⣇⠇⣱⡁⢀⠀⢀⡜⠠⠻⣿⣿⠺⡄⣿⠠⣸⢻⡽⢾⢿⠋⢫⣷⣿⢀⠎⡑⣀⠀⠈⣦⠛⢼⠀⠙⢻⣿",
            r"⠡⣠⢺⡇⡇⣠⠿⢧⠱⠀⢸⡡⢟⣡⢇⠓⣻⡷⠛⡇⠀⣿⢷⣿⡿⠁⣸⡏⠃⣀⢱⡊⢀⢺⡸⡅⠧⢺⣿⢦⣰⣄⣥⢾⣯⡽⢋⢻⣜⡀⡇⣿⠎⠀⠸⣜⣠⡾⡋⢣⡸⡡⣠⠂⢹",
            r"⣶⢹⣼⣷⡟⠁⡆⢻⣶⣣⣿⢣⡼⣥⠁⣆⠺⡇⠀⢃⢼⢧⡽⣿⣇⠔⢸⡝⣺⣼⠛⡱⢃⣜⠤⢚⡄⢸⣇⣽⣿⢿⡀⣹⣫⠏⢺⡾⠈⠳⣇⢿⡇⣘⢞⣿⡿⣦⡰⠘⠉⢷⣵⡴⠉",
            r"⠻⣿⣿⣿⡐⠉⠏⢢⣽⣛⣿⡊⠱⣎⠶⣹⡀⢹⡰⠻⣮⣿⠣⣸⣿⣢⣾⡴⠉⡘⡰⣹⢟⠉⠆⠈⡌⣾⡿⠁⠘⠄⢳⣿⠳⡠⡎⢡⡇⢠⣿⣼⣷⣻⡿⠫⠀⠈⠎⢦⡆⡸⣾⠣⣤",
            r"⢇⢻⣿⡷⢳⠈⠀⢀⡿⣿⡧⠊⡶⣽⡄⠀⣱⢾⣗⣽⡽⡿⠉⢹⣿⢷⣿⠀⠀⣷⠻⢀⠌⢧⡦⠞⠑⣿⡇⠐⢤⠈⣺⡿⡎⢸⡀⠃⡷⠁⣿⠀⣿⣿⡁⠀⠱⡀⢘⣤⡟⢡⡯⢾⠉",
            r"⢸⢠⣿⣿⣅⣹⡖⠉⢀⣿⡟⣀⡕⢀⣬⡿⣵⠙⣿⣿⡀⠰⠰⠹⣿⡞⣿⡀⠇⣯⡆⣱⣜⠊⣇⠀⠀⣿⡗⡮⣼⣲⢿⣷⡷⠂⢡⠞⣧⠞⣸⣏⣿⡟⠀⠁⢢⡾⠫⡖⢹⣴⠏⢂⢡",
            r"⢸⣿⢾⣿⡟⢧⣇⢀⣿⢸⣇⣽⡞⠉⠀⣣⠉⢳⣿⠡⣫⡳⡅⠈⣿⣇⢸⡝⣼⠋⡗⢱⡊⣼⠈⣆⢸⣿⠈⢳⣸⣯⣽⡇⠘⣤⠏⣧⣯⣴⢼⣏⣿⡇⣦⡴⠫⠱⡜⠙⣾⣿⠔⡡⢞",
            r"⢸⡷⢿⣿⡇⠈⢿⣼⡿⢻⣧⠁⠻⡀⡰⠁⠱⡄⣿⢶⢡⣳⡈⣲⣻⣿⣾⡿⣱⠃⣇⡾⢻⢺⠀⡟⣾⡿⠐⣱⣿⢡⣹⣗⣾⣹⣠⣿⣏⠀⣺⣇⣿⣿⠋⢄⠀⠢⡇⢀⡼⣿⣜⠗⢹",
            r"⢺⣧⠊⢻⣿⣲⣼⣿⣷⣼⣿⠎⠀⡹⡅⠀⠀⠘⣿⡸⠷⣽⣷⢁⡽⣿⣿⣟⣇⣳⢁⡃⣸⠹⣶⠸⣿⣷⣾⡟⢸⡞⣽⣯⡶⣿⣏⢻⡇⡽⢹⡧⣿⢯⡀⠀⠑⢄⣿⣿⢶⢻⢸⢠⢻",
            r"⢸⡷⣣⣸⣿⡿⢝⣿⣧⣫⣿⢀⡤⠁⠘⣆⢀⠆⣿⣇⢀⣸⣿⠊⠀⢈⣿⣷⡹⠳⡝⣠⢗⢊⣧⣿⣿⢿⡿⣀⣶⢿⣿⣳⡅⣿⠜⣿⡿⠀⣼⢋⣿⠀⠬⣶⣄⢰⡟⡷⡆⢸⣧⠖⢻",
            r"⣻⣷⣿⢿⣿⣷⣈⣧⣿⠁⣿⡏⠀⠀⠀⠸⣧⣀⣿⡇⣹⡿⠈⢧⣀⡞⢸⣿⡇⣠⢿⡥⢋⠔⣿⣿⡳⣿⣷⡿⣏⣾⡿⣹⡼⣿⠀⢸⣿⣴⡿⢸⣿⠀⠠⢀⢋⣿⣓⣼⡾⢿⣇⠀⣸"
        ],
    },
        {
        "id": "desert_arena",
        "name": "Desert Arena",
        "desc": "Scorching dunes where only the strongest warriors battle beneath the burning sun.",
        "encounters": ["pekka", "mega_knight", "prince", "dark_prince", "archer_queen", "royal_ghost", "electro_wizard"],
        "loot": ["royal_blade", "steel_armor", "magic_tome"],
        "art": [
            r"        $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$W",
            r"        .$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$W",
            r"        .$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$i",
            r"        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$.",
            r"        W$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
            r"$u       #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$~",
            r"$#      `$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
            r"$i        $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
            r"$$        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
            r"$$         $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
            r"#$.        $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#",
            r"$$      $iW$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$!",
            r"$$i      $$$$$$$#'' `'''#$$$$$$$$$$$$$$$$$#'''''''#$$$$$$$$$$$$$$$W",
            r"#$$W    `$$$#'            '       !$$$$$`           `'#$$$$$$$$$$#",
            r"$$$     ``                 ! !iuW$$$$$                 #$$$$$$$#",
            r"#$$    $u                  $   $$$$$$$                  $$$$$$$~",
            r" #    #$$i.               #   $$$$$$$.                 `$$$$$$",
            r"        $$$$$i.                '''#$$$$i.               .$$$$#",
            r"        $$$$$$$$!         .   `    $$$$$$$$$i           $$$$$",
            r"        `$$$$$  $iWW   .uW`        #$$$$$$$$$W.       .$$$$$$#",
            r"            '#$$$$$$$$$$$$#`          $$$$$$$$$$$iWiuuuW$$$$$$$$W",
            r"            !#'''    ''             `$$$$$$$##$$$$$$$$$$$$$$$$",
            r"        i$$$$    .                   !$$$$$$ .$$$$$$$$$$$$$$$#",
            r"        $$$$$$$$$$`                    $$$$$$$$$Wi$$$$$$#'#$$`",
            r"        #$$$$$$$$$W.                   $$$$$$$$$$$#   ``",
            r"        `$$$$##$$$$!       i$u.  $. .i$$$$$$$$$#''",
            r"            '     `#W       $$$$$$$$$$$$$$$$$$$`      u$#",
            r"                            W$$$$$$$$$$$$$$$$$$      $$$$W",
            r"                            $$`!$$$##$$$$``$$$$      $$$$!",
            r"                           i$' $$$$  $$#''  '''     W$$$$",
            r"                                                W$$$$!",
            r"                    uW$$  uu  uu.  $$$  $$$Wu#   $$$$$$",
            r"                    ~$$$$iu$$iu$$$uW$$! $$$$$$i .W$$$$$$",
            r"            ..  !   '#$$$$$$$$$$##$$$$$$$$$$$$$$$$$$$$#'",
            r"            $$W  $     '#$$$$$$$iW$$$$$$$$$$$$$$$$$$$$$W",
            r"            $#`   `       ''#$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        ]
    },
    {
        "id": "dragons_peak",
        "name": "Dragon's Peak",
        "desc": "Crimson heights where the Baby Dragon sleeps upon treasure.",
        "encounters": ["baby_dragon"],
        "loot": ["magic_tome"],
        "art": [
            r"                     _",
            r"                    /#\\",
            r"                    /###\     /\\",
            r"                /  ###\   /##\  /\\",
            r"                /      #\ /####\/##\\",
            r"                /  /      /   # /  ##\             _       /\\",
            r"            // //  /\  /    _/  /  #\ _         /#\    _/##\    /\\",
            r"            // /   /  \     /   /    #\ \      _/###\_ /   ##\__/ _\\",
            r"            /  \   / .. \   / /   _   { \ \   _/       / //    /    \\",
            r"    /\     /    /\  ...  \_/   / / \   } \ | /  /\  \ /  _    /  /    \ /\\",
            r"_ /  \  /// / .\  ..%:.  /... /\ . \ {:  \\   /. \     / \  /   ___   /  \\",
            r"/.\ .\.\// \/... \.::::..... _/..\ ..\:|:. .  / .. \\  /.. \    /...\ /  \ \\",
            r"/...\.../..:.\. ..:::::::..:..... . ...\{:... / %... \\/..%. \  /./:..\__   \\",
            r".:..\:..:::....:::;;;;;;::::::::.:::::.\}.....::%.:. \ .:::. \/.%:::.:..\\",
            r"::::...:::;;:::::;;;;;;;;;;;;;;:::::;;::{:::::::;;;:..  .:;:... ::;;::::..",
            r";;;;:::;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;];;;;;;;;;;::::::;;;;:.::;;;;;;;;:..",
            r";;;;;;;;;;;;;;ii;;;;;;;;;;;;;;;;;;;;;;;;[;;;;;;;;;;;;;;;;;;;;;;:;;;;;;;;;;;;;",
            r";;;;;;;;;;;;;;;;;;;iiiiiiii;;;;;;;;;;;;;;};;ii;;iiii;;;;i;;;;;;;;;;;;;;;ii;;;",
            r"iiii;;;iiiiiiiiiiIIIIIIIIIIIiiiiiIiiiiii{iiIIiiiiiiiiiiiiiiii;;;;;iiiilliiiii",
            r"IIIiiIIllllllIIlllIIIIlllIIIlIiiIIIIIIIIIIIIlIIIIIllIIIIIIIIiiiiiiiillIIIllII",
            r"IIIiiilIIIIIIIllTIIIIllIIlIlIIITTTTlIlIlIIIlIITTTTTTTIIIIlIIllIlIlllIIIIIIITT",
            r"IIIIilIIIIITTTTTTTIIIIIIIIIIIIITTTTTIIIIIIIIITTTTTTTTTTIIIIIIIIIlIIIIIIIITTTT",
            r"IIIIIIIIITTTTTTTTTTTTTIIIIIIIITTTTTTTTIIIIIITTTTTTTTTTTTTTIIIIIIIIIIIIIITTTTT"
        ],
    },
    {
        "id": "dragon_finale",
        "name": "Dragon Arena",
        "description": "A silent crater where the air vibrates with ancient power.",
        "encounters": ["adult_dragon"],
        "loot": ["dragon_scale"],
    },
]
SECRET_FINAL_ARENA = {
    "id": "hidden_throne",
    "name": "Hidden Throne",
    "desc": "A forgotten arena sealed behind royal magic.",
    "encounters": ["archer_queen", "mega_knight", "golem"],
    "loot": ["magic_tome"],
    "art": [                                                                                                                                                
        r"-@@@@@@@@@@@@@@*#::+#@                                  .:+#@@@     @@@@@@@@@@@@@@@@@%",                      
        r"-@@@@@@@@@@@@@@@            . .                             ::-**@ @@@@@ @@@@@@@@@@@@+.",                     
        r"-@@@@@@@@@@@@                                                   .-  %@@@@@@@@@@@@@@@@+",                      
        r"-@@@@@@@@@@@@@@                                                     =@@@@@@@@@@@@@@@@-",                      
        r"=@@@@@@@@@@%=                                                       .-:-= @@@@@@@@@@@+",                      
        r"=@@@@@@@@@@#   ..                                                         @@@@@@@@@@@+.",                     
        r"=@@@@@@@@@@#=                                                              *%%@@@@@@@+",                      
        r"#@@@@@@@@@*                      ::-.          .#*#.                        :#@%@@@#",                       
        r"=@@@@@@@@      =:+#@#+---------+#@@@#-        :#@@@#+--:-----+#@@#=-.        +@@@@@+",                       
        r":@@@@@@@  -.  @@#+--:----+#@@@@@@@@@@#.      -#@@@@@@@@@@#+--------+++       :@@@@#.",                       
        r".#@@@@@@ *  +%%+.         :%@@@@@@@@@@+     -#@@@@@@@@#+-.          :##:      =#@@+",                        
        r"-#@@@@@   :++.            .=#@@@@@@@@#.   .#@@@@@@@#+               .++:      #@#.",                        
            r"+@@@@@@ *+-            :   #@@@@@@@@@+   +@@@@@@@@#    -==           +%+    +%@+",                         
            r"-@@@@  @#:       .-...-....+@@@@@@@@@#:  #@@@@@@@@#+-+++:+++-:-       *#=     @:",                         
            r"#@@@ @#-     -+==-.       =+%@@@@@@@@- -@@@@@@@@#+-:      @%#**+      -+.  @@@-",                         
            r"+@@@%%-    +%#*     .--:-   .+#@@@@@@: -@@@@@@@#-    ++-+%@#  @@*==    :: #@@@:",                         
            r"-@@@@+   +##==  +--+#@@@@#+-  -#@@@@@= -@@@@@@#+  .-+#@@@@@###  ####    :@*@@@.",                         
            r"-@@@@= -%@%+  :+#@@@@@@@@@@#-   #*@*#. :@@@@@#=  +#@@@@@@@@@@@@@* #@#:  .#@@@@=",                         
            r"-@@@@ #+++  :+#@@@@@@@@@@@@@#:  :: ++  .#@@@#-  *@@@@@@@@@@@@@@@##  %+-  +@@@@-",                         
            r":@@@@+-.  *%#@@##++--------+##-    =-    @@#+  +@@#+----:----+#@@@@% #+. %@@@@:",                         
            r"+@@@=    -#@@@@# .          %@#    @     @@@   %@@#           %@@@@#@    @@@@@:",                         
            r"#@@@    .%@@@@@%      .......-..   %     @@@  .-++-..--:-:=  :#@@#+-#+  :@@@@@-",                         
            r":@@@@     =----:-........           *+   -@@@        .----:-...---.        @@@@+ ",                        
            r"-@@@@#                          .   =#.  -@@@                            #@@@@@#",                         
            r"-@@@@@                       -:+::  :+.  :@@@ *.                         @@@@@@@",                         
            r"+@@@@@ *                  .+%@@@+   :     #@@  +*.                       @@@@@@@",                         
            r"+@@@ @@@              . -=%@@@#+   +-     +@@*  +++ :.                   @@@@@@@:",                        
            r"+@@@@@ @@=      -=--:=#@@@@@@#:   .+-     +@@    :#@@#+-. -              @@@@@@#",                         
            r".#@@@@@@@@  .   @@@@@@@ @@@@@#     %+    +#@@@-   #@@@@@@@@@@+          +@@@@@@+",                         
            r"-#@@@@@@ #- :##%@@@@@@@@@@@@#=  .  #  :%@@@@@#   %@@@@###@@@#+::.    -+#@@@@@#.",                         
            r"+@@@@@@%@-    + @@@@@@@@@++#%++#@@@ %#@@@@@@@####+-- * #@@@@@@@#   #@@@@@@@#-",                          
            r".#@@@@@@@+      @@@@@@@@    @#+-: -=*@@@@@@@@@@@#    +##@@@@@#*:::#@@@@@@@@+",                           
            r"-#@@@@@@%     #@@@@@@@@%++#@        %@@@@@@@@@%#+--+#@@@@@@@@      @@@@@@@",                            
            r"    +@@@@@@@=   +@@@@@@@@@@@@@@#+---:++% @@@@@@@@@@@@@@@@@@@@@@@    %@@@@@@@",                             
            r"    #@@@@@%.   #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#%#@@     @@@@@#=",                             
            r"    -#@@@@@   -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%  #@@-  :# %@@#:",                              
            r"    +@@@@%+  :@@@@%%#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #@@-  + @@@@+",                               
            r"    #@@@@#- -#@@@+ =#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%. +@@#  :%@@@@#.",                               
            r"    +@@@@@#- +@@@#+ +#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+ +#@@+ -#@@@@@+",                                
            r"    .#@@@@@+ +@@@ =- %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%= :+% #- =@@@@@#.",                                
            r"        -#@@@@#= #@@# :+ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@*- *+  @+  #@@@@@+",                                 
            r"        -#@@@@+  #@   =:  :+#@@@@@@@@@@@@@@@@@@@@@#+   +  ##@  +@@@@@#.",                                 
            r"        -#@@@*   #@%       ++-+#@@@@@@@@@@@@###@@+  +#%@@@@@ *#@@@@#=",                                  
            r"        :#@@  -  @@#:    =    #@@@@@@@@@@@@% %@@+ -+%@@@@@@@@@@@@#",                                    
            r"            .+%@@%#* ##++-+  @-...-:*%@@@@@@@@### @###@@@@@ @@@@@@%*",                                     
            r"            :#@@@@@# +#@@@@@+       @@@@@@@@@@@@@@@@@@@@@@@@@@#+",                                       
            r"                +#@@@#+  ###@@%+-:....+#@@@@@@@@@@@@###@@@@@@@#+.",                                        
            r"                .-+#@%%=* @@#+--:     #@@@@@@@@@@@@# #@@@@@#+.",                                          
            r"                    -#@@% + @:         *@%@@@@@@@%@ *##@@@@#:",                                            
            r"                    :+###@@            @@@@@@@@@@@@@@@@@#+"                                                                  
    ],  # Optional: leave blank or add throne ASCII if you want
}
AREAS.append(SECRET_FINAL_ARENA)
ITEMS = {
    "elixir_bottle": {"name": "Elixir Bottle", "effect": ("mana", 5)},
    "elixir_flask": {"name": "Elixir Flask", "effect": ("mana", 12)},
    "magic_tome": {"name": "Magic Tome", "effect": ("mana", 8)},
    "royal_sword": {"name": "Royal Sword", "effect": ("equip", {"atk": 3})},
    "crown_key": {"name": "Crown Key", "effect": ("key", None)},
    "treasure_map": {"name": "Treasure Map", "effect": ("map", None)},
    "dragon_scale": {"name": "Dragon Scale", "effect": ("dragon_scale", None)},
    "small_potion": {"name": "Small Potion", "effect": ("heal", 12)},
    "large_potion": {"name": "Large Potion", "effect": ("heal", 30)},
    "iron_sword": {"name": "Iron Sword", "effect": ("equip", {"atk": 2})},
    "royal_blade": {"name": "Royal Blade", "effect": ("equip", {"atk": 5})},
    "leather_armor": {"name": "Leather Armor", "effect": ("equip", {"def": 2})},
    "steel_armor": {"name": "Steel Armor", "effect": ("equip", {"def": 4})},
}
SHOP_ITEMS = [
    {"id": "elixir_bottle", "name": "Elixir Bottle", "price": 10},
    {"id": "small_potion", "name": "Small Potion", "price": 12},
    {"id": "elixir_flask", "name": "Elixir Flask", "price": 20},
    {"id": "royal_sword", "name": "Royal Sword", "price": 40},
    {"id": "steel_armor", "name": "Steel Armor", "price": 45},
    {"id": "magic_tome", "name": "Magic Tome", "price": 60},
    {"id": "dragon_scale", "name": "Dragon Scale", "price": 120},
]

ENEMIES = {
    "spear_goblin": {"name": "Spear Goblin", "hp": 10, "atk": 3, "agility": 8, "special": "throw", "range": 3, "taunts": ["Take this!", "Speeeear!"]},
    "ghost": {"name": "Ghost", "hp": 12, "atk": 4, "agility": 4, "special": "phase", "taunts": ["...fades...", "Whooo..."]},
    "skeleton_army": {"name": "Skeletons", "hp": 18, "atk": 5, "agility": 6, "special": "swarm", "taunts": ["Bones!", "Rattle!"]},
    "mini_pekka": {"name": "Mini P.E.K.K.A.", "hp": 34, "atk": 10, "agility": 3, "special": "sturdy", "taunts": ["CLANG!", "Charge!"]},
    "mega_minion": {"name": "Mega Minion", "hp": 26, "atk": 8, "agility": 5, "special": None, "taunts": ["Screee!", "Wing flap!"]},
    "valkyrie": {"name": "Valkyrie", "hp": 28, "atk": 8, "agility": 4, "special": "spin", "taunts": ["Spin!", "For glory!"]},
    "bandit": {"name": "Bandit", "hp": 24, "atk": 9, "agility": 10, "special": "dash", "taunts": ["Dash!", "Gotcha!"]},
    "trap_spike": {"name": "Spike Trap", "hp": 8, "atk": 11, "agility": 2, "special": "ambush", "taunts": ["Snap!", "Trap!"]},
    "baby_dragon": {"name": "Baby Dragon", "hp": 80, "atk": 12, "agility": 5, "special": "fire_breath", "taunts": ["ROAR!", "Flame!"]},
    "prince": {"name": "Prince", "hp": 48, "atk": 14, "agility": 6, "special": "charge", "taunts": ["Charge!", "For the King!"]},
    "dark_prince": {"name": "Dark Prince", "hp": 32, "atk": 10, "agility": 7, "special": "charge", "taunts": ["Small charge!", "Mini charge!"]},
    "pekka": {"name": "P.E.K.K.A.", "hp": 60, "atk": 18, "agility": 3, "special": "sturdy", "taunts": ["DESTROY!", "P.E.K.K.A. POWER!"]},
    "electro_wizard": {"name": "Electro Wizard", "hp": 40, "atk": 7, "agility": 8, "special": "stun", "range": 3, "taunts": ["Zap zap!", "Don't blink!"]},
    "witch": {"name": "Witch", "hp": 18, "atk": 4, "agility": 5, "special": "summon", "range": 3, "taunts": ["Rise, my minions!", "Heh heh!"]},
    "golem": {"name": "Golem", "hp": 80, "atk": 16, "agility": 2, "special": "explode", "taunts": ["Grrr!", "Crush!"]},
    "bowler": {"name": "Bowler", "hp": 22, "atk": 6, "agility": 4, "special": "knockback", "range": 3, "taunts": ["Strike!", "Rock and roll!"]},
    "lumberjack": {"name": "Lumberjack", "hp": 38, "atk": 12, "agility": 8, "special": "rage", "taunts": ["Raaagh!", "Chop chop!"]},
    "archer_queen": {"name": "Archer Queen", "hp": 40, "atk": 9, "agility": 9, "special": "invis", "range": 4, "taunts": ["Silent shot!", "Can’t see me!"]},
    "mega_knight": {"name": "Mega Knight", "hp": 70, "atk": 17, "agility": 5, "special": "slam", "taunts": ["Mega slam!", "Boom!"]},
    "royal_ghost": {"name": "Royal Ghost", "hp": 25, "atk": 8, "agility": 8, "special": "phase", "taunts": ["Boo!", "Invisible strike!"]},
    "adult_dragon": {"name": "Adult Dragon", "hp": 200, "atk": 11, "agility": 6, "special": "fire", "range": 3, "taunts": ["Roooar!", "Flames rise."]},
}

# -------------------- Globals --------------------
GRID_ROWS = 7
GRID_COLS = 11

# -------------------- Utilities --------------------
def roll(sides=20):
    # random roll with digit-by-digit correctness not required; still uses randint
    return random.randint(1, sides)

def clamp_pos(r, c):
    r = max(0, min(GRID_ROWS - 1, r))
    c = max(0, min(GRID_COLS - 1, c))
    return (r, c)

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# -------------------- Player --------------------
class Player:
    def __init__(self, name, pclass):
        base = CLASSES[pclass]
        self.name = name
        self.pclass = pclass
        # buff player stats slightly per request
        self.strength = base["Strength"] + 2
        self.agility = base["Agility"] + 2
        self.magic = base["Magic"] + 2
        self.max_hp = base["hp"] + 8
        self.hp = self.max_hp
        self.level = 1
        self.exp = 0
        self.inventory = []
        self.equipment = {}
        self.gold = 0
        self.mana = self.magic * 2
        self.story_flags = set()
        self.passive = base["passive"]

    def add_item(self, item_id):
        self.inventory.append(item_id)

    def remove_item(self, item_id):
        if item_id in self.inventory:
            self.inventory.remove(item_id)

    def describe_item(self, item_id):
        it = ITEMS.get(item_id)
        if not it:
            return "Unknown item."

        name = it["name"]
        eff = it.get("effect")

        if eff[0] == "heal":
            return f"{name}: Restores {eff[1]} HP."
        if eff[0] == "mana":
            return f"{name}: Restores {eff[1]} MP."
        if eff[0] == "equip":
            stats = eff[1]
            if "atk" in stats:
                return f"{name}: Weapon (+{stats['atk']} ATK)"
            if "def" in stats:
                return f"{name}: Armor (+{stats['def']} DEF)"
        if eff[0] == "key":
            return f"{name}: A key item. Used to unlock something later."
        if eff[0] == "map":
            return f"{name}: Reveals the way to a hidden place."
        if eff[0] == "dragon_scale":
            return f"{name}: A mystical scale. Affects the dragon encounter."

        return f"{name}: No special description."


    def summary_line(self):
        return f"{self.name} ({self.pclass}) HP:{self.hp}/{self.max_hp} STR:{self.strength} AGI:{self.agility} MAG:{self.magic} MP:{self.mana}"

    def apply_item(self, key, state=None):
        it = ITEMS.get(key)
        if not it:
            return False, "Unknown item."
        if state is None:
            state = {}
        eff = it["effect"]
        if eff[0] == "heal":
            # --- Health scaling by arena ---
            area_name = state.get("area_name", "")
            scale = 1.0

            if area_name == "Goblin Forest":
                scale = 1.0
            elif area_name == "Royal Arena":
                scale = 1.2
            elif area_name == "Dark Valley":
                scale = 1.4
            elif area_name == "Desert Arena":
                scale = 1.6
            elif area_name == "Hidden Throne":
                scale = 2.0

            heal_amount = int(eff[1] * scale)
            old = self.hp
            self.hp = min(self.max_hp, self.hp + heal_amount)
            return True, f"You heal {self.hp - old} HP."
        if eff[0] == "mana":
            old = self.mana
            self.mana += eff[1]
            return True, f"You restore {self.mana - old} mana."
        if eff[0] == "equip":
            # Determine whether this is a weapon or armor
            if "atk" in eff[1]:
                slot = "weapon"
            elif "def" in eff[1]:
                slot = "armor"
            else:
                return False, "Invalid equipment type."
            # If something is already equipped in that slot, return it to inventory
            if slot in self.equipment:
                old_item = self.equipment[slot]
                self.inventory.append(old_item)
            # Equip the new item
            self.equipment[slot] = key
            return True, f"You equip {it['name']}."
        if eff[0] == "key":
            self.story_flags.add("has_crown_key")
            return True, f"You got {it['name']}."
        if eff[0] == "map":
            self.story_flags.add("has_map")
            return True, "Map found."
        if eff[0] == "dragon_scale":
            self.story_flags.add("dragon_scale")
            return True, "Dragon Scale resonates with you."
        return False, "Nothing happened."

# -------------------- Curses helper UI --------------------
def show_throne_room_ending(ui, player):
    ui.clear()
    lines = [
        "",
        "The throne room falls silent.",
        "The final echo of battle fades into the vaulted stone.",
        "",
        "Sunlight breaks through shattered stained glass,",
        "casting fractured colors across the marble floor.",
        "",
        "You stand victorious.",
        "",
        "The tyrant who ruled through fear is gone.",
        "The people will speak your name with hope now.",
        "",
        f"{player.name}, Liberator of the Realm.",
        "",
        "",
        "Press any key to continue..."
    ]

    row = 2
    for line in lines:
        ui.stdscr.addstr(row, 4, line)
        ui.stdscr.refresh()
        time.sleep(0.6)
        row += 1

    ui.stdscr.getch()
    ui.clear()

    # Final title card
    title = [
        "",
        "   === EPILOGUE ===",
        "",
        "   Peace does not come easily.",
        "   It must be protected.",
        "",
        "   But today, the world breathes freely.",
        "",
        "",
        "   THE END"
    ]

    row = 3
    for line in title:
        ui.stdscr.addstr(row, 4, line, curses.A_BOLD)
        ui.stdscr.refresh()
        time.sleep(0.5)
        row += 2

    ui.stdscr.getch()
    exit()
def show_spared_dragon_ending(ui, player):
    ui.clear()
    lines = [
        "",
        "The dragon lowers its wings.",
        "Its breath comes slow and ragged, but it does not strike again.",
        "",
        "You hold your weapon, but you do not lift it.",
        "",
        "For a long moment, neither of you move.",
        "",
        "Then, the dragon's eyes meet yours.",
        "",
        "Not as enemies.",
        "Not as beast and slayer.",
        "",
        "But as two beings who have survived the world.",
        "",
        f"'{player.name}...'",
        "The voice is ancient, felt rather than heard.",
        "",
        "'You choose mercy, when others chose fear.'",
        "",
        "The dragon bows its head.",
        "",
        "",
        "Press any key to continue..."
    ]

    row = 2
    for line in lines:
        ui.stdscr.addstr(row, 4, line)
        ui.stdscr.refresh()
        time.sleep(0.6)
        row += 1

    ui.stdscr.getch()
    ui.clear()

    # Closing scene
    closing = [
        "",
        "The world will never know what passed here.",
        "They will speak of the dragon you could have slain.",
        "They will never understand the choice you made.",
        "",
        "But the sky feels wider now.",
        "The horizon feels open.",
        "",
        "And somewhere beyond the mountains,",
        "a great shadow flies not as terror...",
        "but as freedom itself.",
        "",
        "",
        "   === THE END ==="
    ]

    row = 3
    for line in closing:
        ui.stdscr.addstr(row, 4, line, curses.A_BOLD if "THE END" in line else 0)
        ui.stdscr.refresh()
        time.sleep(0.5)
        row += 2

    ui.stdscr.getch()
    exit()

def show_ending_cutscene(ui, player):
    ui.clear()
    lines = [
        "",
        "The battlefield falls quiet.",
        "Ash drifts through the still air.",
        "",
        "Before you lies the fallen dragon.",
        "A creature of legend. A mountain of power and fire.",
        "",
        "Your chest rises slowly. Every breath heavy. Every muscle trembling.",
        "",
        "Yet you stand.",
        "",
        "The world will remember this moment.",
        "",
        f"{player.name}, Dragonslayer.",
        "",
        "",
        "Press any key to continue..."
    ]

    row = 2
    for line in lines:
        ui.stdscr.addstr(row, 4, line)
        ui.stdscr.refresh()
        time.sleep(0.6)
        row += 1

    ui.stdscr.getch()
    ui.clear()

    # Final title card
    title = [
        "",
        "   === THE END ===",
        "",
        "   Thank you for playing."
    ]

    row = 5
    for line in title:
        ui.stdscr.addstr(row, 6, line, curses.A_BOLD)
        row += 2
    ui.stdscr.refresh()
    ui.stdscr.getch()
    exit()


class UI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        # color pairs (foreground, background)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   # player tile
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)    # enemy tile
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # HUD
        curses.init_pair(4, curses.COLOR_YELLOW, -1)                 # highlight
        curses.init_pair(5, curses.COLOR_GREEN, -1)                  # success
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)                # info
        self.height, self.width = self.stdscr.getmaxyx()

    def clear(self):
        self.stdscr.erase()

    def draw_text_block(self, lines, y_off=1, x_off=2):
        for i, line in enumerate(lines):
            if y_off + i < self.height - 1:
                self.stdscr.addstr(y_off + i, x_off, line)

    def draw_zone_art(self, art_lines, title, desc):
        self.clear()
        mid_x = max(0, (self.width // 2) - 20)
        self.stdscr.addstr(1, mid_x, title, curses.A_BOLD | curses.color_pair(6))
        for i, ln in enumerate(art_lines):
            if 3 + i < self.height - 2:
                try:
                    self.stdscr.addstr(3 + i, mid_x, ln[:self.width - mid_x - 2])
                except curses.error:
                    pass
        # description box
        self.stdscr.addstr(10, 2, desc)
        self.stdscr.addstr(self.height - 2, 2, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getch()

    def display_message_with_animation(self, message, y=None, x=2, delay=0.04):
        if y is None:
            y = self.height - 4
        for i in range(1, len(message)+1):
            self.stdscr.addstr(y, x, message[:i])
            self.stdscr.refresh()
            time.sleep(delay)

    def rolling_animation(self, label="Rolling", y=None, x=2, rolls=6, max_val=20):
        if y is None:
            y = self.height - 4

        # Always decide the final roll first
        final_val = random.randint(1, max_val)
        shown_val = None

        for i in range(rolls):
            dots = "." * ((i % 3) + 1)
            if i < rolls - 2:
                shown_val = random.randint(1, max_val)
            elif i == rolls - 2:
                # show a slightly off value
                shown_val = max(1, min(max_val, final_val - random.randint(1, 3)))
            else:
                shown_val = final_val  # exact final value now visible
            self.stdscr.addstr(y, x, f"{label} {dots} {shown_val:2d}   ")
            self.stdscr.refresh()
            time.sleep(0.18)

        # make sure the very last draw stays visible as the final result
        self.stdscr.addstr(y, x, f"{label}: {final_val:2d}   ")
        self.stdscr.refresh()
        time.sleep(0.4)

        return final_val



    def type_and_replace(self, frames, y=None, x=2, delay=0.05):
        if y is None:
            y = self.height - 4
        for frame in frames:
            self.stdscr.addstr(y, x, " " * (self.width - x - 2))
            self.stdscr.addstr(y, x, frame)
            self.stdscr.refresh()
            time.sleep(delay)

    def draw_grid(self, player_pos, enemies):
        top = 2
        left = 2
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                ch = " . "
                color = curses.color_pair(0)
                if (r, c) == player_pos:
                    ch = " P "
                    color = curses.color_pair(1)
                else:
                    found = None
                    for idx, e in enumerate(enemies, 1):
                        if e["hp"] > 0 and e["pos"] == (r, c):
                            found = idx
                            break
                    if found is not None:
                        ch = f"E{found}"
                        color = curses.color_pair(2)
                try:
                    self.stdscr.addstr(top + r, left + c*3, ch, color)
                except curses.error:
                    pass  # in case terminal is small
                # >>> Show enemy list neatly under the player's inventory in the HUD
                try:
                    hud_x = 45
                    # draw starting a bit lower than inventory section (line ~9)
                    y = 13
                    self.stdscr.addstr(y, hud_x, "=== Enemies ===", curses.A_BOLD | curses.color_pair(3))
                    line = 1
                    for i, e in enumerate(enemies, 1):
                        if e["hp"] > 0:
                            name = e["name"]
                            self.stdscr.addstr(y + line, hud_x, f"E{i}: {name} {e['hp']}/{e.get('max_hp', e['hp'])}")
                            line += 1
                    # clear a couple extra lines below in case old enemies are gone
                    for clr in range(line, line + 4):
                        self.stdscr.addstr(y + clr, hud_x, " " * 35)
                except curses.error:
                    pass
                # <<<



    def draw_hud(self, player, messages):
        # top-right area for stats
        stat_x = 45
        try:
            # Player stats
            self.stdscr.addstr(1, stat_x, "=== STATUS ===", curses.A_BOLD | curses.color_pair(3))
            self.stdscr.addstr(2, stat_x, player.summary_line())
            self.stdscr.addstr(4, stat_x, f"Gold: {player.gold}  Lv:{player.level}  Exp:{player.exp}")
            self.stdscr.addstr(6, stat_x, "Inventory:")
            inv_preview = ", ".join([ITEMS[i]["name"] for i in player.inventory[:5]])
            self.stdscr.addstr(7, stat_x, inv_preview[:self.width - stat_x - 2])

            # Clear old message area first
            msg_y_start = self.height - 7
            msg_lines = 6
            for i in range(msg_lines):
                self.stdscr.addstr(msg_y_start + i, 2, " " * (self.width - 4))

            # Display only latest messages
            latest = messages[-msg_lines:]
            for i, m in enumerate(latest):
                self.stdscr.addstr(msg_y_start + i, 2, m[:self.width-4])
        except curses.error:
            pass

    def refresh(self):
        self.stdscr.refresh()

# -------------------- Combat helpers & smarter AI --------------------

def spawn_enemies(area, player_pos):
# === Arena-based spawn rules ===
    # If this fight has a specifically forced encounter (e.g., adult dragon), respect it
    if area["name"] == "Dragon Arena":
        # Spawn exactly one adult dragon, placed in front of player
        count = 1

        # existing code continues...
    # === SECRET FINAL ARENA ALWAYS 2 ENEMIES ===
    if area["name"] == "Hidden Throne":
        count = 4

    # Desert Arena: Always 1v1 strong duels
    elif area["name"] == "Desert Arena":
        count = 1

    # Goblin Forest: Never 1v1 strong fights — only group fights
    elif area["name"] == "Goblin Forest":
        count = random.randint(2, 3)

    # Other arenas: Increase 1v1 strong fights to be more common
    else:
        count = 1 if random.random() < 0.5 else random.randint(2, 3)


    # spawn 1-3 enemies on right side, not overlapping player
    enemies = []
    attempts = 0

    # pick encounter pool
    encounter_pool = area["encounters"][:]

    # if only one enemy spawns, choose stronger ones
    if count == 1 and area["name"] != "Dragon Arena":
        # strong Clash Royale elites
        strong_pool = ["pekka", "mega_knight", "prince", "golem", "archer_queen", "royal_ghost"]
        # sometimes add electro wizard or lumberjack
        if random.random() < 0.3:
            strong_pool += ["electro_wizard", "lumberjack"]
        encounter_pool = strong_pool

    for i in range(count):
        key = random.choice(encounter_pool)
        template = deepcopy(ENEMIES[key])
        placed = False
        while not placed and attempts < 400:
            attempts += 1
            r = random.randint(0, GRID_ROWS - 1)
            c = random.randint(GRID_COLS//2, GRID_COLS - 1)
            if (r, c) != player_pos and all(e["pos"] != (r, c) for e in enemies):
                template["pos"] = (r, c)
                # scale HP slightly depending on group size
                hp_mult = 1.0 + (0.25 if count == 1 else -0.1 * (count - 1))
                template["hp"] = int(template["hp"] * hp_mult)
                template["max_hp"] = template["hp"]
                template["id"] = f"{key}_{i+1}"
                # Arena-based scaling for 1v1 powerful fights
                # Only applies when count == 1 (meaning elite duel)
                if count == 1 or count == 4:
                    arena_name = area["name"]
                    # Define scaling by arena progression
                    if arena_name == "Goblin Forest":
                        scale = 0.75   # weaker elites early
                    elif arena_name == "Royal Arena":
                        scale = 0.75    # normal strength
                    elif arena_name == "Dark Valley":
                        scale = 1   # slightly buffed
                    elif arena_name == "Desert Arena":
                        scale = 1.25    # real boss fights
                    elif arena_name == "Hidden Throne":
                        scale = 2 # super boss fights
                    else:
                        scale = 1.0    # fallback

                    template["hp"] = int(template["hp"] * scale)
                    template["max_hp"] = template["hp"]
                    template["atk"] = int(template["atk"] * scale)
                enemies.append(template)
                placed = True
        if not placed:
            template["pos"] = (0, GRID_COLS - 1 - i)
            template["id"] = f"{key}_{i+1}"
            enemies.append(template)
    return enemies


def compute_attack(attacker, defender, roll_override=None):
    """
    Compute damage and return (damage, roll_val).
    If roll_override is provided, use that value instead of generating a new random roll.
    """
    # allow tests / UI to supply the roll so animation and logic match
    roll_val = roll_override if roll_override is not None else roll(20)
    atk = attacker.get("atk", 0)
    str_bonus = attacker.get("strength", 0) // 2
    mag_bonus = attacker.get("magic", 0) // 2
    def_ag = defender.get("agility", 0) // 2
    dmg = max(0, (roll_val // 2) + atk + str_bonus + mag_bonus - def_ag)
    return dmg, roll_val

def find_path_around(enemies, src, dest):
    # Simple BFS pathfinder that treats enemy tiles as obstacles (so enemies will try to go around each other)
    # returns next step toward dest, or direct greedy fallback
    q = deque()
    q.append(src)
    visited = {src: None}
    obstacles = {e["pos"] for e in enemies if e["hp"] > 0}
    obstacles.discard(dest)  # allow destination if an enemy stands there
    while q:
        cur = q.popleft()
        if cur == dest:
            break
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = cur[0]+dr, cur[1]+dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                nxt = (nr, nc)
                if nxt not in visited and nxt not in obstacles:
                    visited[nxt] = cur
                    q.append(nxt)
    if dest not in visited:
        # fallback: greedy step
        dr = 0
        dc = 0
        if src[0] < dest[0]: dr = 1
        elif src[0] > dest[0]: dr = -1
        if src[1] < dest[1]: dc = 1
        elif src[1] > dest[1]: dc = -1
        nextpos = clamp_pos(src[0]+dr, src[1]+dc)
        return nextpos
    # reconstruct path
    cur = dest
    while visited[cur] != src:
        cur = visited[cur]
        if cur is None:
            return src
    return cur

def enemy_ai_move_and_act(e_idx, enemy, state, player, player_pos, enemies, ui, messages):
    # smarter AI:
    # prioritize target: if multiple players/targets were present they'd pick lowest HP; here always player
    # behaviour:
    # - if adjacent: decide attack (or special) or defend if low hp
    # - if not adjacent: pathfind around obstacles toward player, sometimes flank (choose lateral move)
    # - taunt occasionally
    if enemy["hp"] <= 0:
        return
    # random taunt
    if random.random() < 0.08:
        t = random.choice(enemy.get("taunts", ["..."]))
        messages.append(f"{enemy['name']}: {t}")
    # pre-turn special set
    sp = enemy.get("special")
    if sp == "phase" and random.random() < 0.2:
        state["phased"] = True
        messages.append(f"{enemy['name']} fades and will evade next hit.")
    elif sp == "phase":
        state["phased"] = False
        messages.append(f"{enemy['name']} de-fades")
    if sp == "swarm" and random.random() < 0.2:
        state["swarm_rage"] = True
    else:
        state["swarm_rage"] = False
    # decide move
    # --- MOVE FIRST ---
    dist_before = manhattan(enemy["pos"], player_pos)

    moved = False  # track if this unit moved this turn

    enemy_range = enemy.get("range", 1)

    # If ranged enemy is too close (adjacent), step back instead of forward
    if enemy_range > 1 and dist_before <= 2:
        best = enemy["pos"]
        bestd = dist_before
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = enemy["pos"][0]+dr, enemy["pos"][1]+dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS and not any(e["pos"] == (nr,nc) for e in enemies):
                d = manhattan((nr,nc), player_pos)
                if d > bestd:
                    best = (nr,nc)
                    bestd = d
        if best != enemy["pos"]:
            enemy["pos"] = best
            messages.append(f"{enemy['name']} backs away!")
            moved = True

    # Try to move toward player if not already adjacent
    if dist_before > 1:
        nextpos = find_path_around(enemies, enemy["pos"], player_pos)

        # avoid collisions and moving onto player tile
        if nextpos != player_pos and not any(other["pos"] == nextpos and other["hp"] > 0 for other in enemies if other is not enemy):
            enemy["pos"] = nextpos
            moved = True

    # --- THEN ATTACK IF IN RANGE ---
    dist_after = manhattan(enemy["pos"], player_pos)
    enemy_range = enemy.get("range", 1)
    # 50/50 chance ranged units will NOT attack if they moved this turn
    if moved and enemy_range > 1 and random.random() < 0.5:
        return


    if dist_after <= enemy_range:
        # ranged taunt or message
        if enemy_range > 1 and dist_after > 1:
            messages.append(f"{enemy['name']} attacks from a distance!")

        # retreat logic for low hp melee only
        if enemy_range == 1 and enemy["hp"] < max(6, enemy.get("atk", 5)) and random.random() < 0.4:
            best = enemy["pos"]
            bestd = manhattan(best, player_pos)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = enemy["pos"][0] + dr, enemy["pos"][1] + dc
                if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS and not any(other["pos"] == (nr, nc) for other in enemies):
                    d = manhattan((nr, nc), player_pos)
                    if d > bestd:
                        best = (nr, nc)
                        bestd = d
            if best != enemy["pos"]:
                enemy["pos"] = best
                messages.append(f"{enemy['name']} retreats!")
                return
        # perform attack
        dmg, r = compute_attack(enemy, {"agility": player.agility})

        if state.get("swarm_rage"):
            dmg += 3
        if player.passive == "armor":
            dmg = max(0, dmg - 1)
        if "armor" in player.equipment:
            armor_key = player.equipment["armor"]
            armor = ITEMS.get(armor_key, {})
            eff = armor.get("effect", (None, None))
            if isinstance(eff[1], dict) and eff[1].get("def"):
                dmg = max(0, dmg - eff[1]["def"])

        if enemy_range > 1:
            messages.append(f"{enemy['name']} fires a ranged attack for {dmg} damage!")
        else:
            messages.append(f"{enemy['name']} hits you for {dmg} damage!")

        player.hp -= dmg
        return


        # else attack
        # maybe special multi-hit for 'dash' or 'spin'
        # compute attack roll animation
        # do a dice roll using UI if provided

# -------------------- Combat main (curses-driven) --------------------
def combat_sequence(stdscr, ui, player, area):
    # spawn enemies
    # If area is a dict, use its name. If it's just a string, use it directly.
    state = {"area_name": area["name"] if isinstance(area, dict) else area}
    player_pos = (GRID_ROWS//2, 1)
    enemies = spawn_enemies(area, player_pos)
    enemy_states = [dict(first=True) for _ in enemies]
    messages = [f"Encounter: {', '.join(e['name'] for e in enemies)}"]
    turn = 1
    defending = False

    while True:
        ui.clear()
        messages.append(f"========= Turn {turn}")
        ui.draw_grid(player_pos, enemies)
        ui.draw_hud(player, messages)
        messages.clear()
        messages.append(f"========= Turn {turn}")
        ui.stdscr.addstr(
            GRID_ROWS + 4,
            2,
            "Turn {} - Move (W/A/S/D), then choose action (1 Attack, 2 Defend, 3 Magic, 4 Item, m Move Again, r Run, p Pass).".format(turn)
        )
        ui.refresh()

        # pre-turn enemy states
        for i,e in enumerate(enemies):
            if e["hp"]>0 and enemy_states[i].get("phased"):
                # phased remains until next incoming attack; we set it already in AI pre-turns
                pass

        # Movement input (one step max)
        ui.stdscr.addstr(GRID_ROWS + 6, 2, "Movement: ")
        ui.stdscr.refresh()
        key = ui.stdscr.getkey()
        ui.stdscr.addstr(GRID_ROWS + 6, 12, key)
        ui.stdscr.refresh()
        time.sleep(0.15)
        mv_done = False
        try:
            if key.lower() in ("w","a","s","d"):
                drdc = {"w":(-1,0),"s":(1,0),"a":(0,-1),"d":(0,1)}[key.lower()]
                newp = clamp_pos(player_pos[0]+drdc[0], player_pos[1]+drdc[1])
                # cannot move onto enemy tile
                if any(e["pos"] == newp and e["hp"]>0 for e in enemies):
                    messages.append("Can't move onto enemy — blocked.")
                else:
                    player_pos = newp
            elif key.lower() == "p":  # pass movement
                messages.append("You chose to skip movement.")
            else:
                # if not movement key, treat as action key pressed immediately (fall through)
                pass
        except Exception:
            pass

        # action selection
        ui.stdscr.addstr(GRID_ROWS + 7, 2, "Action: ")
        ui.stdscr.refresh()
        action_key = ui.stdscr.getkey()
        ui.stdscr.addstr(GRID_ROWS + 7, 10, action_key)
        ui.stdscr.refresh()
        time.sleep(0.15)  
        action = ""
        if action_key == "1":
            action = "attack"
        elif action_key == "2":
            action = "defend"
        elif action_key == "3":
            action = "magic"
        elif action_key == "4":
            action = "item"
        elif action_key.lower() == "r":
            action = "run"
        elif action_key.lower() == "p":  # pass action
            action = "pass"
        elif action_key == "m":
            action = "move_again"
        else:
            # some terminals return string length >1; allow w/a/s/d repeated -> attempt to ignore
            messages.append("Invalid action key.")
            action = None

        # Player action resolution
        if action == "attack":
            # display rolling animation and use that same roll for the actual damage
            rollv = ui.rolling_animation("Attack roll", y=GRID_ROWS + 8, x=2, rolls=6, max_val=20)

            # find adjacent enemies
            adjacent = [(i,e) for i,e in enumerate(enemies)
                        if e["hp"] > 0 and manhattan(player_pos, e["pos"]) == 1]

            if not adjacent:
                messages.append("No adjacent enemy to attack.")
            else:
                # --- MULTIPLE TARGETS: LET PLAYER CHOOSE ---
                if len(adjacent) > 1:
                    ui.stdscr.addstr(GRID_ROWS + 10, 2, "Choose target: ")
                    y = GRID_ROWS + 11
                    for n, (idx, enemy) in enumerate(adjacent, start=1):
                        ui.stdscr.addstr(y, 2, f"{n}) {enemy['name']} ({enemy['hp']} HP)")
                        y += 1
                    ui.stdscr.refresh()
                    choice = ui.stdscr.getkey()
                    ui.stdscr.addstr(GRID_ROWS + 10, 17, choice)
                    ui.stdscr.refresh()
                    time.sleep(0.15)
                    if choice.isdigit():
                        sel = int(choice)
                        if 1 <= sel <= len(adjacent):
                            chosen_idx = adjacent[sel - 1][0]
                        else:
                            chosen_idx = adjacent[0][0]
                            messages.append("Invalid target, attacking nearest.")
                    else:
                        chosen_idx = adjacent[0][0]
                        messages.append("Invalid input, attacking nearest.")
                else:
                    chosen_idx = adjacent[0][0]

                target = enemies[chosen_idx]
                tstate = enemy_states[chosen_idx]
                if tstate.get("phased"):
                    messages.append(f"{target['name']} phases and avoids your attack!")
                    tstate["phased"] = False
                else:
                    # compute damage with a short damage text animation
                    weapon_atk = 0
                    if "weapon" in player.equipment:
                        weapon_key = player.equipment["weapon"]
                        weapon = ITEMS.get(weapon_key, {})
                        eff = weapon.get("effect", (None, None))
                        if isinstance(eff[1], dict) and eff[1].get("atk"):
                            weapon_atk = eff[1]["atk"]
                        else:
                            weapon_atk = 2

                    p_stat = {"atk": weapon_atk, "strength": player.strength, "magic": 0}
                    # use the same roll value from animation
                    dmg, _ = compute_attack(p_stat, {"agility": target["agility"]}, roll_override=rollv)
                    if player.passive == "swift":
                        dmg += 1

                    if rollv > 18:
                        dmg *= 2
                        ui.display_message_with_animation("CRITICAL STRIKE!", y=GRID_ROWS+9, x=2)

                    frames = ["D", "Da", "Dam", "Dama", "Damag", "Damage!"]
                    ui.type_and_replace(frames, y=GRID_ROWS+10, x=2, delay=0.06)
                    messages.append(f"You deal {dmg} to {target['name']} (roll {rollv}).")
                    target["hp"] -= dmg
                    if target["hp"] <= 0:
                        messages.append(f"{target['name']} falls!")
        elif action == "move_again":
            ui.stdscr.addstr(GRID_ROWS + 8, 2, "Move Again: ")
            ui.stdscr.refresh()
            k2 = ui.stdscr.getkey()

            # display pressed key
            ui.stdscr.addstr(GRID_ROWS + 8, 14, k2)
            ui.stdscr.refresh()
            time.sleep(0.15)

            if k2.lower() in ("w", "a", "s", "d"):
                drdc = {"w":(-1,0), "s":(1,0), "a":(0,-1), "d":(0,1)}[k2.lower()]
                newp = clamp_pos(player_pos[0] + drdc[0], player_pos[1] + drdc[1])
                if any(e["pos"] == newp and e["hp"] > 0 for e in enemies):
                    messages.append("Second move blocked by enemy.")
                else:
                    player_pos = newp
                    messages.append("You move again.")
            else:
                messages.append("Invalid second movement.")
        elif action == "defend":
            defending = True
            messages.append("You brace for incoming attacks. (Damage reduced this turn)")
        elif action == "magic":
            if player.mana < 1:
                messages.append("No mana.")
            else:
                # simple choices: 1 Firebolt (3), 2 Heal (2)
                ui.stdscr.addstr(GRID_ROWS + 8, 2, "1 Firebolt - Damage nearby enemies(3)")
                ui.stdscr.addstr(GRID_ROWS + 9, 2, "2 Heal - Heal yourself (2)")
                ui.stdscr.refresh()
                k = ui.stdscr.getkey()
                if k == "1" and player.mana >= 3:
                    player.mana -= 3
                    # area damage up to distance 2
                    # Fire magic range: can hit any enemy within 3 tiles
                    targets = [(i,e) for i,e in enumerate(enemies)
                            if e["hp"]>0 and manhattan(player_pos, e["pos"]) <= 3]
                    if not targets:
                        messages.append("No targets in range for Firebolt.")
                    else:
                        for idx, e in targets:
                            tstate = enemy_states[idx]
                            if tstate.get("phased"):
                                messages.append(f"{e['name']} phased and avoided Firebolt!")
                                tstate["phased"] = False
                            else:
                                dmg, rv = compute_attack({"atk":3,"magic":player.magic}, {"agility": e["agility"]})
                                messages.append(f"Firebolt hits {e['name']} for {dmg}.")
                                e["hp"] -= dmg
                elif k == "2" and player.mana >= 2:
                    player.mana -= 2
                    healed = min(player.max_hp - player.hp, 6 + player.magic)
                    player.hp += healed
                    messages.append(f"You cast Heal and gain {healed} HP.")
                else:
                    messages.append("Invalid magic choice or insufficient mana.")
        elif action == "item":
            if not player.inventory:
                messages.append("Inventory empty.")
            else:
                # show simple numbered inventory
                ui.stdscr.addstr(GRID_ROWS + 8, 2, "Inventory: " + ", ".join([f"{i+1}:{ITEMS[k]['name']}" for i,k in enumerate(player.inventory[:6])]) + "   ")
                ui.stdscr.addstr(11, 2, "Press number to use, 'i' to inspect, or any other key to cancel.")
                ui.stdscr.refresh()
                k = ui.stdscr.getkey()
            if k.isdigit():
                idx = int(k)-1
                if 0 <= idx < len(player.inventory):
                    key = player.inventory.pop(idx)
                    ok, msg = player.apply_item(key, state)
                    messages.append(msg)
                else:
                    messages.append("Invalid item index.")

            elif k.lower() == "i":
                # inspect mode
                ui.clear()
                ui.draw_text_block(["Select an item number to inspect:"], 2, 2)
                ui.draw_text_block(
                    [f"{i+1}: {ITEMS[item]['name']}" for i, item in enumerate(player.inventory)], 
                    4, 2
                )
                ui.refresh()
                ch2 = ui.stdscr.getkey()

                if ch2.isdigit():
                    idx = int(ch2)-1
                    if 0 <= idx < len(player.inventory):
                        desc = player.describe_item(player.inventory[idx])
                        ui.display_message_with_animation(desc, y=ui.height-4)
                        ui.stdscr.getch()
                else:
                    ui.display_message_with_animation("Inspection canceled.", y=ui.height-4)
                    ui.stdscr.getch()
            else:
                messages.append("Item canceled.")
        elif action == "run":
            flee_chance = max(10, min(95, 30 + player.agility * 3 - len([e for e in enemies if e["hp"]>0])*5))
            # animated roll
            val = ui.rolling_animation("Flee roll", y=GRID_ROWS+8, x=2, rolls=5, max_val=100)
            if val <= flee_chance:
                messages.append("You successfully fled.")
                return False
            else:
                messages.append("Failed to flee.")
        else:
            messages.append("No action taken.")

        # cleanup dead enemies, check victory
        if all(e["hp"] <= 0 for e in enemies):
            messages.append("All foes defeated!")
            # reward
            loot = random.choice(area["loot"])
            player.inventory.append(loot)
            g = random.randint(8, 30)
            xp = random.randint(8, 20)
            player.gold += g
            player.exp += xp
            messages.append(f"Found {ITEMS[loot]['name']} and {g} gold (+{xp} XP)!")
            ui.draw_hud(player, messages)
            ui.refresh()
            time.sleep(2.5)
            return True

        # Enemies take turns with smarter AI
        for idx, e in enumerate(enemies):
            if e["hp"] <= 0:
                continue
            enemy_ai_move_and_act(idx, e, enemy_states[idx], player, player_pos, enemies, ui, messages)
            # if enemy attacked and player was defending, reduce damage
            if defending and messages:
                # last message likely an enemy hit (crudely), reduce last damage by half
                # (we already reduced damage when computing in AI not knowing defending state — for simplicity, we apply a textual effect)
                messages.append("Your defense absorbed some damage.")
                defending = False

        # check player death
        if player.hp <= 0:
            # clear messages and redraw HUD so the screen is clean
            messages.clear()
            ui.clear()
            ui.draw_grid(player_pos, enemies)
            ui.draw_hud(player, ["You were slain..."])
            ui.refresh()
            time.sleep(2.5)
            return None


        # loop end
        # Wizard passive: restore 1 mana per turn
        if player.passive == "arcane" and player.mana < player.magic * 2:
            player.mana += 1
            messages.append("Arcane energy restores 1 mana.")
        turn += 1
        # trim messages to avoid overflow
        if len(messages) > 40:
            messages = messages[-40:]

# -------------------- Story & Overworld art --------------------
def show_zone_ui(stdscr, ui, area):
    ui.draw_zone_art(area["art"], area["name"], area["desc"])

# -------------------- Game flow (curses main) --------------------
def shop_menu(ui, player):
    items = SHOP_ITEMS
    selection = 0
    mode = "buy"  # "buy" or "sell"

    while True:
        ui.stdscr.clear()
        ui.stdscr.addstr(1, 2, f"🏪 Shop — Mode: {mode.upper()} — Gold: {player.gold}")
        ui.stdscr.addstr(3, 2, "Press TAB to switch between BUY/SELL | Q to leave")

        if mode == "buy":
            ui.stdscr.addstr(5, 2, "Items for Sale:")
            for i, item in enumerate(items):
                line = f"{item['name']} - {item['price']} gold"
                if i == selection:
                    line = "> " + line
                ui.stdscr.addstr(6 + i, 4, line)
        else:
            ui.stdscr.addstr(5, 2, "Your Inventory:")
            inv_items = [(iid, 1) for iid in player.inventory]
            if not inv_items:
                ui.stdscr.addstr(7, 4, "(empty)")
            for i, (item_id, qty) in enumerate(inv_items):
                item = ITEMS[item_id]
                sell_price = max(1, item.get("value", 10) // 2)
                line = f"{item['name']} x{qty} - sells for {sell_price} gold"
                if i == selection:
                    line = "> " + line
                ui.stdscr.addstr(7 + i, 4, line)

        ui.stdscr.refresh()
        key = ui.stdscr.getkey().lower()

        # Exit
        if key == "q":
            break
        # Switch mode
        elif key == "\t":
            mode = "sell" if mode == "buy" else "buy"
            selection = 0
        # Move selection
        elif key in ("w", "k"):
            selection = max(0, selection - 1)
        elif key in ("s", "j"):
            if mode == "buy":
                selection = min(len(items) - 1, selection + 1)
            else:
                inv_len = len(player.inventory)
                selection = min(inv_len - 1, selection + 1) if inv_len > 0 else 0
        # Confirm action
        elif key in (" ", "\n"):
            if mode == "buy":
                chosen = items[selection]
                if player.gold >= chosen["price"]:
                    player.gold -= chosen["price"]
                    player.add_item(chosen["id"])
                    ui.display_message_with_animation(f"Bought {chosen['name']}!", y=ui.height - 3)
                else:
                    ui.display_message_with_animation("Not enough gold!", y=ui.height - 3)
            else:  # sell mode
                inv_items = [(iid, 1) for iid in player.inventory]
                if not inv_items:
                    continue
                item_id, qty = inv_items[selection]
                sell_price = max(1, ITEMS[item_id].get("value", 10) // 2)
                player.gold += sell_price
                player.remove_item(item_id)
                ui.display_message_with_animation(
                    f"Sold {ITEMS[item_id]['name']} for {sell_price} gold.",
                    y=ui.height - 3
                )
                selection = 0

def choose_class_curses(stdscr, ui):
    ui.clear()
    ui.stdscr.addstr(1, 2, "Choose a class (1 Knight, 2 Wizard, 3 Bandit): ")
    ui.stdscr.refresh()
    while True:
        k = ui.stdscr.getkey()
        if k == "1":
            return "Knight"
        if k == "2":
            return "Wizard"
        if k == "3":
            return "Bandit"
        ui.stdscr.addstr(3, 2, "Invalid choice. Press 1,2 or 3.")

def get_choice(options, ui, prompt="Choose an option:"):
    """
    Displays a simple choice list with curses and returns the chosen option.
    """
    stdscr = ui.stdscr
    curses.curs_set(0)
    selected = 0

    while True:
        ui.clear()
        stdscr.addstr(2, 2, prompt, curses.A_BOLD)
        for i, opt in enumerate(options):
            attr = curses.A_REVERSE if i == selected else curses.A_NORMAL
            stdscr.addstr(4 + i, 4, opt, attr)
        stdscr.refresh()

        key = stdscr.getch()
        if key in [curses.KEY_UP, ord("w")]:
            selected = (selected - 1) % len(options)
        elif key in [curses.KEY_DOWN, ord("s")]:
            selected = (selected + 1) % len(options)
        elif key in [ord("\n"), 10, 13]:
            return options[selected]


def main_curses(stdscr):
    ui = UI(stdscr)
    ui.clear()
    ui.stdscr.addstr(1, 2, "Welcome to Clash-Style Curses RPG!")
    ui.stdscr.addstr(3, 2, "Enter your name (press Enter for 'Champion'):")
    curses.echo()
    name = ui.stdscr.getstr(4, 2, 20).decode().strip()
    curses.noecho()
    if not name:
        name = "Champion"
    pclass = choose_class_curses(stdscr, ui)
    player = Player(name, pclass)
    # starter items
    player.inventory.extend(["small_potion", "elixir_bottle"])
    if pclass == "Wizard":
        player.inventory.append("magic_tome")
    elif pclass == "Knight":
        player.inventory.append("royal_sword")
    else:
        player.inventory.append("treasure_map")
        player.inventory.append("crown_key")
    # progression
    area_index = 0
    saw_dragons_peak = False
    while area_index < len(AREAS):
        area = AREAS[area_index]
        show_zone_ui(stdscr, ui, area)
        explored_once = False
        if area.get("id") == "dragons_peak":
            saw_dragons_peak = True
        # area loop
        while True:
            ui.clear()
            ui.draw_text_block([f"Area: {area['name']}", area["desc"], "", "Commands: e Explore  r Rest  i Inventory  s Stats  n Next  q Quit  p Shop"], 1, 2)
            ui.refresh()
            k = ui.stdscr.getkey()
            if k.lower() == "e":
                explored_once = True
                result = combat_sequence(stdscr, ui, player, area)
                if result is None:
                    # player died
                    ui.display_message_with_animation("You have been defeated. Press any key.", y=ui.height-3)
                    ui.stdscr.getch()
                    # final outcome display
                    end_msg = "Fallen Champion. Your run ends."
                    ui.display_message_with_animation(end_msg, y=ui.height-4)
                    ui.stdscr.getch()
                    return
                elif result is True:
                    # level up check
                    if player.exp >= 20 * player.level:
                        player.level += 1
                        player.max_hp += 6
                        player.hp = player.max_hp
                        player.strength += 1
                        player.agility += 1
                        player.magic += 1
                        player.mana = player.magic * 2
                        ui.display_message_with_animation(f"Level up! Now level {player.level}", y=ui.height-4)
                        ui.stdscr.getch()
                else:
                    # fled
                    pass
            elif k.lower() == "r":
                player.hp = player.max_hp
                player.mana = player.magic * 2
                ui.display_message_with_animation("You rest and fully recover your health and mana.", y=ui.height - 4)
                ui.stdscr.getch()
            elif k.lower() == "i":
                ui.clear()
                # Show equipped gear
                if player.equipment:
                    eq_weapon = player.equipment.get("weapon")
                    eq_armor = player.equipment.get("armor")
                    weapon_name = ITEMS[eq_weapon]["name"] if eq_weapon else "None"
                    armor_name = ITEMS[eq_armor]["name"] if eq_armor else "None"
                    equipped_lines = [f"Equipped Weapon: {weapon_name}", f"Equipped Armor: {armor_name}", ""]
                else:
                    equipped_lines = ["No equipment.", ""]

                inv_lines = [f"{idx+1}) {ITEMS[k]['name']}" for idx, k in enumerate(player.inventory)]
                ui.draw_text_block(["Inventory:"] + equipped_lines + inv_lines, 1, 2)
                ui.draw_text_block(
                    ["Press number to use, i + number to inspect, d + number to discard, or any other key to return."],
                    10 + len(inv_lines), 2
                )
                ui.refresh()

                ch = ui.stdscr.getkey()

                # Use item
                if ch.isdigit():
                    idx = int(ch) - 1
                    if 0 <= idx < len(player.inventory):
                        key = player.inventory.pop(idx)
                        ok, msg = player.apply_item(key)
                        ui.display_message_with_animation(msg, y=ui.height - 4)
                        ui.stdscr.getch()

                # Inspect item
                elif ch.lower() == "i":
                    ui.stdscr.addstr(11, 2, "Inspect which item number? ")
                    curses.echo()
                    s = ui.stdscr.getstr(11, 30, 2).decode()
                    curses.noecho()
                    if s.isdigit():
                        idx = int(s) - 1
                        if 0 <= idx < len(player.inventory):
                            desc = player.describe_item(player.inventory[idx])
                            ui.display_message_with_animation(desc, y=ui.height - 4)
                            ui.stdscr.getch()

                # Discard
                elif ch.lower() == "d":
                    ui.stdscr.addstr(11, 2, "Discard which item number? ")
                    curses.echo()
                    s = ui.stdscr.getstr(11, 31, 2).decode()
                    curses.noecho()
                    if s.isdigit():
                        idx = int(s) - 1
                        if 0 <= idx < len(player.inventory):
                            removed = player.inventory.pop(idx)
                            ui.display_message_with_animation(f"Discarded {ITEMS[removed]['name']}", y=ui.height - 4)
                            ui.stdscr.getch()
                            ui.clear()
                            # >>> Show equipped gear
                            equipped_lines = []
                            if player.equipment:
                                eq_weapon = player.equipment.get("weapon")
                                eq_armor = player.equipment.get("armor")
                                weapon_name = ITEMS[eq_weapon]["name"] if eq_weapon else "None"
                                armor_name = ITEMS[eq_armor]["name"] if eq_armor else "None"
                                equipped_lines = [f"Equipped Weapon: {weapon_name}", f"Equipped Armor: {armor_name}", ""]
                            else:
                                equipped_lines = ["No equipment.", ""]

                            inv_lines = [f"{idx+1}) {ITEMS[k]['name']}" for idx, k in enumerate(player.inventory)]
                            ui.draw_text_block(["Inventory:"] + equipped_lines + inv_lines, 1, 2)
                            # <<<
                            ui.draw_text_block(["Press number to use, d + number to discard, or any other key to return."], 10 + len(inv_lines), 2)
                            ui.refresh()
                            ch = ui.stdscr.getkey()
                            if ch.isdigit():
                                idx = int(ch)-1
                                if 0 <= idx < len(player.inventory):
                                    key = player.inventory.pop(idx)
                                    ok, msg = player.apply_item(key)
                                    ui.display_message_with_animation(msg, y=ui.height-4)
                                    ui.stdscr.getch()
                            elif ch.lower() == "d":
                                ui.stdscr.addstr(11, 2, "Enter index to discard: ")
                                curses.echo()
                                s = ui.stdscr.getstr(11, 26, 2).decode()
                                curses.noecho()
                                if s.isdigit():
                                    idx = int(s)-1
                                    if 0 <= idx < len(player.inventory):
                                        removed = player.inventory.pop(idx)
                                        ui.display_message_with_animation(f"Discarded {ITEMS[removed]['name']}", y=ui.height-4)
                                        ui.stdscr.getch()
            elif k.lower() == "s":
                ui.clear()
                ui.draw_text_block([player.summary_line(), f"Gold: {player.gold}  Level:{player.level}  Exp:{player.exp}"], 2, 2)
                ui.draw_text_block(["Press any key to continue..."], ui.height - 3, 2)
                ui.stdscr.getch()
            elif k.lower() == "n":
                if explored_once == True:

                    # Check if we're currently in Desert Arena
                    if area["id"] == "desert_arena":
                        # Only unlock if player has both items
                        if ("treasure_map" in player.inventory or "has_map" in player.story_flags) and ("crown_key" in player.inventory or "has_crown_key" in player.story_flags):
                            area_index = len(AREAS) - 1  # sends player to Hidden Throne
                            break

                    # Otherwise continue normally
                    if area["id"] == "hidden_throne":
                        show_throne_room_ending(ui, player)
                    if area["id"] != "dragons_peak":
                        area_index += 1
                        break
                    if area["id"] == "dragons_peak":
                        ui.display_message_with_animation("You ascend to the crimson heights of Dragon’s Peak...")
                        time.sleep(1.2)
                        ui.display_message_with_animation("Before you stands the Adult Dragon — wings vast, eyes like molten gold.")
                        time.sleep(1.2)
                        ui.display_message_with_animation("It rumbles: 'Mortal... you dare approach my roost?'")
                        time.sleep(1.0)

                        choice = get_choice(["Fight", "Spare"], ui, prompt="How will you face the dragon?")

                        player_pos = (GRID_ROWS // 2, 1)
                        dragonspeak_area = deepcopy(area)
                        dragonspeak_area["encounters"] = ["adult_dragon"]

                        if choice == "Fight":
                            ui.display_message_with_animation("You draw your weapon. The dragon rears up and unleashes a roar!")
                            time.sleep(1.0)
                            enemies = spawn_enemies(dragonspeak_area, player_pos)
                            area = AREAS[5]
                            result = combat_sequence(stdscr, ui, player, area)
                            if result is None:
                                # player died
                                ui.display_message_with_animation("You have been defeated. Press any key.", y=ui.height-3)
                                ui.stdscr.getch()
                                # final outcome display
                                end_msg = "Fallen Champion. Your run ends."
                                ui.display_message_with_animation(end_msg, y=ui.height-4)
                                ui.stdscr.getch()
                                time.sleep(1)
                                exit()
                            else:
                                show_ending_cutscene(ui, player)
                                

                        elif choice == "Spare":
                            ui.display_message_with_animation("You kneel, lowering your weapon in a gesture of peace...")
                            time.sleep(1.2)
                            ui.display_message_with_animation("The dragon’s gaze narrows, testing your resolve.")
                            time.sleep(1.0)

                            # --- Compute peaceful success chance ---
                            base_chance = 0.35
                            if player.magic >= 10:
                                base_chance += 0.25  # strong magic aura calms it
                            if "dragon_scale" in player.inventory or "dragon_scale" in player.story_flags:
                                base_chance += 0.25  # you carry the scent of dragonkind

                            # Cap at 90% max success chance
                            base_chance = min(base_chance, 0.9)

                            if random.random() < base_chance:
                                ui.display_message_with_animation("The dragon’s eyes soften. A deep rumble shakes the air — laughter.")
                                time.sleep(1.0)
                                ui.display_message_with_animation("'You show wisdom, mortal. Take this, a token of my kin.'")
                                player.story_flags.add("befriended_adult_dragon")
                                player.story_flags.add("befriended_dragon")
                                player.add_item("dragon_scale")
                                time.sleep(1.0)
                                ui.display_message_with_animation("You receive the Dragon Scale in peace.")
                                time.sleep(1.0)
                                show_spared_dragon_ending(ui, player)
                            else:
                                ui.display_message_with_animation("The dragon’s lips curl into a sneer. 'Foolish... mercy is weakness.'")
                                time.sleep(1.0)
                                ui.display_message_with_animation("You draw your weapon. The dragon rears up and unleashes a roar!")
                                time.sleep(1.0)
                                area = AREAS[5]
                                result = combat_sequence(stdscr, ui, player, area)
                                if result is None:
                                    # player died
                                    ui.display_message_with_animation("You have been defeated. Press any key.", y=ui.height-3)
                                    ui.stdscr.getch()
                                    # final outcome display
                                    end_msg = "Fallen Champion. Your run ends."
                                    ui.display_message_with_animation(end_msg, y=ui.height-4)
                                    ui.stdscr.getch()
                                    time.sleep(1)
                                    exit()
                                else:
                                    show_ending_cutscene(ui, player)
                            return
                else:
                    ui.display_message_with_animation("Explore once to progress to the next area", y=ui.height-4)
            elif k.lower() == "p":
                shop_menu(ui, player)
            elif k.lower() == "q":
                ui.display_message_with_animation("Quitting... press any key.", y=ui.height-4)
                ui.stdscr.getch()
                # final outcome quick summary
                if player.hp <= 0:
                    final = "Fallen Champion"
                elif "befriended_dragon" in player.story_flags:
                    final = "Dragon Companion"
                
                elif "slain_dragon" in player.story_flags:
                    final = "Hoard King"
                elif player.exp > 80 or player.level >= 6:
                    final = "Arena Legend"
                else:
                    final = "Wandering Champion"
                ui.display_message_with_animation(f"Ending: {final}. Thanks for playing!", y=ui.height-4)
                ui.stdscr.getch()
                return
            else:
                # ignore
                pass
    if (("has_map" in player.story_flags or "treasure_map" in player.inventory) and
        ("has_crown_key" in player.story_flags or "crown_key" in player.inventory)):
        return  # Secret path chosen, do NOT trigger dragon sequence
    # Dragon's Peak final sequence
    # Dragon's Peak final sequence - only run if player actually reached Dragon's Peak
    # Final Ending
    if player.hp <= 0:
        final = "Fallen Champion"
    elif "befriended_adult_dragon" in player.story_flags:
        final = "Elder Dragon Ally"
    elif "slain_adult_dragon" in player.story_flags:
        final = "Dragonsbane"
    elif player.exp > 80 or player.level >= 6:
        final = "Arena Legend"
    else:
        final = "Wandering Champion"

    ui.clear()
    ui.draw_text_block(["=== FINAL OUTCOME ===", f"Ending: {final}", "", "Thanks for playing!"], 2, 2)
    ui.stdscr.getch()


    if player.hp <= 0:
        final = "Fallen Champion"
    elif "true_ruler" in player.story_flags:    # <--- ADD THIS LINE
        final = "True Ruler"
    elif "befriended_dragon" in player.story_flags:
        final = "Dragon Companion"
    elif "slain_dragon" in player.story_flags and player.gold > 60:
        final = "Hoard King"
    elif player.exp > 80 or player.level >= 6:
        final = "Arena Legend"
    else:
        final = "Wandering Champion"

    ui.clear()
    ui.draw_text_block(["=== FINAL OUTCOME ===", f"Ending: {final}", "", "Thanks for playing!"], 2, 2)
    ui.stdscr.getch()

def main():
    curses.wrapper(main_curses)



def harmonize_dragon_flags(player):
    """Ensure both short and long dragon story flags are present for compatibility."""
    if "befriended_adult_dragon" in player.story_flags:
        player.story_flags.add("befriended_dragon")
    if "slain_adult_dragon" in player.story_flags:
        player.story_flags.add("slain_dragon")
if __name__ == "__main__":
    main()

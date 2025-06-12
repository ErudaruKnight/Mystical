import sqlite3
from typing import Optional, Tuple, List

DB_FILE = "rune_system.db"


def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS spells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            combo TEXT UNIQUE,
            name TEXT,
            description TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_spell(combo: str, name: str, description: str):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO spells (combo, name, description) VALUES (?, ?, ?)",
            (combo, name, description),
        )
        conn.commit()


def get_spell(combo: str) -> Optional[Tuple[str, str]]:
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT name, description FROM spells WHERE combo = ?",
            (combo,),
        )
        return cur.fetchone()


def populate_basic_spells():
    """Fill the database with a few example spells and all simple combos."""
    initialize_db()

    examples: List[Tuple[str, str, str]] = [
        (
            "water-fire-empty-earth-fire",
            "Steam Blast",
            "A burst of scalding steam damages foes.",
        ),
        (
            "fire-fire-earth-water-air",
            "Molten Cyclone",
            "Spins a fiery whirlwind mixed with stone shards.",
        ),
    ]
    for combo, name, desc in examples:
        add_spell(combo, name, desc)

    populate_all_combos()


def populate_all_combos():
    """Generate every combination of five elements and store it."""
    initialize_db()
    elements = ["empty", "fire", "water", "earth", "air"]
    count = 1
    for e1 in elements:
        for e2 in elements:
            for e3 in elements:
                for e4 in elements:
                    for e5 in elements:
                        combo = f"{e1}-{e2}-{e3}-{e4}-{e5}"
                        name = f"Spell {count}"
                        description = f"Auto generated combo {combo}."
                        add_spell(combo, name, description)
                        count += 1

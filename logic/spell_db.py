import sqlite3
from typing import Optional, Tuple, List

from .efficiency import combo_efficiency

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
            description TEXT,
            efficiency REAL
        )
        """
    )
    conn.commit()
    conn.close()


def add_spell(combo: str, name: str, description: str):
    eff = combo_efficiency(combo)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO spells (combo, name, description, efficiency) VALUES (?, ?, ?, ?)",
            (combo, name, description, eff),
        )
        conn.commit()


def get_spell(combo: str) -> Optional[Tuple[str, str, float]]:
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT name, description, efficiency FROM spells WHERE combo = ?",
            (combo,),
        )
        row = cur.fetchone()
        return row if row else None


def populate_basic_spells():
    """Fill the database with auto-generated spell combinations."""
    initialize_db()
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
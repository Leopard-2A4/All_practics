import logging
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

import requests

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

DB_NAME = 'starwars.db'


def init_db() -> None:
    """Инициализация БД."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()


def fetch_character(character_id: int) -> Dict[str, Any]:
    """Загрузка одного персонажа."""
    url = f"https://swapi.dev/api/people/{character_id}/"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            'id': character_id,
            'name': data['name'],
            'age': data['birth_year'],
            'gender': data['gender']
        }
    except Exception as e:
        logger.error(f"Error fetching {character_id}: {e}")
        return None


def sequential_download() -> List[Dict[str, Any]]:
    """Последовательная загрузка 20 персонажей."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    start_time = time.time()
    characters = []

    for i in range(1, 21):
        char = fetch_character(i)
        if char:
            cursor.execute(
                "INSERT OR REPLACE INTO characters (id, name, age, gender) VALUES (?, ?, ?, ?)",
                (char['id'], char['name'], char['age'], char['gender'])
            )
            characters.append(char)

    conn.commit()
    conn.close()
    end_time = time.time()

    logger.info(f"Sequential: {len(characters)} chars, {end_time - start_time:.2f}s")
    return characters


def threaded_download() -> List[Dict[str, Any]]:
    """Многопоточная загрузка с потоками."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    start_time = time.time()
    characters = []

    def save_char(char: Dict[str, Any]):
        if char:
            cursor.execute(
                "INSERT OR REPLACE INTO characters (id, name, age, gender) VALUES (?, ?, ?, ?)",
                (char['id'], char['name'], char['age'], char['gender'])
            )
            characters.append(char)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_character, i) for i in range(1, 21)]
        for future in futures:
            save_char(future.result())

    conn.commit()
    conn.close()
    end_time = time.time()

    logger.info(f"Threaded: {len(characters)} chars, {end_time - start_time:.2f}s")
    return characters


def compare_performance():
    """Тестирование производительности."""
    logger.info("=== Sequential ===")
    seq_time = time.time()
    seq_chars = sequential_download()
    seq_time = time.time() - seq_time

    logger.info("=== Threaded ===")
    thr_time = time.time()
    thr_chars = threaded_download()
    thr_time = time.time() - thr_time

    logger.info(f"Sequential: {seq_time:.2f}s ({len(seq_chars)} chars)")
    logger.info(f"Threaded: {thr_time:.2f}s ({len(thr_chars)} chars)")
    logger.info(f"Speedup: {seq_time / thr_time:.1f}x")


if __name__ == "__main__":
    compare_performance()

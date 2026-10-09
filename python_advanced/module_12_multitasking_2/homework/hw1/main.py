import sqlite3
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import Dict, Any
import logging

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

DB_PATH = '/home/artem/PycharmProjects/python_advanced/module_11_multitasking/homework/hw2/starwars.db'


def init_db():
    """Инициализация/проверка БД."""
    conn = sqlite3.connect(DB_PATH)
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


def fetch_character(args: tuple) -> Dict[str, Any]:
    """Загрузка персонажа (id, db_path)."""
    char_id, db_path = args
    url = f"https://swapi.dev/api/people/{char_id}/"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # Сохраняем сразу в БД
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO characters (id, name, age, gender) VALUES (?, ?, ?, ?)",
            (char_id, data['name'], data['birth_year'], data['gender'])
        )
        conn.commit()
        conn.close()
        logger.info(f"Loaded char {char_id}: {data['name']}")
        return {'id': char_id, 'name': data['name']}
    except Exception as e:
        logger.error(f"Failed {char_id}: {e}")
        return None


def threadpool_download():
    """ThreadPoolExecutor (I/O-bound оптимально)."""
    init_db()
    start_time = time.time()

    tasks = [(i, DB_PATH) for i in range(1, 21)]
    results = []

    with ThreadPoolExecutor(max_workers=20) as executor:  # Много потоков для I/O
        futures = [executor.submit(fetch_character, task) for task in tasks]
        results = [f.result() for f in futures]

    elapsed = time.time() - start_time
    success = len([r for r in results if r])
    logger.info(f"ThreadPool: {success}/20 chars, {elapsed:.2f}s")
    return success


def processpool_download():
    """multiprocessing.Pool."""
    init_db()
    start_time = time.time()

    tasks = [(i, DB_PATH) for i in range(1, 21)]
    results = []

    with Pool(processes=8) as pool:  # По ядрам + немного
        results = pool.map(fetch_character, tasks)

    elapsed = time.time() - start_time
    success = len([r for r in results if r])
    logger.info(f"ProcessPool: {success}/20 chars, {elapsed:.2f}s")
    return success


def compare_performance():
    """Сравнение."""
    logger.info("=== ThreadPoolExecutor ===")
    thread_success = threadpool_download()

    logger.info("=== ProcessPool ===")
    proc_success = processpool_download()

    logger.info(f"\n{'=' * 50}")
    logger.info(f"Threads:  {thread_success}/20 chars")
    logger.info(f"Process:  {proc_success}/20 chars")
    logger.info(f"Threads быстрее для I/O (GIL не мешает)!")


def check_db():
    """Проверка финальной БД."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM characters")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT id, name FROM characters ORDER BY id LIMIT 5")
    sample = cursor.fetchall()
    conn.close()
    logger.info(f"БД: {total} записей. Пример: {sample}")


if __name__ == "__main__":
    compare_performance()
    check_db()
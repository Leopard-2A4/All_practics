import threading
import queue
import time
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOG_FILE = 'logs.txt'
q = queue.Queue()
stop_event = threading.Event()
done_count = 0
lock = threading.Lock()


class LogEntry:
    def __init__(self, timestamp: float, thread_id: int, date_str: str):
        self.timestamp = timestamp
        self.thread_id = thread_id
        self.date_str = date_str

    def __lt__(self, other):
        return self.timestamp < other.timestamp


def get_date_from_api(current_ts: float) -> str:
    """Получаем дату для текущего ts."""
    try:
        url = f"http://127.0.0.1:8080/timestamp/{int(current_ts)}"
        resp = requests.get(url, timeout=2)
        resp.raise_for_status()
        return resp.text.strip()
    except Exception as e:
        logger.error(f"API error: {e}")
        return datetime.fromtimestamp(current_ts).strftime('%Y-%m-%d %H:%M:%S')


def worker(thread_id: int):
    global done_count
    logger.info(f"Thread-{thread_id} started")
    for i in range(20):
        ts = time.time()  # Текущий ts ПЕРЕД запросом!
        date_str = get_date_from_api(ts)
        log = LogEntry(ts, thread_id, date_str)
        q.put(log)
        time.sleep(1)
    with lock:
        done_count += 1
    logger.info(f"Thread-{thread_id} finished")


def log_writer():
    logs = []
    none_count = 0
    while none_count < 10 or not q.empty():  # Ждем 10 сигналов завершения
        try:
            item = q.get(timeout=1)
            if item is None:
                none_count += 1
                continue
            logs.append(item)
        except queue.Empty:
            continue

    logs.sort(key=lambda x: x.timestamp)
    with open(LOG_FILE, 'w') as f:
        for log in logs:
            f.write(f"{log.timestamp} {log.date_str}\n")  # Формат <timestamp> <дата>

    logger.info(f"Wrote {len(logs)} sorted logs to {LOG_FILE}")


def main():
    writer = threading.Thread(target=log_writer)  # Не daemon
    writer.start()

    threads = []
    for i in range(10):
        time.sleep(1)
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    for _ in range(10):
        q.put(None)

    stop_event.set()
    writer.join(timeout=5)
    logger.info("All done!")


if __name__ == "__main__":
    main()
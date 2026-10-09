from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests

URL = "https://cataas.com/cat"
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / "cats/thread_cats"
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


def write_to_disk(idx: int) -> bytes:
    response = requests.get(URL)
    content = response.content
    file_path = OUT_PATH / f"{idx}.png"
    with open(file_path, "wb") as f:
        f.write(content)
    return content


def get_all_cats():
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [executor.submit(write_to_disk, i) for i in range(CATS_WE_WANT)]
        return [task.result() for task in tasks]


def thread_main():
    res = get_all_cats()
    return res
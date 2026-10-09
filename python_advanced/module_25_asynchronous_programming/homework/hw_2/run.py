from async_cats import async_main
from thread_cats import thread_main
from process_cat import process_main
from pathlib import Path
import time

OUT_PATH = Path(__file__).parent / "Results_of_runners/results_3.txt"
OUT_PATH.parent.mkdir(exist_ok=True, parents=True)

def main():
    start = time.time()
    result = async_main()
    end = time.time()
    line = f"Downloaded {len(result)} by async in {end - start:.3f} s.\n"
    print(line, end="")
    return line

def main_2():
    start = time.time()
    result = thread_main()
    end = time.time()
    line = f"Downloaded {len(result)} by threads in {end - start:.3f} s.\n"
    print(line, end="")
    return line

def main_3():
    start = time.time()
    result = process_main()
    end = time.time()
    line = f"Downloaded {len(result)} by processes in {end - start:.3f} s.\n"
    print(line, end="")
    return line

def runner():
    return main_3() + main_2() + main()

if __name__ == '__main__':
    file_of_result = OUT_PATH
    with open(file_of_result, mode='a', encoding="utf-8") as f:

         f.write(runner())
         f.write("[==----------------------------------==]\n")

import subprocess
import os


def process_count(username: str) -> int:
    """Количество процессов пользователя (pgrep -u + wc)."""
    try:
        result = subprocess.run(['pgrep', '-cu', username],
                                capture_output=True, text=True, check=False)
        count = int(result.stdout.strip())
        return count
    except Exception:
        return 0


def total_memory_usage(root_pid: int) -> float:
    """
    Суммарное %MEM древа процессов с корнем root_pid.
    ps -o %mem --ppid PID --no-headers | awk '{sum+=$1} END {print sum}'
    Рекурсивно по --ppid.
    """
    try:
        cmd = ['ps', '-o', '%mem', f'--ppid={root_pid}', '--no-headers']
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0 or not result.stdout.strip():
            return 0.0

        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        total_mem = sum(float(line) for line in lines)
        return round(total_mem, 2)

    except Exception:
        return 0.0


def demo():
    """Демо функций."""
    username = os.getlogin()
    count = process_count(username)
    print(f"Процессов user '{username}': {count}")

    my_pid = os.getpid()
    my_mem = total_memory_usage(my_pid)
    print(f"Память моего древа PID {my_pid}: {my_mem}%")

    systemd_mem = total_memory_usage(1)
    print(f"Память systemd (PID 1): {systemd_mem}%")


if __name__ == "__main__":
    demo()
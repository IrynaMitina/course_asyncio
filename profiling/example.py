"""run it with:
% scalene run --cli example.py
"""
import asyncio


def cpu_heavy(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


def memory_heavy(n: int) -> list[int]:
    data = []
    for i in range(n):
        data.append(i)
    return data


async def main():
    # CPU-bound work (offloaded to a thread so the loop stays responsive)
    await asyncio.to_thread(cpu_heavy, 10_000_000)

    # Async "idle" time (non-CPU)
    await asyncio.sleep(1)

    # Memory-heavy allocation (also offloaded; otherwise it blocks the loop)
    await asyncio.to_thread(memory_heavy, 5_000_000)


if __name__ == "__main__":
    asyncio.run(main())

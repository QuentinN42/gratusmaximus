import time


def fib(n: int) -> int:
    if n <= 1:
        return n
    else:
        return fib(n - 2) + fib(n - 1)


def speedtest(n: int) -> None:
    print(f"Testing speed of fibo for {n=}")
    t0 = time.time()
    res = fib(32)
    print(f"Took {time.time() - t0}s")
    print(f"{res=}")

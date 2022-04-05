from time import sleep
from typing import List

from pprof import cpu


cpu.auto_report()


def foo():
    sleep(1.01)
    return 3


@cpu
def run(arr: List) -> float:
    tmp = []
    cnt = foo()

    # comment action #1
    for row in arr:
        # comment action #2 row 1
        # comment action #2 row 2
        if row % cnt == 0:
            tmp.append(row)
    result = (sum(tmp * 200) + len(arr)) / len(tmp)  # comment action #3
    return result


run(list(range(250000)))

<p align="center">
  <a href="https://github.com/mirecl/pprof"><img src="https://github.com/mirecl/pprof/blob/master/examples/report.png?raw=true" alt="pprof"></a>
</p>

<p align="center">
    <a href="https://pypi.org/project/pprof" target="_blank">
        <img src="https://img.shields.io/pypi/v/pprof" alt="PyPi">
    </a>
    <a href="https://pepy.tech/project/pprof" target="_blank">
        <img src="https://pepy.tech/badge/pprof" alt="PePy">
    </a>
    <a href="https://github.com/psf/black" target="_blank">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
    </a>
    <a href="https://github.com/mirecl/pprof/blob/master/LICENSE" target="_blank">
        <img src="https://img.shields.io/pypi/l/pprof" alt="License">
    </a>
    <a href="https://github.com/mirecl/pprof/actions/workflows/test.yaml" target="_blank">
        <img src="https://github.com/mirecl/pprof/actions/workflows/test.yaml/badge.svg" alt="Test">
    </a>
    <a href="https://codecov.io/gh/mirecl/pprof" target="_blank">
        <img src="https://codecov.io/gh/mirecl/pprof/branch/master/graph/badge.svg?token=UFDA1JG40A" alt="Test">
    </a>
    <br>
    <a href="https://pypi.org/project/pprof/" target="_blank">
        <img src="https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue?logoColor=white&logo=python" alt="PyPi">
    </a>
    <a href="https://github.com/mirecl/pprof" target="_blank">
        <img src="https://img.shields.io/badge/OS-win%20%7C%20mac%20%7C%20linux-green" alt="OS">
    </a>
</p>


---

## Installing

```sh
pip install pprof
```

or

```sh
poetry add pprof
```

## A Simple Example

```python
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
```

```sh
(venv) python run.py
```

## Links

+ **line_profiler** (<https://github.com/pyutils/line_profiler>)

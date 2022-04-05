<p align="center">
  <a href="https://github.com/mirecl/pprof"><img src="https://github.com/mirecl/pprof/blob/master/examples/report.png?raw=true" alt="pprof"></a>
</p>

[![PyPI](https://img.shields.io/pypi/v/pprof)](https://pypi.org/project/pprof/)
[![Downloads](https://pepy.tech/badge/pprof)](https://pepy.tech/project/pprof)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - License](https://img.shields.io/pypi/l/pprof)](https://github.com/mirecl/pprof/blob/master/LICENSE)
[![Tests](https://github.com/mirecl/pprof/actions/workflows/tests.yaml/badge.svg)](https://github.com/mirecl/pprof/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/mirecl/pprof/branch/master/graph/badge.svg?token=UFDA1JG40A)](https://codecov.io/gh/mirecl/pprof)
[![python version](https://img.shields.io/pypi/pyversions/pprof.svg)](https://pypi.org/project/pprof/)

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

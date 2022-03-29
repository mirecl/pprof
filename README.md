<p align="center">
  <a href="https://github.com/mirecl/pprof"><img src="https://github.com/mirecl/pprof/blob/master/examples/report.png?raw=true" alt="pprof"></a>
</p>

[![Downloads](https://pepy.tech/badge/pprof)](https://pepy.tech/project/pprof)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
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
from typing import List
from pprof import cpu

cpu.auto_report()

@cpu
def run(arr: List) -> float:
    tmp = []
    for row in arr:
        if row % 3 == 0:
            tmp.append(row)
    result = (sum(tmp*100) + len(arr)) / len(tmp)
    return result

run(list(range(100000)))
```

```sh
(venv) python run.py
```

## Links

+ **line_profiler** (<https://github.com/pyutils/line_profiler>)

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

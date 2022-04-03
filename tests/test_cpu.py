import atexit
import os.path
import webbrowser

from tempfile import gettempdir

import pytest

from pprof.cpu import CPUProfiler


empty_report = '<html><head><meta charset="UTF-8"/></head><pre>Timer unit: 0.001 s\n\n</pre></html>'


def f(a, b):
    return a + b


def g(a, b):
    yield f(a, b)


async def c(a, b):
    return f(a, b)


@pytest.mark.asyncio
async def test_run(mocker):
    profiler = CPUProfiler()

    report = profiler.get_report()
    assert report == empty_report

    mocker.patch.object(atexit, "register", lambda x: x)
    profiler.auto_report()

    mocker.patch.object(webbrowser, "open", lambda x: x)
    profiler.open_report()
    path = f"{gettempdir()}/cpu_profile.html"
    assert os.path.exists(path) == True

    wrapper_f = profiler(f)
    wrapper_g = profiler(g)
    wrapper_c = profiler(c)

    report = profiler.get_report()
    assert report != empty_report

    assert len(profiler.functions) == 3

    excepted = f(1, 2)

    assert wrapper_f(1, 2) == excepted
    assert next(wrapper_g(1, 2)) == excepted

    n = await wrapper_c(1, 2)
    assert n == excepted

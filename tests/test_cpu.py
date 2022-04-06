import atexit
import os.path
import webbrowser

from tempfile import gettempdir

import pytest

from pprof import cpu
from pprof.cpu import show_html


empty_report = '<html><head><meta charset="UTF-8"/></head></html>'


def f(a, b):
    # fake func
    res = a + b
    return res


@pytest.mark.run(order=2)
def test_cpu(mocker):
    report = cpu.get_report()
    assert report == empty_report

    mocker.patch.object(atexit, "register", lambda x: x)
    cpu.auto_report()

    mocker.patch.object(webbrowser, "open", lambda x: x)
    cpu.open_report()
    path = f"{gettempdir()}/cpu_profile.html"
    assert os.path.exists(path) is True

    wrapper_f = cpu(f)
    assert wrapper_f(1, 1) == 2


@pytest.mark.run(order=1)
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([(18, 1, 0), (19, 1, 300_000)], "300.0ms"),
        ([(18, 1, 0), (19, 1, 0)], "."),
        ([(18, 1, 1_000_001), (19, 1, 0)], "1.00s"),
    ],
)
def test_show_html(test_input, expected):
    report = show_html({(__file__, 16, "f"): test_input})
    assert report.__contains__(expected) is True

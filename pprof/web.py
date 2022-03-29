import webbrowser

from functools import partial
from io import StringIO
from tempfile import gettempdir

from line_profiler import LineProfiler


class WebRender:
    def __init__(self, profiler: LineProfiler.print_stats):
        self.profiler = partial(profiler, output_unit=0.001, stripzeros=False)

    def _get_content(self) -> str:
        stream = StringIO()
        self.profiler(stream)
        return stream.getvalue()

    def render(self) -> None:
        path = f"{gettempdir()}/cpu_profile.html"

        with open(path, "w") as f:
            html = self.get_html()
            f.write(html)

        webbrowser.open(f"file://{path}")

    def get_html(self) -> str:
        content = self._get_content()
        return f'<html><head><meta charset="UTF-8"/></head><pre>{content}</pre></html>'

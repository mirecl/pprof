import atexit

from line_profiler import LineProfiler

from .web import WebRender


class CPUProfiler(LineProfiler):
    def __init__(self):
        super(LineProfiler, self).__init__()
        self.stream = WebRender(self.print_stats)

    def auto_report(self) -> None:
        """
        Auto open web report in browser after execute script.
        """

        atexit.register(self.open_report)

    def open_report(self) -> None:
        """
        Open web report in browser.
        """
        self.stream.render()

    def get_report(self) -> str:
        """
        Get source html for web report.
        """
        return self.stream.get_html()


cpu = CPUProfiler()

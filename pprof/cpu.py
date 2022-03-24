import atexit

from functools import wraps
from inspect import iscoroutinefunction

from line_profiler import LineProfiler
from line_profiler.line_profiler import is_generator

from .web import WebRender


is_coroutine = iscoroutinefunction


class CPUProfiler(LineProfiler):
    def __init__(self):
        super(LineProfiler, self).__init__()
        self.stream = WebRender(self.print_stats)

    def __call__(self, func):
        """
        Decorate a function to start the profiler on function entry and stop
        it on function exit.
        """
        self.add_function(func)
        if is_coroutine(func):
            wrapper = self.wrap_coroutine(func)
        elif is_generator(func):
            wrapper = self.wrap_generator(func)
        else:
            wrapper = self.wrap_function(func)
        return wrapper

    def wrap_coroutine(self, func):
        """
        Wrap a Python coroutine to profile it (support async func).
        """

        @wraps(func)
        async def wrapper(*args, **kwds):
            self.enable_by_count()
            try:
                result = await func(*args, **kwds)
            finally:
                self.disable_by_count()
            return result

        return wrapper

    def auto_report(self) -> None:
        """
        Auto open web report in browser after execute script.
        """

        @atexit.register
        def handler():
            self.open_report()

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

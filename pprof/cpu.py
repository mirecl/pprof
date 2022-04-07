import atexit
import inspect
import linecache
import os
import tokenize
import webbrowser

from io import StringIO
from tempfile import gettempdir

from line_profiler import LineProfiler


class CPUProfiler(LineProfiler):
    def auto_report(self) -> None:
        """
        Auto open web report in browser after execute script.
        """

        atexit.register(self.open_report)

    def open_report(self) -> None:
        """
        Open web report in browser.
        """
        path = f"{gettempdir()}/cpu_profile.html"

        with open(path, "w") as f:
            html = self.get_report()
            f.write(html)

        webbrowser.open(f"file://{path}")

    def get_report(self) -> str:
        """
        Get source html for web report.
        """
        stats = self.get_stats()
        return show_html(stats.timings)


def show_html(stats) -> str:
    """
    Generate html for web report with all functions.
    """
    report = StringIO()
    report.write('<html><head><meta charset="UTF-8"/></head>')

    func = []

    for (fn, lineno, name), timings in sorted(stats.items()):
        data = show_func(fn, lineno, name, timings)
        func.append(data)

    for content in func:
        report.write(f"<pre>{content}</pre>")

    report.write("</html>")

    return report.getvalue()


def show_func(filename, start_lineno, func_name, timings) -> str:
    """
    Generate html for funcrion.
    """
    stream = StringIO()

    scalar = 0.001

    template = "%6s %9s %12s %12s %9s    %-s"
    d = {}
    total_time = 0.0
    linenos = []

    for lineno, _, time in timings:
        total_time += time
        linenos.append(lineno)

    stream.write(f"Total time: {total_time / 1_000_000:.3f}s\n")

    stream.write(f"File: {filename}\n")
    stream.write(f"Function: {func_name} at line {start_lineno}\n")
    if os.path.exists(filename):
        # Clear the cache to ensure that we get up-to-date results.
        linecache.clearcache()
    all_lines = linecache.getlines(filename)
    sublines = inspect.getblock(all_lines[start_lineno - 1 :])

    # style for comment in source code.
    for toktype, tok, start, _, _ in tokenize.generate_tokens(StringIO("".join(sublines)).readline):
        if toktype == tokenize.COMMENT:
            source_line = start[0] - 1
            sublines[source_line] = sublines[source_line].replace(tok, f'<a style="color:#b9b9b9">{tok}</a>')

    for lineno, nhits, time in timings:
        if total_time == 0:  # Happens rarely on empty function
            percent = ""
        else:
            p = 100 * time / total_time
            percent = f"{p:5.1f}%"
            if p > 10:
                percent = f'<a style="color:#B85450">{p:8.1f}%</a>'

        time_line = time * scalar

        if time_line > 1000:
            t = "%5.2fs" % (time_line / 1000)
        else:
            t = "%5.1fms" % time_line

        per_hit_line = float(time) * scalar / nhits

        if per_hit_line > 1000:
            p = "%5.2fs" % (per_hit_line / 1000)
        else:
            p = "%5.1fms" % per_hit_line

        d[lineno] = (nhits, t, p, percent)

    linenos = range(start_lineno, start_lineno + len(sublines))
    empty = ("", "", "", "")
    header = template % ("Line #", "Hits", "Time", "Per Hit", "% Time", "Line Contents")
    stream.write("\n")
    stream.write(header)
    stream.write("\n")
    stream.write("=" * len(header))
    stream.write("\n")

    for lineno, line in zip(linenos, sublines):
        nhits, time, per_hit, percent = d.get(lineno, empty)
        if time.strip() == "0.0ms":
            time = "."

        if per_hit.strip() == "0.0ms":
            per_hit = "."

        if percent.strip() == "0.0%":
            percent = "."

        txt = template % (lineno, nhits, time, per_hit, percent, line.rstrip("\n").rstrip("\r"))
        stream.write(txt)
        stream.write("\n")
    stream.write("\n")
    return stream.getvalue()


cpu = CPUProfiler()

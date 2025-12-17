import runpy
import pathlib
import sys

assert sys.version_info >= (3, 12), "Python 3.12+ required"

if __name__ == "__main__":
    runpy.run_path(
        str(pathlib.Path(__file__).resolve().parents[1] / "src/bot/bot.py"),
        run_name="__main__",
    )

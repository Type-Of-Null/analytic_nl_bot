import runpy
import pathlib

if __name__ == "__main__":
    runpy.run_path(
        str(pathlib.Path(__file__).resolve().parents[1] / "src/bot/bot.py"),
        run_name="__main__",
    )

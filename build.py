import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

print("Building Qt resources...")

subprocess.run([
    "pyside6-rcc",
    str(ROOT / "qml/resources.qrc"),
    "-o",
    str(ROOT / "qml/resources_rc.py")
], check=True)


print("Done.")

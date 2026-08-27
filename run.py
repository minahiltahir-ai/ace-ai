import subprocess
import sys
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parent

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/ui/main.py",
        ],
        cwd=project_root,
        check=True,
    )


if __name__ == "__main__":
    main()
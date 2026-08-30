import subprocess
import sys


def main() -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/ui/main.py",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
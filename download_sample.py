"""Download a small CC0 traffic video for local testing.

Run from the repository root:
    python download_sample.py
"""

from pathlib import Path
from urllib.request import Request, urlopen

SAMPLE_URL = (
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
    "Temporary_traffic_signal_at_Colonel_By_Drive.webm"
)
OUTPUT = Path("traffic_sample.webm")


def main() -> None:
    if OUTPUT.exists() and OUTPUT.stat().st_size > 0:
        print(f"Sample video already exists: {OUTPUT}")
        return

    print("Downloading CC0 sample traffic video...")
    request = Request(SAMPLE_URL, headers={"User-Agent": "YOLO-Vahan-Saarthi/1.0"})
    with urlopen(request, timeout=60) as response, OUTPUT.open("wb") as file:
        while chunk := response.read(1024 * 1024):
            file.write(chunk)

    print(f"Downloaded: {OUTPUT}")
    print("Run: python src\\tracking_counting.py --source traffic_sample.webm")


if __name__ == "__main__":
    main()

"""Download NBA game results from the balldontlie API (free tier) into local raw files.

Usage (the API key is read from the environment and never written to disk):

    read -s "BALLDONTLIE_API_KEY?API key: "; echo
    export BALLDONTLIE_API_KEY
    python3 scripts/ingest_balldontlie_games.py --seasons 2020 2021 2022 2023 2024 2025
    unset BALLDONTLIE_API_KEY

Season numbers follow the API convention: 2024 means the 2024-25 season.

Design notes:
- Standard library only, so no new dependencies are added to the project.
- Respects the free-tier limit of 5 requests per minute.
- Writes one JSON file per page under data/raw/balldontlie/ (ignored by Git).
- Each season is written to its own folder and is re-downloaded only when
  --force is passed, so an interrupted run can be restarted safely.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_URL = "https://api.balldontlie.io/nba/v1/games"
PER_PAGE = 100
MIN_INTERVAL_SECONDS = 13.0  # 5 requests per minute on the free tier, with a margin
MAX_RETRIES = 3
DEFAULT_OUTPUT = Path("data/raw/balldontlie")


_last_request_at: float = 0.0


def _respect_rate_limit() -> None:
    """Wait until MIN_INTERVAL_SECONDS have passed since the previous request."""
    global _last_request_at
    elapsed = time.monotonic() - _last_request_at
    if _last_request_at and elapsed < MIN_INTERVAL_SECONDS:
        time.sleep(MIN_INTERVAL_SECONDS - elapsed)
    _last_request_at = time.monotonic()


def fetch_page(api_key: str, season: int, cursor: int | None) -> dict:
    """Return one page of games for a season, retrying on rate limits and server errors."""
    params = [("seasons[]", str(season)), ("per_page", str(PER_PAGE))]
    if cursor is not None:
        params.append(("cursor", str(cursor)))
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"Authorization": api_key})

    for attempt in range(1, MAX_RETRIES + 1):
        _respect_rate_limit()
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code in (401, 403):
                sys.exit(
                    f"HTTP {error.code}: the API key was rejected or this endpoint is not "
                    "included in your plan. Check the key and the plan limits."
                )
            if error.code == 429 or error.code >= 500:
                wait = float(error.headers.get("Retry-After", 30))
                print(f"  HTTP {error.code}, waiting {wait:.0f}s (attempt {attempt}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            sys.exit(f"HTTP {error.code} for season {season}: {error.reason}")
        except urllib.error.URLError as error:
            print(f"  network error ({error.reason}), attempt {attempt}/{MAX_RETRIES}")
            time.sleep(10)
    sys.exit(f"Giving up on season {season} after {MAX_RETRIES} attempts.")


def download_season(api_key: str, season: int, output_dir: Path, force: bool) -> int:
    """Download every page for one season. Returns the number of games written."""
    season_dir = output_dir / f"season_{season}"
    manifest_path = season_dir / "manifest.json"

    if manifest_path.exists() and not force:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"Season {season}: already downloaded ({manifest['games']} games), skipping.")
        return manifest["games"]

    season_dir.mkdir(parents=True, exist_ok=True)
    for old_page in season_dir.glob("page_*.json"):
        old_page.unlink()

    cursor = None
    page_number = 0
    total_games = 0
    while True:
        page = fetch_page(api_key, season, cursor)
        page_number += 1
        games = page.get("data", [])
        total_games += len(games)

        page_path = season_dir / f"page_{page_number:03d}.json"
        page_path.write_text(json.dumps(page, ensure_ascii=False), encoding="utf-8")
        print(f"Season {season}: page {page_number}, {len(games)} games (total {total_games})")

        next_cursor = (page.get("meta") or {}).get("next_cursor")
        if next_cursor is None or not games:
            break
        if next_cursor == cursor:
            sys.exit(f"Season {season}: the API returned the same cursor twice; stopping to avoid a loop.")
        cursor = next_cursor

    manifest = {"season": season, "pages": page_number, "games": total_games}
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return total_games


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seasons", nargs="+", type=int, required=True, help="season start years, e.g. 2021 2022")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="output folder (default: data/raw/balldontlie)")
    parser.add_argument("--force", action="store_true", help="download again even if a season already exists")
    args = parser.parse_args()

    api_key = os.environ.get("BALLDONTLIE_API_KEY", "").strip()
    if not api_key:
        sys.exit("BALLDONTLIE_API_KEY is not set. See the usage notes at the top of this script.")

    args.output.mkdir(parents=True, exist_ok=True)
    grand_total = 0
    for season in args.seasons:
        grand_total += download_season(api_key, season, args.output, args.force)
    print(f"Done. {grand_total} games written under {args.output}.")


if __name__ == "__main__":
    main()

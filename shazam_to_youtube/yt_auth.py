#!/usr/bin/env python
"""
Run the "ytmusicapi oauth" login.
"""
import argparse
from pathlib import Path

from ytmusicapi.setup import setup_oauth

default_oauth_path = Path.home() / ".ytmusicapi" / "oauth.json"


def run_setup_oauth(oauth_path=default_oauth_path):
    oauth_path = oauth_path.resolve()
    oauth_path.parent.mkdir(parents=True, exist_ok=True)

    setup_oauth(filepath=str(oauth_path), open_browser=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup ytmusicapi.")
    parser.add_argument(
        "--file",
        type=Path,
        default=default_oauth_path,
        help="Path for Youtube oauth token",
    )
    args = parser.parse_args()
    run_setup_oauth(args.file)

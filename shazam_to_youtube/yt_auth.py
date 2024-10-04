#!/usr/bin/env python
"""
Run the "ytmusicapi oauth" login.
"""
import sys

from ytmusicapi.setup import main as yt_auth_main


def run_main():
    sys.argv = ["ytmusicapi", "oauth"]
    sys.exit(yt_auth_main())


if __name__ == "__main__":
    run_main()

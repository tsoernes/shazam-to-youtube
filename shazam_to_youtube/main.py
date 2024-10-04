#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from spotify2ytmusic import backend
from ytmusicapi.setup import main as yt_auth_main

# Download CSV at https://www.shazam.com/myshazam
base_dir = Path.home() / "Downloads"
default_shazam_csv_path = base_dir / "shazamlibrary.csv"


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        help="Shazam playlist CSV path",
        default=default_shazam_csv_path,
    )
    parser.add_argument(
        "--ytmusic_playlist_id",
        type=str,
        help="ID of the YTMusic playlist to copy to. If this argument starts with a '+', it is asumed to be the playlist title rather than playlist ID, and if a playlist of that name is not found, it will be created (without the +).  Example: '+My Favorite Blues'. NOTE: The shell will require you to quote the name if it contains spaces.",
        default="+Shazam Playlist",
    )
    parser.add_argument(
        "--track-sleep",
        type=float,
        default=0.1,
        help="Time to sleep between each track that is added (default: 0.1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not add songs to destination playlist (default: False)",
    )
    parser.add_argument(
        "--algo",
        type=int,
        default=0,
        help="Algorithm to use for search (0 = exact, 1 = extended, 2 = approximate)",
    )
    parser.add_argument(
        "--privacy_status",
        default="PRIVATE",
        help="The privacy seting of created playlists (PRIVATE, PUBLIC, UNLISTED, default PRIVATE)",
        choices=["PRIVATE", "PUBLIC", "UNLISTED", "PRIVATE"],
    )

    return vars(parser.parse_args())


def main(
    path: Path,
    ytmusic_playlist_id="+Shazam Playlist",
    track_sleep=0.5,
    dry_run=False,
    algo=0,
    spotify_playlists_encoding="utf-8",
    reverse_playlist=False,
    privacy_status="PRIVATE",
):
    if not path.exists():
        raise FileNotFoundError(path)
    oauth_path = Path().cwd() / "oath.json"
    if not oauth_path.exists():
        sys.argv = ["ytmusicapi", "oauth"]
        yt_auth_main()

    df = pd.read_csv(path, skiprows=1)
    df.drop_duplicates("TrackKey", inplace=True)

    df = df[["Artist", "Title"]]
    df.columns = "artists", "name"
    df["artists"] = df["artists"].map(lambda s: [{"name": s}])
    df["album"] = df["artists"].map(lambda s: {"name": "", "artists": [s]})

    SHAZAM_PLAYLIST_ID = "SHAZAM_PLAYLIST_ID"

    playlists = {
        "playlists": [
            {
                "name": "shazam",
                "description": "shazam playlist",
                "id": SHAZAM_PLAYLIST_ID,
                "tracks": [
                    {
                        # This is how spotify2music expects the json to look like
                        "track": {
                            "artists": [{"name": "ARTIST1"}],
                            "album": {
                                "name": "ALBUM1",
                                "artists": [{"name": "ALBUM_ARTIST1"}],
                            },
                            "name": "TRACK_NAME",
                        }
                    }
                ],
            }
        ]
    }

    tracks = df.to_dict(orient="records")
    tracks = [{"track": t} for t in tracks]
    playlists["playlists"][0]["tracks"] = tracks

    backend.load_playlists_json = lambda x, y: playlists

    backend.copy_playlist(
        spotify_playlist_id=SHAZAM_PLAYLIST_ID,
        ytmusic_playlist_id=ytmusic_playlist_id,
        track_sleep=track_sleep,
        dry_run=dry_run,
        spotify_playlists_encoding="utf-8",
        reverse_playlist=reverse_playlist,
        privacy_status=privacy_status,
        yt_search_algo=algo,
    )


def run_main():
    main(**parse_arguments())


if __name__ == "__main__":
    run_main()

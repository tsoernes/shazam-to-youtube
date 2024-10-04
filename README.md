# shazam-to-youtube
## Create a Youtube Playlist from Shazam hits
### Installation
1. Clone repo
2. `poetry install`
3. Download Shazam playlist CSV at [https://www.shazam.com/myshazam](https://www.shazam.com/myshazam)
4. Log in to youtube: `python yt_auth.py`
4. Copy shazam playlist to youtube: `python main.py --path <PATH_TO_SHAZAM_CSV>`

### Help
Run `python main.py --help`
or open a issue

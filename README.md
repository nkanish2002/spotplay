# Spotify Playlist Creator (spotplay):notes:

Welcome to spotify playlist creator, your destination for generating random playlists for upto :100: songs.

## Installation

* Clone/download this repository
* Get developer credentials from [Spotify Developer portal](https://developer.spotify.com/dashboard/login)
* Python 3
* Install dependencies

```
pip install -r requirements.txt
```

## Usage

* Set API credentials in the background
```sh
export SPOTIPY_CLIENT_ID="<your client id>"
export SPOTIPY_CLIENT_SECRET="<your client secret>"
```

### Getting a list of all genres available

```
./spotplay.py list
```

### Generating a playlist

This might prompt you to login to your spotify account

```
./spotplay.py create --seed-genres pop sleep sad --count 100 --name "My Awesome Playlist" 
```

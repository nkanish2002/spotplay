#!/usr/bin/env python3

import spotipy

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from pprint import pprint

from terminaltables import SingleTable

import argparse

import sys, os


class PlaylistGenerator:
    def __init__(self, scope="public"):
        self.scopes = {
            "private": "playlist-modify-private",
            "public": "playlist-modify-public",
        }
        if scope not in self.scopes:
            raise Exception("Illegal scope")
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self.uc = None
        self.user = None
        self.scope = scope

    def get_genres(self):
        genres = self.sp.recommendation_genre_seeds()["genres"]
        data = [["Genres"]]
        for each in genres:
            data.append([each])
        table = SingleTable(data)
        print(table.table)

    def get_recommendation(self, genres: list, country="US", limit=10):
        return self.sp.recommendations(seed_genres=genres, country="US", limit=limit)

    def login(self):
        self.uc = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=self.scopes[self.scope],
                redirect_uri="http://localhost:8080/callback",
                username=os.environ["USER"],
            )
        )
        self.user = self.uc.current_user()
        print("Logged in as %s" % self.user["display_name"])

    def create_playlist(self, name: str, tracks: list):
        playlist = self.uc.user_playlist_create(
            user=self.user["id"],
            public=(self.scope == "public"),
            description="Playlist created with PL creator",
            name=name,
        )
        self.uc.user_playlist_add_tracks(self.user["id"], playlist["id"], tracks)
        print("Playlist %s created" % playlist["name"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify playlist generator")
    subparser = parser.add_subparsers(help="Commands", dest="subparser_name")
    command_list = subparser.add_parser("list", help="List all available genres")

    # parser.add_argument(
    #     "--genres", help="List genres available with spotify", action="store_true"
    # )

    command_create = subparser.add_parser("create", help="Create a new playlist")
    command_create.add_argument(
        "--seed-genres", help="List of genres", nargs="+", required=True
    )
    command_create.add_argument(
        "--count", help="Number of tracks (max 100)", default=10, type=int
    )
    # Didn't try the country feature. Use at your own risk :P
    command_create.add_argument(
        "--country",
        help="An ISO 3166-1 alpha-2 country code. If provided, all results will \
            be playable in this country.",
        default="US",
        type=str,
    )
    command_create.add_argument(
        "--name", help="Name of the playtlist (max 5)", default="PL playlist", type=str
    )
    command_create.add_argument(
        "--private", help="Set playlist as private", action="store_true"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    pg = PlaylistGenerator()
    if args.subparser_name == "list":
        pg.get_genres()
        sys.exit(0)
    if args.subparser_name == "create":
        if args.private:
            pg.scope = "private"

        pg.login()
        if len(args.seed_genres) > 5:
            print("Number of seed genres can't be more than 5")
            sys.exit(1)
        if args.count > 100:
            print("Cannot add more than 100 tracks to the playlist")
            sys.exit(1)

        recommendations = pg.get_recommendation(args.seed_genres, limit=args.count)
        tracks = [track["id"] for track in recommendations["tracks"]]
        pg.create_playlist(args.name, tracks)
        sys.exit(0)

#!/usr/bin/env python3

from typing import List, Tuple
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = ["user-library-read", "user-follow-modify", "user-library-modify"]

# Make sure to authorize the redirect_uri
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=True, redirect_uri="http://localhost:8080/callback"))

# Also, configure your environment variables


def follow_artists_from_tracks(all_artists: bool = False) -> Tuple[List[str], List[str]]:
    """
    Keyword arguments:
    all_artists: If all artists, or just the first listed artist should be followed

    Calls Spotify API and obtains all artists saved by the user.
        This is done in batches of 50 (limitation of standard API usage)

    After recieving a request, the first artist listed on each artist 
        is followed (if all_artists == True, then every artist on each artist
        is followed)


    Returns:
    followed_artists    -- Followed artist names
    followed_artist_ids -- Followed artist ids
    """
    max_request = 50 # Size of max request
    followed_artists, followed_artist_ids = set(), set()

    print("Getting all saved artists, and following their artists.")
    responses = []
    api_response = sp.current_user_saved_tracks(
        limit=max_request, 
        offset=0,
    )
    responses.extend(api_response['items'])
    count = 0
    while len(responses) < api_response['total']:
        ofst = len(responses)
        print((f"{datetime.now()} Getting request number"
            f" {count}, offset: {ofst}"))
        count += 1

        api_response = sp.current_user_saved_tracks(
            limit=max_request, 
            offset=ofst
        )
        responses.extend(api_response['items'])
        # End collection if api response is empty
        if len(api_response['items']) == 0:
            break

        artists = set()
        artist_ids = set()
        for item in api_response['items']:
            artist = item['track']
            for artist in artist['artists']:
                artists.add(artist['name'])
                artist_ids.add(artist['id'])

                # Only use first artists if not all_artists
                if not all_artists:
                    break

        followed_artists = followed_artists.union(artists)
        followed_artist_ids = followed_artist_ids.union(artist_ids)

    # Follow api calls are also limited
    # So we need to break these up
    print("Following found artists")
    artist_ids_list = list(followed_artist_ids)
    requested_follows = []
    count = 0
    for artist_id in artist_ids_list:
        requested_follows.append(artist_id)
        if len(requested_follows) == max_request:
            count += 1
            print((f"Following request {count} / "
                f"{len(artist_ids_list) // max_request + 1}"))
            sp.user_follow_artists(requested_follows)
            requested_follows = []
        
    if requested_follows:
        count += 1
        print((f"Following request {count} / "
            f"{len(artist_ids_list) // max_request + 1}"))
        sp.user_follow_artists(requested_follows)
        
    
    print("Done collecting all artists, and following their artists")
    followed_artists = list(followed_artists)
    followed_artists.sort()
    return followed_artists, artist_ids_list

def follow_artists_from_albums(all_artists: bool = False) -> Tuple[List[str], List[str]]:
    """
    Keyword arguments:
    all_artists: If all artists, or just the first listed artist should be followed

    Calls Spotify API and obtains all albums saved by the user.
        This is done in batches of 50 (limitation of standard API usage)

    After recieving a request, the first artist listed on each album 
        is followed (if all_artists == True, then every artist on each album
        is followed)


    Returns:
    followed_artists    -- Followed artist names
    followed_artist_ids -- Followed artist ids
    """
    max_request = 50 # Size of max request
    followed_artists, followed_artist_ids = set(), set()

    print("Getting all saved albums, and following their artists.")
    responses = []
    api_response = sp.current_user_saved_albums(
        limit=max_request, 
        offset=0,
    )
    responses.extend(api_response['items'])
    count = 0
    while len(responses) < api_response['total']:
        ofst = len(responses)
        print((f"{datetime.now()} Getting request number"
            f" {count}, offset: {ofst}"))
        count += 1

        api_response = sp.current_user_saved_albums(
            limit=max_request, 
            offset=ofst
        )
        responses.extend(api_response['items'])
        # End collection if api response is empty
        if len(api_response['items']) == 0:
            break

        artists = set()
        artist_ids = set()
        for item in api_response['items']:
            album = item['album']
            for artist in album['artists']:
                artists.add(artist['name'])
                artist_ids.add(artist['id'])

                # Only use first artists if not all_artists
                if not all_artists:
                    break

        followed_artists = followed_artists.union(artists)
        followed_artist_ids = followed_artist_ids.union(artist_ids)

    # Follow api calls are also limited
    # So we need to break these up
    print("Following found artists")
    artist_ids_list = list(followed_artist_ids)
    requested_follows = []
    count = 0
    for artist_id in artist_ids_list:
        requested_follows.append(artist_id)
        if len(requested_follows) == max_request:
            count += 1
            print((f"Following request {count} / "
                f"{len(artist_ids_list) // max_request + 1}"))
            sp.user_follow_artists(requested_follows)
            requested_follows = []
        
    if requested_follows:
        count += 1
        print((f"Following request {count} / "
            f"{len(artist_ids_list) // max_request + 1}"))
        sp.user_follow_artists(requested_follows)
        
    
    print("Done collecting all albums, and following their artists")
    followed_artists = list(followed_artists)
    followed_artists.sort()
    return followed_artists, artist_ids_list

def save_tracks_from_saved_albums():
    """
    Calls Spotify API and obtains all albums saved by the user.
        This is done in batches of 50 (limitation of standard API usage)

    After recieving a request, each song on every saved album is saved

    Returns:
    saved_tracks    -- Saved track names
    saved_track_ids -- Saved track ids
    """
    max_request = 50 # Size of max request
    saved_tracks, saved_track_ids = set(), set()

    print("Getting all saved albums, and saving their tracks.")
    responses = []
    api_response = sp.current_user_saved_albums(
        limit=max_request, 
        offset=0,
    )
    responses.extend(api_response['items'])
    count = 0
    while len(responses) < api_response['total']:
        ofst = len(responses)
        print((f"{datetime.now()} Getting request number"
            f" {count}, offset: {ofst}"))
        count += 1

        api_response = sp.current_user_saved_albums(
            limit=max_request, 
            offset=ofst
        )
        responses.extend(api_response['items'])
        # End collection if api response is empty
        if len(api_response['items']) == 0:
            break
        
        tracks = set()
        track_ids = set()

        for item in api_response['items']:
            album = item['album']
            secondary_api_response = sp.album_tracks(album['id'])
            for secondary_item in secondary_api_response['items']:
                track = secondary_item['name']
                track_id = secondary_item['id']
                tracks.add(track)
                track_ids.add(track_id)

        saved_tracks = saved_tracks.union(tracks)
        saved_track_ids = saved_track_ids.union(track_ids)

    # Follow api calls are also limited
    # So we need to break these up
    print("Saving found tracks")
    track_ids_list = list(saved_track_ids)
    requested_saves = []
    count = 0
    for track_id in track_ids_list:
        requested_saves.append(track_id)
        if len(requested_saves) == max_request:
            count += 1
            print((f"Saving request {count} / "
                f"{len(track_ids_list) // max_request + 1}"))
            sp.current_user_saved_tracks_add(requested_saves)
            requested_saves = []
        
    if requested_saves:
        count += 1
        print((f"Saving request {count} / "
            f"{len(track_ids_list) // max_request + 1}"))
        sp.current_user_saved_tracks_add(requested_saves)
        
    
    print("Done collecting all albums, and saving their tracks")
    saved_tracks = list(saved_tracks)
    saved_tracks.sort()
    return saved_tracks, track_ids_list


if __name__=="__main__":
    saved_tracks, _ = save_tracks_from_saved_albums() # follow_artists_from_albums()
    print(f"Saved {len(saved_tracks)} Tracks!")
    print("Saved the following tracks:")
    for track in saved_tracks:
        print(track)

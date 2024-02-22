from lyricsgenius import Genius
import sys
import os
import json
import re


def sanitize_filename(filename):
    # Replace spaces with underscores
    sanitized_filename = filename.replace(" ", "_")
    # Replace non-valid filename characters with underscores
    sanitized_filename = re.sub(r'[^\w\-_.()]', '_', sanitized_filename)
    return sanitized_filename


def create_folder_if_not_exists(folder_path):
    if os.path.exists(folder_path):
        print(f"Folder '{folder_path}' already exists.")
        return False  # Directory already exists
    else:
        try:
            # Create the directory, since it doesn't exist
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder_path}' created.")
            return True
        except Exception as e:
            print(f"An error occurred while creating the folder: {e}")
            return False  


def get_song_count(json_filepath):
    # Check if the JSON file already exists
    if os.path.exists(json_filepath):
        with open(json_filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            file_song_count = len(data)
        
        # Check if appending new songs is necessary
        if  file_song_count >= song_number:
            print("The JSON file already contains the maximum number of songs. Stop writing to the file.")
            sys.exit(0)  # Stop writing to the file
        else:
            print("Appending new entries to the JSON file.")
    else:
        file_song_count = 0
        print("Creating a new JSON file.") 

    return file_song_count


def fetch_lyrics(artist_name, song_number, api_timeout=20):
    artist_name_cleaned = artist_name.replace(' ', '_')
    # filename = filename = f'{sanitize_filename(artist_name)}-{song_number}'
    filename = filename = f'{sanitize_filename(artist_name)}'
    json_filepath = f'genius_export/{artist_name_cleaned}/{filename}.json'

    create_folder_if_not_exists(f'genius_export/{artist_name_cleaned}')
    file_song_count = get_song_count(json_filepath)

    
    api_key = os.getenv("GENIUS_API_KEY")
    if not api_key:
        raise ValueError("Genius API key not found in environment variables")

    genius = Genius(api_key, timeout=api_timeout)

    artist = genius.search_artist(artist_name, max_songs=song_number)
    page = 1
    songs = []
    lyrics = []

    while page:
        request = genius.artist_songs(artist.id,
                                    sort='popularity',
                                    per_page=50,
                                    page=page,
                                    )
        songs.extend(request['songs'])
        page = request['next_page']

    # Create a list to store song information as dictionaries
    song_info_list = []

    for i in range(file_song_count, song_number):
        most_popular_song = genius.search_song(songs[i]['title'], artist.name)
        if most_popular_song:
            # Remove contributor information from the beginning of the lyrics
            lyrics = most_popular_song.lyrics

            # Use regular expression to remove contributor information
            lyrics_index = lyrics.find("Lyrics")

            if lyrics_index != -1:
                # Remove everything before the first occurrence of "Lyrics"
                lyrics = lyrics[lyrics_index + len("Lyrics"):].strip()

            song_info = {
                "artist": most_popular_song.artist,
                "song name": most_popular_song.title,
                "lyrics": lyrics
            }
            song_info_list.append(song_info)

    # Append new entries to the existing data if the file already exists
    if os.path.exists(json_filepath):
        with open(json_filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            data.extend(song_info_list)
            song_info_list = data

    # Save the song information in JSON format
    with open(json_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(song_info_list, json_file, ensure_ascii=False, indent=4)


def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <artist_name> <song_number>")
        sys.exit(1)

    artist_name = sys.argv[1]
    song_number = int(sys.argv[2])

    fetch_lyrics(artist_name, song_number)


if __name__ == "__main__":
    main()
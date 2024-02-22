import json
import sys

if len(sys.argv) != 2:
    print("Usage: python script_name.py <directory/filename>")
    sys.exit(1)

filepath = sys.argv[1]
json_filepath = f'{filepath}.json'

def remove_duplicate_songs(input_json_path, output_json_path):
    # Load the JSON file
    with open(input_json_path, 'r', encoding='utf-8') as file:
        songs_data = json.load(file)

    # Initialize a list to hold unique songs and a set to track seen song names
    unique_songs = []
    seen_song_names = set()

    # Iterate through each song in the data
    for song in songs_data:
        # Check if the song name has already been seen
        if song["song name"] not in seen_song_names:
            # If not, add the song to the list of unique songs and mark the song name as seen
            unique_songs.append(song)
            seen_song_names.add(song["song name"])

    # Write the unique songs back to a new JSON file
    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(unique_songs, file, indent=4)

# Specify the input and output file paths
input_json_path = f'{json_filepath}'  # Update this path
output_json_path = f'{filepath}-cleaned.json'  # Update this path

# Call the function to remove duplicate songs
remove_duplicate_songs(input_json_path, output_json_path)

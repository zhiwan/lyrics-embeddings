import json
import glob
import sys

if len(sys.argv) != 2:
    print("Usage: python script_name.py <filepath>")
    sys.exit(1)

json_filepath = sys.argv[1]

def extract_song_data_from_directory(input_directory, output_json_path):
    # Initialize a list to hold all extracted tracks from all files
    all_tracks = []

    # Use glob to find all JSON files in the input directory
    for input_json_path in glob.glob(f"{input_directory}/*.json"):
        try:
            # Load the current JSON file
            with open(input_json_path, 'r') as file:
                data = json.load(file)

            # Extract the required information from the current file
            extracted_songs = [
                {
                    "artist": track["song"]["artist_names"],
                    "song name": track["song"]["full_title"],
                    "lyrics": track["song"]["lyrics"]
                } for track in data["tracks"]
            ]

            # Append the extracted songs from the current file to the all_songs list
            all_tracks.extend(extracted_songs)

        except TypeError as e:
            # If a TypeError occurs, print the error and the file name, then continue to the next file
            print(f"Error processing file {input_json_path}: {e}")

    # Write all the extracted data to the output JSON file
    with open(output_json_path, 'w') as file:
        json.dump(all_tracks, file, indent=4)
        json.dump({"tracks": all_tracks}, file, indent=4)

# Define the paths for the input and output JSON files
input_json_path = f'{json_filepath}'  # Update this path
output_json_path = f'{json_filepath}/{json_filepath}-theo-simplified.json'  # Update this path
 
# Call the function with the specified paths
extract_song_data_from_directory(input_json_path, output_json_path)

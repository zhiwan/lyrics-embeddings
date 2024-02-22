import os
import json
import sys

def combine_json_folders(folders):
    combined_data = []

    # Loop through each folder and read the JSON data
    for folder in folders:
        filepath = os.path.join(f'genius_export/{folder}', f'{folder}_embeddings.json')
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            combined_data.extend(data)

    return combined_data

def main(folders):
    if len(folders) < 2:
        print("Please provide at least two folders.")
        sys.exit(1)

    # Combine the JSON data from the specified folders
    combined_data = combine_json_folders(folders)

    # Create a new folder name and JSON filename based on the input folders
    new_folder_name = "_vs_".join(folders)
    os.makedirs(f'plot/{new_folder_name}', exist_ok=True)
    new_json_filename = os.path.join(f'plot/{new_folder_name}', f"{new_folder_name}_embeddings.json")

    # Write the combined data to the new JSON file
    with open(new_json_filename, 'w', encoding='utf-8') as file:
        json.dump(combined_data, file, indent=4)

    print(f"Combined JSON data written to {new_json_filename}")

if __name__ == "__main__":
    main(sys.argv[1:])  # Pass all command line arguments except the script name to main

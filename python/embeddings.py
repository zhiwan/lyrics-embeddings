import json
from openai import OpenAI
import sys
import os




def check_filepath(json_filepath):
    # Check if the JSON file exists then loads
    if os.path.exists(json_filepath):
        with open(json_filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        print("No file found.")
        sys.exit(0)  # Stop writing to the file

    return data


def get_embedding(client, text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


def add_embeddings_to_file(client, json_filepath, json_out_filepath):

    data = check_filepath(json_filepath)

    # Iterate over each entry in the JSON file
    for entry in data:
        # Retrieve the lyrics from the entry
        lyrics = entry['lyrics']
        # lyrics = entry['text']

        # Generate embeddings for the lyrics
        embeddings = get_embedding(client, lyrics, model='text-embedding-3-small')

        # Update the entry in the JSON file with the embeddings
        entry['embeddings'] = embeddings
    
    save_file(json_out_filepath, data)


def save_file(json_out_filepath, data):
    # Save the updated data back to the JSON file
    with open(json_out_filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    json_filepath = f'genius_export/{filename}/{filename}.json'
    json_out_filepath = f'genius_export/{filename}/{filename}_embeddings.json'

    client = OpenAI(
        #define openai api key
        api_key = os.getenv("OPENAI_API_KEY")
    )

    add_embeddings_to_file(client, json_filepath, json_out_filepath)
    # check_filepath(json_filepath)


if __name__ == "__main__":
    main()

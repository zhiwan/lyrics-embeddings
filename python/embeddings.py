import json
from openai import OpenAI
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python script_name.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
json_filepath = f'genius_export/{filename}.json'

client = OpenAI(
    #define openai api key
    api_key = "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"
)


# Check if the JSON file exists then loads
if os.path.exists(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
else:
    print("No file found.")
    sys.exit(0)  # Stop writing to the file


def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding




# Iterate over each entry in the JSON file
for entry in data:
    # Retrieve the lyrics from the entry
    lyrics = entry['lyrics']

    # Generate embeddings for the lyrics
    embeddings = get_embedding(lyrics, model='text-embedding-3-small')

    # Update the entry in the JSON file with the embeddings
    entry['embeddings'] = embeddings

# Save the updated data back to the JSON file
with open(json_filepath, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)
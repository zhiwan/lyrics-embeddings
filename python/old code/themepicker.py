from requests.exceptions import HTTPError, Timeout
from lyricsgenius import Genius
import json
import re
from openai import OpenAI


def summarize_themes(lyrics):
    client = OpenAI(
        #define openai api key
        api_key = "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"
    )

    # Create an empty list to store response content
    response_content = []
    
    # Create a prompt for ChatGPT
    prompt = f"Provide 5 single word summaries of the theme of the following lyrics:\n\n{lyrics}\n\nThemes:"

    # Generate a response from ChatGPT
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],

        model="gpt-3.5-turbo",
        # max_tokens=50,  # Adjust as needed
        # n=1,  # Number of responses to generate
        # stop=["\n"]  # Stop generating after a newline character
    )

    # Extract the generated summary from the response
    summary = stream.choices[0].message.content

    # Use regular expression to remove numbers and periods
    cleaned_summary = re.sub(r'\d+\.', '', summary)

    # Split the string by newline and period, and remove empty elements
    split_summary = [item.strip() for item in cleaned_summary.split("\n") if item.strip() != ""]

    # Join the list elements with commas
    result = ", ".join(split_summary)

    return result


genius = Genius("HKtIlU3CSjM8tfVPmBYS59hu7o633x96FRNCsnayK_oxXU7lFOJ_QU5a5gMWb_-x")

artist = genius.search_artist('Andy Shauf', max_songs=10)
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

for i in range(10):
    most_popular_song = genius.search_song(songs[i]['title'], artist.name)
    if most_popular_song:
        song_info = {
            "artist": most_popular_song.artist,
            "song name": most_popular_song.title,
            "lyrics": most_popular_song.lyrics
        }
        song_info_list.append(song_info)

# Save the song information in JSON format
with open('beatles.json', 'w', encoding='utf-8') as json_file:
    json.dump(song_info_list, json_file, ensure_ascii=False, indent=4)

# Load the lyrics from the JSON file
with open('beatles.json', 'r', encoding='utf-8') as json_file:
    songs_data = json.load(json_file)

# Process each song's lyrics and generate summaries
for song_info in songs_data:
    lyrics = song_info["lyrics"]
    summary = summarize_themes(lyrics)
    song_info["theme_summary"] = summary

# Save the updated data (including theme summaries) to a new JSON file
with open('beatles_with_themes.json', 'w', encoding='utf-8') as json_file:
    json.dump(songs_data, json_file, ensure_ascii=False, indent=4)

    
# Load the JSON file with themes
with open('beatles_with_themes.json', 'r') as json_file:
    themes_data = json.load(json_file)

# Initialize an empty set to store the unique themes
unique_themes = set()

# Iterate through the data and add each theme to the set
for entry in themes_data:
    theme_summary = entry.get("theme_summary", "")
    if theme_summary:
        # Split the theme summary into individual themes using a comma as the separator
        themes = [theme.strip() for theme in theme_summary.split(",")]
        
        # Add each theme to the set
        unique_themes.update(themes)

# Convert the set of unique themes to a list
# unique_themes_list = list(unique_themes)

themes_string = ", ".join(unique_themes)

client = OpenAI(
    #define openai api key
    api_key = "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"
)

# Create an empty list to store response content
response_content = []

# Create a prompt for ChatGPT
prompt=f"Simplify the following themes: {themes_string}\nLimit the list to 20 items.\n"

# Generate a response from ChatGPT
stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],

    model="gpt-3.5-turbo",
)

# Extract the generated summary from the response
simplified_themes  = stream.choices[0].message.content

# Split the simplified themes into a list
simplified_themes_list = [theme.strip() for theme in simplified_themes.split(",") if theme.strip()]

# Take the first 20 items (or less) from the list just in case chat gives more
simplified_themes_20 = simplified_themes_list[:20]

# Create a dictionary to represent the simplified themes
simplified_themes_dict = {"simplified_themes": simplified_themes_20}

# Save the simplified themes to a JSON file
with open('simplified_themes.json', 'w', encoding='utf-8') as json_file:
    json.dump(simplified_themes_dict, json_file, ensure_ascii=False, indent=4)

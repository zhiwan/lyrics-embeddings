from lyricsgenius import Genius
import json
import re
from openai import OpenAI


def summarize_themes(lyrics):
    client = OpenAI(
        #define openai api key
        api_key = "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"
    )

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

# def summarize_themes(lyrics):
#     #define openai api key
#     api_key = "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"

#     # Initialize the OpenAI API client
#     openai.api_key = api_key

#     # Create a prompt for ChatGPT
#     prompt = f"Summarize 3 to 4 themes in the following lyrics:\n\n{lyrics}\n\nThemes:"

#     # Generate a response from ChatGPT
#     response = openai.Completion.create(
#         model="gpt-3.5-turbo",
#         prompt=prompt,
#         max_tokens=50,  # Adjust as needed
#         n=1,  # Number of responses to generate
#         stop=["\n"]  # Stop generating after a newline character
#     )

#     # Extract the generated summary from the response
#     summary = response.choices[0].text.strip()

#     return summary

genius = Genius("HKtIlU3CSjM8tfVPmBYS59hu7o633x96FRNCsnayK_oxXU7lFOJ_QU5a5gMWb_-x")

artist = genius.search_artist('Andy Shauf', max_songs=2)
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

for i in range(2):
    most_popular_song = genius.search_song(songs[i]['title'], artist.name)
    if most_popular_song:
        song_info = {
            "artist": most_popular_song.artist,
            "song name": most_popular_song.title,
            "lyrics": most_popular_song.lyrics
        }
        song_info_list.append(song_info)

        # print(most_popular_song.lyrics)
        # print("\n" + "=" * 50 + "\n")  # Separation line
    # else:
    #     print(f"No lyrics found for '{songs[i]['title']}'")

# Save the song information in JSON format
with open('andy_shauf_lyrics.json', 'w', encoding='utf-8') as json_file:
    json.dump(song_info_list, json_file, ensure_ascii=False, indent=4)

# Load the lyrics from the JSON file
with open('andy_shauf_lyrics.json', 'r', encoding='utf-8') as json_file:
    songs_data = json.load(json_file)

# Process each song's lyrics and generate summaries
for song_info in songs_data:
    lyrics = song_info["lyrics"]
    summary = summarize_themes(lyrics)
    song_info["theme_summary"] = summary

# Save the updated data (including theme summaries) to a new JSON file
with open('andy_shauf_lyrics_with_summaries.json', 'w', encoding='utf-8') as json_file:
    json.dump(songs_data, json_file, ensure_ascii=False, indent=4)

# print("Lyrics saved as 'andy_shauf_lyrics.json'")
# print(most_popular_songs)
# artist.save_lyrics()
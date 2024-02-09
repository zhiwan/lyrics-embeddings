import json
from openai import OpenAI

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

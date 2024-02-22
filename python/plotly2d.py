import plotly.express as px
import pandas as pd
import json
import sys
import os
import glob

# Load Embeddings from JSON
def load_embeddings(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extracting 'tsne_embeddings' and interpreting the first element as 'x' and the second as 'y'
    embeddings = []
    for entry in data:
        # Check if 'tsne_embeddings' key exists
        if 'tsne_embeddings' in entry:
            # Extract artist, song name, and lyrics, using placeholders if they don't exist
            artist = entry.get('artist', 'Unknown Artist')
            song_name = entry.get('song name', 'Unknown Song')
            text = entry.get('text', 'No Lyrics Available')[:100] + '...'  # Truncate lyrics for brevity

            embeddings.append({
                'x': entry['tsne_embeddings'][0], 
                'y': entry['tsne_embeddings'][1], 
                'artist': artist, 
                'song_name': song_name, 
                'text': text
            })
    
    # Proceed only if there are embeddings to plot
    if embeddings:
        return pd.DataFrame(embeddings)  # Directly return a DataFrame
    else:
        return None

def plot_tsne_embeddings(df, filename='tsne2d_plot.html'):
    hover_text = [
        f'X: {x:.2f}<br>Y: {y:.2f}<br>Artist: {artist}<br>Song: {song}<br>Lyrics: {text}'
        for x, y, artist, song, text in zip(df['x'], df['y'], df['artist'], df['song_name'], df['text'])
    ]
    fig = px.scatter(df, x='x', y='y', color='artist', hover_name='song_name', hover_data={'lyrics': df['text']},
                     title='t-SNE Visualization by Artist', labels={'x': 'Component 1', 'y': 'Component 2'})
    
    fig.update_traces(text=hover_text, hoverinfo='text')
    fig.update_layout(showlegend=True)

    fig.show()
    fig.write_html(filename)
    print(f"Plot saved to '{filename}'")


def main():
    if len(sys.argv) != 2:
        print("Directory holding json embeddings <load_filename>")
        sys.exit(1)

    load_filename = sys.argv[1]
    filepath = f'plot/{load_filename}'
    json_filepath = f'{filepath}/{load_filename}_embeddings_2d.json'

    tsne_embeddings = load_embeddings(json_filepath)
    
    # Check if there are any embeddings to plot
    if tsne_embeddings is not None:
        plot_tsne_embeddings(tsne_embeddings, filename=os.path.splitext(f'{filepath}/')[0] + '_2dplot.html')
    else:
        print("No valid tsne_embeddings found in the file.")

if __name__ == "__main__":
    main()
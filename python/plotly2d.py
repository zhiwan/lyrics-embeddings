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
            lyrics = entry.get('lyrics', 'No Lyrics Available')[:100] + '...'  # Truncate lyrics for brevity

            embeddings.append({
                'x': entry['tsne_embeddings'][0], 
                'y': entry['tsne_embeddings'][1], 
                'artist': artist, 
                'song_name': song_name, 
                'lyrics': lyrics
            })
    
    # Proceed only if there are embeddings to plot
    if embeddings:
        return pd.DataFrame(embeddings)  # Directly return a DataFrame
    else:
        return None

def plot_tsne_embeddings(dataframes, labels, filename='tsne_plot.html'):
    fig = px.scatter()
    for df, label in zip(dataframes, labels):
        hover_text = [
            f'X: {x:.2f}<br>Y: {y:.2f}<br>Artist: {artist}<br>Song: {song}<br>Lyrics: {lyrics}'
            for x, y, artist, song, lyrics in zip(df['x'], df['y'], df['artist'], df['song_name'], df['lyrics'])
        ]
        fig.add_scatter(x=df['x'], y=df['y'], mode='markers', name=label, 
                        hoverinfo='text', text=hover_text)
    
    fig.update_layout(title='t-SNE Visualization', xaxis_title='Component 1', yaxis_title='Component 2')
    fig.show()
    fig.write_html(filename)
    print(f"Plot saved to '{filename}'")


def main():
    if len(sys.argv) != 2:
        print("Directory holding json embeddings <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    dataframes = []
    labels = []

    # Use glob to find all JSON files in the directory
    for json_filepath in glob.glob(os.path.join(directory, '*.json')):
        tsne_embeddings = load_embeddings(json_filepath)

        # Proceed only if tsne_embeddings were found
        if tsne_embeddings is not None:
            # Generate a filename for the plot
            # plot_filename = f'{os.path.splitext(json_filepath)[0]}_plot.html'
            # plot_tsne_embeddings(tsne_embeddings, filename=plot_filename)
            dataframes.append(tsne_embeddings)
            # Use the filename (without extension) as the label
            labels.append(os.path.splitext(os.path.basename(json_filepath))[0])
    
    # Check if there are any embeddings to plot
    if dataframes:
        plot_tsne_embeddings(dataframes, labels, filename=os.path.join(directory, 'combined_tsne_plot.html'))
    else:
        print("No valid tsne_embeddings found in the directory.")

if __name__ == "__main__":
    main()
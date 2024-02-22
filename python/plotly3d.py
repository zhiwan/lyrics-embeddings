import plotly.express as px
import plotly.graph_objects as go  # Import Graph Objects for more control over traces
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
                'z': entry['tsne_embeddings'][2],
                'artist': artist, 
                'song_name': song_name, 
                'lyrics': lyrics
            })
    
    # Proceed only if there are embeddings to plot
    if embeddings:
        return pd.DataFrame(embeddings)  # Directly return a DataFrame
    else:
        return None

def plot_tsne_embeddings(dataframes, labels, filename='tsne3d_plot.html'):
    fig = go.Figure()  # Use a generic Figure object to have more control over traces

    # Define a color palette (extend this list if you have more files)
    color_palette = px.colors.qualitative.Plotly

    for df, label, color in zip(dataframes, labels, color_palette):
        # Add a trace for each DataFrame with a unique color and label
        fig.add_trace(go.Scatter3d(
            x=df['x'], y=df['y'], z=df['z'],
            mode='markers',
            marker=dict(size=5, color=color),  # Use the color from the palette
            name=label,  # Set the trace name to the label for the legend
            hoverinfo='text',  # Show custom hover text
            text=[  # Define custom hover text using DataFrame values
                f'X: {x:.2f}<br>Y: {y:.2f}<br>Z: {z:.2f}<br>Artist: {artist}<br>Song: {song}<br>Lyrics: {lyrics}'
                for x, y, z, artist, song, lyrics in zip(df['x'], df['y'], df['z'], df['artist'], df['song_name'], df['lyrics'])
            ]
        ))

    fig.update_layout(
        title='3D t-SNE Visualization',
        scene=dict(
            xaxis_title='Component 1',
            yaxis_title='Component 2',
            zaxis_title='Component 3'
        ),
        legend_title="JSON Files"
    )
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
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
            text = entry.get('text', 'No Lyrics Available')[:100] + '...'  # Truncate lyrics for brevity

            embeddings.append({
                'x': entry['tsne_embeddings'][0], 
                'y': entry['tsne_embeddings'][1], 
                'z': entry['tsne_embeddings'][2],
                'artist': artist, 
                'song_name': song_name, 
                'text': text
            })
    
    # Proceed only if there are embeddings to plot
    if embeddings:
        return pd.DataFrame(embeddings)  # Directly return a DataFrame
    else:
        return None

def plot_tsne_embeddings(df, filename='tsne3d_plot.html'):
    fig = go.Figure()  # Use a generic Figure object to have more control over traces

    # Create a list of unique artists for coloring
    unique_artists = df['artist'].unique()
    # Generate a color for each unique artist
    colors = px.colors.qualitative.Plotly * (len(unique_artists) // len(px.colors.qualitative.Plotly) + 1)

    # Map each artist to a color
    color_map = {artist: colors[i] for i, artist in enumerate(unique_artists)}

    # Add a trace for each point, coloring by artist
    for i, row in df.iterrows():
        fig.add_trace(go.Scatter3d(
            x=[row['x']], y=[row['y']], z=[row['z']],
            mode='markers',
            marker=dict(size=5, color=color_map[row['artist']]),  # Use the mapped color
            hoverinfo='text',  # Show custom hover text
            text=  # Define custom hover text using DataFrame values
                f"X: {row['x']:.2f}<br>Y: {row['y']:.2f}<br>Z: {row['z']:.2f}<br>Artist: {row['artist']}<br>Song: {row['song_name']}<br>Text: {row['text']}",
            showlegend=False  # Optionally hide individual trace legends, since there will be many
        ))

    # Optionally add a legend trace for each artist
    for artist, color in color_map.items():
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            mode='markers',
            marker=dict(size=5, color=color),
            name=artist
        ))

    fig.update_layout(
        title='3D t-SNE Visualization',
        scene=dict(
            xaxis_title='Component 1',
            yaxis_title='Component 2',
            zaxis_title='Component 3'
        ),
        legend_title="Artists"
    )
    fig.show()
    fig.write_html(filename)
    print(f"Plot saved to '{filename}'")


def main():

    if len(sys.argv) != 2:
        print("Directory holding json embeddings <load_filename>")
        sys.exit(1)

    load_filename = sys.argv[1]
    filepath = f'plot/{load_filename}'
    json_filepath = f'{filepath}/{load_filename}_embeddings_3d.json'

    tsne_embeddings = load_embeddings(json_filepath)

    # Check if there are any embeddings to plot
    if tsne_embeddings is not None:
        plot_tsne_embeddings(tsne_embeddings, filename=os.path.splitext(f'{filepath}/')[0] + '_3dplot.html')
    else:
        print("No valid tsne_embeddings found in the file.")


if __name__ == "__main__":
    main()
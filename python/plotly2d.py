import plotly.express as px
import pandas as pd
import json
import sys
import os

# Load Embeddings from JSON
def load_embeddings(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extracting 'tsne_embeddings' and interpreting the first element as 'x' and the second as 'y'
    embeddings = [{'x': entry['tsne_embeddings'][0], 'y': entry['tsne_embeddings'][1]} for entry in data]

    return pd.DataFrame(embeddings)  # Directly return a DataFrame


# Function to plot t-SNE embeddings using Plotly
def plot_tsne_embeddings(df, filename='tsne_plot.html'):
    # Use Plotly Express to create the scatter plot
    fig = px.scatter(df, x='x', y='y', title='t-SNE Visualization')

    # Show the plot
    fig.show()

    # Optionally, save the plot to an HTML file
    fig.write_html(filename)
    print(f"Plot saved to '{filename}'")


def main():

    if len(sys.argv) != 2:
        print("Usage: python script_name.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    json_filepath = f'genius_export/{filename}.json'

    tsne_embeddings = load_embeddings(json_filepath)
    plot_tsne_embeddings(tsne_embeddings, filename=f'{os.path.splitext(json_filepath)[0]}_plot.html')

if __name__ == "__main__":
    main()
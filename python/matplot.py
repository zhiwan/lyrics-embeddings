import matplotlib.pyplot as plt
import matplotlib

import pandas as pd
import json
import sys
import os

# Load Embeddings from JSON
def load_embeddings(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to plot t-SNE embeddings using Plotly
def plot_tsne_embeddings(tsne_embeddings, filename='tsne_plot.html'):
    # Create a DataFrame from the t-SNE embeddings for easy plotting
    df = pd.DataFrame(tsne_embeddings, columns=['x', 'y'])
    
    # Use Plotly Express to create the scatter plot
    fig = px.scatter(df, x='x', y='y', title='t-SNE Visualization')

    # Show the plot
    fig.show()

    # Optionally, save the plot to an HTML file
    fig.write_html(filename)
    print(f"Plot saved to '{filename}'")

df = pd.read_csv('output/embedded_1k_reviews.csv')
matrix = df.ada_embedding.apply(eval).to_list()

# Create a t-SNE model and transform the data
tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200)
vis_dims = tsne.fit_transform(matrix)

colors = ["red", "darkorange", "gold", "turquiose", "darkgreen"]
x = [x for x,y in vis_dims]
y = [y for x,y in vis_dims]
color_indices = df.Score.values - 1

colormap = matplotlib.colors.ListedColormap(colors)
plt.scatter(x, y, c=color_indices, cmap=colormap, alpha=0.3)
plt.title("Amazon ratings visualized in language using t-SNE")


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
from sklearn.manifold import TSNE
import numpy as np
import json
import sys
import os


# Load Embeddings from JSON
def load_embeddings(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    embeddings = [entry['embeddings'] for entry in data]
    return data, np.array(embeddings)  # Return both data and embeddings


def apply_tsne(embeddings, n_components=2, random_state=42, init='random', learning_rate=200):
    # get length of embeddings. adjust perplexity of num of samples is less than 30
    n_samples = len(embeddings)
    if n_samples > 30:
        perplexity = 30
    else:
        perplexity = max(n_samples / 3, 1)  # Ensure a minimum perplexity value, e.g., 5

    tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state, init=init, learning_rate=learning_rate)
    return tsne.fit_transform(embeddings)


def save_tsne_embeddings(original_data, tsne_embeddings, original_json_filepath):
    # Update the original data entries with t-SNE embeddings
    for entry, embedding in zip(original_data, tsne_embeddings):
        entry['tsne_embeddings'] = embedding.tolist()  # Convert numpy array to list for JSON serialization

    # Save updated data to the new JSON file
    with open(original_json_filepath, 'w', encoding='utf-8') as file:
        json.dump(original_data, file, indent=4)

    print(f"Saved t-SNE embeddings to '{original_json_filepath}'")


def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    json_filepath = f'genius_export/{filename}/{filename}_embeddings.json'

    # Load original embeddings
    original_data, embeddings = load_embeddings(json_filepath)
    
    # Apply t-SNE with n_components=2
    tsne_embeddings_2d = apply_tsne(embeddings, n_components=2)
    # Save the t-SNE transformed embeddings for 2D
    save_tsne_embeddings(original_data, tsne_embeddings_2d, json_filepath.replace('.json', '_2d.json'))
    
    # Apply t-SNE with n_components=3
    tsne_embeddings_3d = apply_tsne(embeddings, n_components=3)
    # Save the t-SNE transformed embeddings for 3D
    save_tsne_embeddings(original_data, tsne_embeddings_3d, json_filepath.replace('.json', '_3d.json'))


if __name__ == "__main__":
    main()
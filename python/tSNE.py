from sklearn.manifold import TSNE
import numpy as np
import json
import sys
import os


if len(sys.argv) != 2:
    print("Usage: python script_name.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
json_filepath = f'genius_export/{filename}.json'

# Load Embeddings from JSON
def load_embeddings(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    embeddings = [entry['embeddings'] for entry in data]
    return data, np.array(embeddings)  # Return both data and embeddings


# Apply t-SNE
def apply_tsne(embeddings, n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200):
    tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state, init=init, learning_rate=learning_rate) #random_state=0
    return tsne.fit_transform(embeddings)

# Save t-SNE Embeddings to New JSON File
def save_tsne_embeddings(original_data, tsne_embeddings, original_json_filepath):
    # Update the original data entries with t-SNE embeddings
    for entry, embedding in zip(original_data, tsne_embeddings):
        entry['tsne_embeddings'] = embedding.tolist()  # Convert numpy array to list for JSON serialization

    # Generate new filename with '_small' suffix before the file extension
    base, ext = os.path.splitext(original_json_filepath)
    new_filename = f"{base}_tsne{ext}"

    # Save updated data to the new JSON file
    with open(new_filename, 'w', encoding='utf-8') as file:
        json.dump(original_data, file, indent=4)

    print(f"Saved t-SNE embeddings to '{new_filename}'")

def main():
    # Load original embeddings
    original_data, embeddings = load_embeddings(json_filepath)
    
    # Apply t-SNE
    tsne_embeddings = apply_tsne(embeddings)
    
    # Save the t-SNE transformed embeddings
    save_tsne_embeddings(original_data, tsne_embeddings, json_filepath)

if __name__ == "__main__":
    main()
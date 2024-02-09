from sklearn.manifold import TSNE
import numpy as np
import json
from openai import OpenAI
import sys
import os


# Convert the embeddings list to a NumPy array if it's not already
X = np.array(embeddings)

# Initialize and fit t-SNE
tsne = TSNE(n_components=2, perplexity=30, learning_rate=200, random_state=0)
X_embedded = tsne.fit_transform(X)

embeddings = [entry['embeddings'] for entry in data]

from ahocorasick import Automaton
from itertools import combinations

def build_automaton(tags):
    automaton = Automaton()
    for tag in tags:
        # Generate all possible combinations of words in the tag
        words = tag.lower().split()
        for i in range(1, len(words) + 1):
            for combo in combinations(words, i):
                combo_str = " ".join(combo)
                automaton.add_word(combo_str, combo_str)
    automaton.make_automaton()
    return automaton

def tag_text(text, automaton):
    text_lower = text.lower()
    matched_tags = set()
    for end_index, tag in automaton.iter(text_lower):
        matched_tags.add(tag)
    return list(matched_tags)

from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np

def build_tag_embeddings(tags, model):
    """Build embeddings for all tags."""
    return {tag: model.encode(tag.lower()) for tag in tags}

def build_faiss_index(tag_embeddings):
    """Build a FAISS index for fast similarity search."""
    # Convert embeddings into a numpy array for FAISS
    embeddings_matrix = np.array(list(tag_embeddings.values())).astype('float32')
    
    # Create a FAISS index (L2 distance for Euclidean similarity)
    index = faiss.IndexFlatL2(embeddings_matrix.shape[1])  # L2 distance
    index.add(embeddings_matrix)
    return index

def tag_text_with_faiss(text, tag_embeddings, faiss_index, model, top_k=10):
    """Tag new text and rank the matched tags using FAISS."""
    # Encode the input text into an embedding
    text_embedding = model.encode(text.lower()).astype('float32')
    
    # Search for the top_k closest tags (top_k=5 in this case)
    D, I = faiss_index.search(np.expand_dims(text_embedding, axis=0), k=top_k)  # k closest matches

    ranked_tags = []
    for idx, dist in zip(I[0], D[0]):
        if idx == -1:  # Skip invalid indices
            continue
        tag = list(tag_embeddings.keys())[idx]
        similarity = 1 / (1 + dist)  # Similarity: 1 / (1 + Euclidean distance)
        ranked_tags.append((tag, similarity))
    
    # Sort the ranked tags by similarity score (highest first)
    ranked_tags.sort(key=lambda x: x[1], reverse=True)
    
    return ranked_tags

def build_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')
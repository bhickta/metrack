from ahocorasick import Automaton
from itertools import combinations
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def build_automaton(tags):
    automaton = Automaton()
    for tag in tags:
        words = tag.lower().split()
        for i in range(1, len(words) + 1):
            for combo in combinations(words, i):
                automaton.add_word(" ".join(combo), tag)
    automaton.make_automaton()
    return automaton

def tag_text(text, automaton):
    return list({tag for _, tag in automaton.iter(text.lower())})

def build_tag_embeddings(tags, model):
    return {tag: model.encode(tag.lower(), convert_to_numpy=True) for tag in tags}

def build_faiss_index(tag_embeddings):
    embeddings_matrix = np.array(list(tag_embeddings.values()), dtype='float32')
    d = embeddings_matrix.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings_matrix)
    return index

def tag_text_with_faiss(text, tag_embeddings, faiss_index, model, top_k=10):
    text_embedding = model.encode(text.lower(), convert_to_numpy=True).reshape(1, -1)
    D, I = faiss_index.search(text_embedding, k=top_k)
    return sorted(((list(tag_embeddings.keys())[idx], 1 / (1 + dist)) for idx, dist in zip(I[0], D[0]) if idx != -1), key=lambda x: x[1], reverse=True)

def build_embedding_model():
    return SentenceTransformer('hkunlp/instructor-xl')

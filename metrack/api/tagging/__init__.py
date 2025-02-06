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

import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer

def preprocess_text(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def build_embedding_model():
    return SentenceTransformer("BAAI/bge-large-en")

def build_tag_embeddings(tags, model):
    return {tag: model.encode(preprocess_text(tag), convert_to_numpy=True) for tag in tags}

def build_faiss_index(tag_embeddings):
    embeddings_matrix = np.array(list(tag_embeddings.values()), dtype='float32')
    d = embeddings_matrix.shape[1]
    index = faiss.IndexHNSWFlat(d, 32)
    index.add(embeddings_matrix)
    return index

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def tag_text_with_faiss(text, tag_embeddings, faiss_index, model, top_k=20):
    text_embedding = model.encode(preprocess_text(text), convert_to_numpy=True).reshape(1, -1)
    D, I = faiss_index.search(text_embedding, k=top_k)
    scores = softmax(np.array([1 / (1 + dist) for dist in D[0] if dist >= 0]))
    return sorted(((list(tag_embeddings.keys())[idx], score) for idx, score in zip(I[0], scores) if idx != -1), key=lambda x: x[1], reverse=True)
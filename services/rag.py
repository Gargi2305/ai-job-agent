from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# load model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# cache
resume_cache = {}

def chunk_text(text, size=300, overlap=50):
    words = text.split()
    return [
        " ".join(words[i:i + size])
        for i in range(0, len(words), size - overlap)
    ]

def build_index(chunks):
    embeddings = embedding_model.encode(chunks)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index

def get_resume_index(resume):
    if resume in resume_cache:
        return resume_cache[resume]

    chunks = chunk_text(resume)
    index = build_index(chunks)

    resume_cache[resume] = (chunks, index)
    return chunks, index

def retrieve_chunks(query, chunks, index, k=5):
    query_embedding = embedding_model.encode([query])
    _, indices = index.search(np.array(query_embedding), k)

    return [chunks[i] for i in indices[0]]
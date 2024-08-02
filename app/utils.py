

import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

import logging
logger = logging.getLogger(__name__)

def create_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def create_embeddings(space_name, data, is_file_based):
    model = SentenceTransformer('model/all-MiniLM-L6-v2')
    if is_file_based:
        # Assuming data is a DataFrame
        texts = data.apply(lambda row: ' '.join(row.astype(str)), axis=1).tolist()
    else:
        # Assuming data is a string (query or notes)
        texts = [data]
    embeddings = model.encode(texts)
    index = create_faiss_index(embeddings)
    faiss.write_index(index, f"spaces/{space_name}/index")



def retrieve_relevant_files(space_name, query):
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/all-MiniLM-L6-v2'))
    model = SentenceTransformer(model_path)
    query_embedding = model.encode([query])

    space_path = os.path.join("spaces", space_name)
    index_path = os.path.join(space_path, "index")
    texts_path = os.path.join(space_path, "texts.pkl")

    # Load the FAISS index
    index = faiss.read_index(index_path)
    logger.debug(f"Loaded index from {index_path} with {index.ntotal} vectors")

    # Load the original texts
    with open(texts_path, 'rb') as f:
        texts = pickle.load(f)
    logger.debug(f"Loaded {len(texts)} texts from {texts_path}")

    # Perform the search
    k = min(5, len(texts))  # Ensure we don't request more results than we have texts
    D, I = index.search(query_embedding, k)
    logger.debug(f"Search results - Distances: {D[0]}, Indices: {I[0]}")

    similarity_threshold = 0.5  # Adjust as needed
    relevant_files = []

    for distance, idx in zip(D[0], I[0]):
        similarity_score = 1 - distance  # Convert distance to similarity score
        if similarity_score < similarity_threshold:
            continue

        relevant_text = texts[idx]

        file_info = {
            "source_file": f"document_{idx}",
            "short_content": relevant_text[:500],  # First 500 characters as preview
            "full_content": relevant_text,
            "similarity_score": similarity_score
        }

        relevant_files.append(file_info)

    logger.debug(f"Retrieved {len(relevant_files)} relevant documents")
    return relevant_files


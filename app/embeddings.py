import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

from utils import create_faiss_index

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_embeddings(space_name, data, is_file_based):
    # Determine the absolute path to the model directory
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/all-MiniLM-L6-v2'))

    model = SentenceTransformer(model_path)
    if is_file_based:
        # Assuming data is a DataFrame
        texts = data.apply(lambda row: ' '.join(row.astype(str)), axis=1).tolist()
    else:
        # Assuming data is a string (query or notes)
        texts = [data]

    logger.debug(f"Creating embeddings for {len(texts)} documents in {space_name}")

    embeddings = model.encode(texts)

    logger.debug(f"Embeddings shape: {embeddings.shape}")
    logger.debug(f"Sample embedding: {embeddings[0][:5]}...")  # Print first 5 values of first embedding

    index = create_faiss_index(embeddings)

    # Ensure the directory exists
    space_path = os.path.join("spaces", space_name)
    os.makedirs(space_path, exist_ok=True)

    # Save the FAISS index
    index_path = os.path.join(space_path, "index")
    faiss.write_index(index, index_path)

    # Save the original texts
    texts_path = os.path.join(space_path, "texts.pkl")
    with open(texts_path, 'wb') as f:
        pickle.dump(texts, f)

    logger.debug(f"FAISS index created for space: {space_name}")
    logger.debug(f"Index saved at: {index_path}")
    logger.debug(f"Texts saved at: {texts_path}")
    logger.debug(f"Number of vectors in index: {index.ntotal}")

    # Verify the index
    loaded_index = faiss.read_index(index_path)
    logger.debug(f"Loaded index vector count: {loaded_index.ntotal}")

    return index
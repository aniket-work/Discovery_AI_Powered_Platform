from embeddings import create_embeddings
from utils import retrieve_relevant_files


def test_faiss_retrieval():
    space_name = "test_space"
    test_docs = [
        "This is a test document about cats",
        "Dogs are man's best friend",
        "Python is a popular programming language",
        "Artificial intelligence is revolutionizing many industries",
        "The quick brown fox jumps over the lazy dog"
    ]

    # Create embeddings and index
    create_embeddings(space_name, "\n".join(test_docs), is_file_based=False)

    # Test queries
    queries = ["Tell me about cats", "What programming languages are popular?", "AI applications"]
    for query in queries:
        results = retrieve_relevant_files(space_name, query)
        print(f"\nQuery: {query}")
        for result in results:
            print(f"- Score: {result['similarity_score']:.2f}, Content: {result['short_content']}")


test_faiss_retrieval()
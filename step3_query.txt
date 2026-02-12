"""
Step 3: Query your POA documents using RAG.
Performs semantic search + vector search (hybrid), then sends results to GPT-4o.
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

load_dotenv()

# -- Clients --
openai_client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-06-01",
)

search_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]),
)


def get_embedding(text):
    """Get embedding vector for a text string."""
    response = openai_client.embeddings.create(
        input=text,
        model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"],
    )
    return response.data[0].embedding


def search_documents(query, top_k=5):
    """
    Hybrid search: combines keyword search + vector similarity + semantic ranking.
    This is the 'Retrieval' in RAG.
    """
    query_vector = get_embedding(query)

    results = search_client.search(
        search_text=query,
        vector_queries=[
            VectorizedQuery(
                vector=query_vector,
                k_nearest_neighbors=top_k,
                fields="content_vector",
            )
        ],
        top=top_k,
        query_type="semantic",
        semantic_configuration_name="my-semantic-config",
        select=["content", "source_file", "chunk_index"],
    )

    retrieved = []
    for result in results:
        retrieved.append({
            "content": result["content"],
            "source": result["source_file"],
            "score": result.get("@search.score", 0),
        })

    return retrieved


def ask_question(question):
    """
    Full RAG pipeline: retrieve relevant chunks, then generate an answer.
    """
    print(f"\n{'='*50}")
    print(f"Question: {question}")
    print(f"{'='*50}")

    # Step A: Retrieve relevant chunks
    print("\nSearching documents...")
    chunks = search_documents(question)

    if not chunks:
        print("No relevant documents found.")
        return

    # Show what was retrieved
    print(f"\nRetrieved {len(chunks)} relevant chunk(s):")
    for i, chunk in enumerate(chunks):
        preview = chunk['content'][:100].replace('\n', ' ')
        print(f"  {i+1}. [{chunk['source']}] {preview}...")

    # Step B: Build the context from retrieved chunks
    context = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['content']}" for c in chunks
    )

    # Step C: Generate answer using GPT-4o
    print("\nGenerating answer...")

    system_prompt = """You are a helpful legal document assistant. You answer questions
about Power of Attorney (POA) documents based ONLY on the provided context.

Rules:
- Only use information from the provided context to answer.
- If the context doesn't contain enough information, say so clearly.
- Always mention which source document (PA or IL) the information comes from.
- Be precise about legal details - do not paraphrase legal terms loosely.
- If PA and IL differ on something, highlight the differences."""

    response = openai_client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Context from POA documents:

{context}

---

Question: {question}

Please answer based on the context above."""}
        ],
        temperature=0.3,       # Lower = more factual, less creative
        max_tokens=1000,
    )

    answer = response.choices[0].message.content
    print(f"\nAnswer:\n{answer}")
    return answer


# -- Interactive Loop --
if __name__ == "__main__":
    print("+" + "="*48 + "+")
    print("|  POA Document RAG Assistant                |")
    print("|  Ask questions about your PA & IL POA      |")
    print("|  Type 'quit' to exit                       |")
    print("+" + "="*48 + "+")

    while True:
        question = input("\nYour question: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not question:
            continue
        ask_question(question)

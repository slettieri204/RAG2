"""
Step 2: Chunk the extracted text, generate embeddings, and upload to Azure AI Search.
Creates the search index with semantic search enabled.
"""

import os
import glob
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticSearch,
    SemanticPrioritizedFields,
    SemanticField,
)

load_dotenv()

# -- Configuration --
INDEX_NAME = os.environ["AZURE_SEARCH_INDEX_NAME"]
CHUNK_SIZE = 1000      # characters per chunk
CHUNK_OVERLAP = 200    # overlap between chunks
EMBEDDING_DIMENSIONS = 1536  # for text-embedding-ada-002

# -- Clients --
openai_client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-06-01",
)

search_index_client = SearchIndexClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]),
)

search_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]),
)


# -- Step 2a: Create the Search Index --
def create_search_index():
    """Creates the Azure AI Search index with vector search and semantic ranking."""

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True,
                     filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="source_file", type=SearchFieldDataType.String,
                     filterable=True),
        SimpleField(name="chunk_index", type=SearchFieldDataType.Int32,
                     filterable=True, sortable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=EMBEDDING_DIMENSIONS,
            vector_search_profile_name="my-vector-profile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(name="my-hnsw"),
        ],
        profiles=[
            VectorSearchProfile(
                name="my-vector-profile",
                algorithm_configuration_name="my-hnsw",
            ),
        ],
    )

    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            content_fields=[SemanticField(field_name="content")],
        ),
    )

    semantic_search = SemanticSearch(configurations=[semantic_config])

    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search,
    )

    # Create or update the index
    search_index_client.create_or_update_index(index)
    print(f"Search index '{INDEX_NAME}' created/updated.")


# -- Step 2b: Chunk the Text --
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
    return [c for c in chunks if c]  # Remove empty chunks


# -- Step 2c: Generate Embeddings --
def get_embedding(text):
    """Get embedding vector for a text string."""
    response = openai_client.embeddings.create(
        input=text,
        model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"],
    )
    return response.data[0].embedding


# -- Step 2d: Process and Upload --
def process_and_upload():
    """Read extracted files, chunk them, embed them, upload to search index."""

    extracted_files = glob.glob("extracted/*.md")
    print(f"Found {len(extracted_files)} extracted file(s)")

    all_documents = []

    for filepath in extracted_files:
        filename = os.path.basename(filepath)
        print(f"\nProcessing: {filename}")

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        print(f"  -> Split into {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            print(f"  -> Embedding chunk {i+1}/{len(chunks)}...", end="\r")

            embedding = get_embedding(chunk)

            doc = {
                "id": f"{filename}-chunk-{i}".replace(" ", "-").replace(".", "-"),
                "content": chunk,
                "source_file": filename,
                "chunk_index": i,
                "content_vector": embedding,
            }
            all_documents.append(doc)

        print(f"  -> Embedded {len(chunks)} chunks          ")

    # Upload in batches of 100
    print(f"\nUploading {len(all_documents)} document(s) to search index...")
    batch_size = 100
    for i in range(0, len(all_documents), batch_size):
        batch = all_documents[i:i + batch_size]
        result = search_client.upload_documents(documents=batch)
        succeeded = sum(1 for r in result if r.succeeded)
        print(f"  -> Batch {i//batch_size + 1}: {succeeded}/{len(batch)} succeeded")

    print(f"\nAll {len(all_documents)} chunks indexed successfully.")


# -- Run Everything --
if __name__ == "__main__":
    print("=" * 50)
    print("STEP 2: Creating index and uploading documents")
    print("=" * 50)
    create_search_index()
    process_and_upload()

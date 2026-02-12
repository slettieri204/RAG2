"""
Step 1: Use Azure Document Intelligence to extract text from POA documents.
Outputs extracted text as Markdown files in the 'extracted/' folder.
"""

import os
import glob
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentContentFormat

load_dotenv()

# Connect to Document Intelligence
client = DocumentIntelligenceClient(
    endpoint=os.environ["AZURE_DOCINTEL_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_DOCINTEL_KEY"])
)

# Create output folder
os.makedirs("extracted", exist_ok=True)

# Process each file in the docs/ folder
doc_files = glob.glob("docs/*")
print(f"Found {len(doc_files)} file(s) in docs/")

for filepath in doc_files:
    filename = os.path.basename(filepath)
    print(f"\nProcessing: {filename}")

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    # Determine content type
    ext = filename.lower().split(".")[-1]
    content_type_map = {
        "pdf": "application/pdf",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "tiff": "image/tiff",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    content_type = content_type_map.get(ext, "application/octet-stream")

    # Analyze the document using the Layout model (best for structured docs)
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=file_bytes,
        content_type=content_type,
        output_content_format=DocumentContentFormat.MARKDOWN,
    )
    result = poller.result()

    # Save extracted Markdown
    output_path = f"extracted/{filename}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.content)

    print(f"  -> Saved to {output_path}")
    print(f"  -> Extracted {len(result.content)} characters")

print("\nAll documents extracted. Check the 'extracted/' folder.")

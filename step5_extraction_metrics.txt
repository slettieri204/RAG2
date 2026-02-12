"""
step5_extraction_metrics.py

Analyzes the quality of Document Intelligence extraction across all documents.
Produces a summary table with metrics like:
- Characters extracted
- Pages analyzed
- Tables detected
- Checkboxes/selection marks found
- Structure elements (headings, paragraphs)
- Confidence scores (where available)

Also runs a "field completeness" check using GPT-4o to assess how many
expected POA fields were successfully extracted from each document.

Output:
  - extraction_metrics/metrics_summary.csv
  - extraction_metrics/metrics_summary.json
  - Prints a formatted table to console
"""

import os
import glob
import json
import csv
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentContentFormat
from openai import AzureOpenAI

load_dotenv()

# -- Clients --
doc_client = DocumentIntelligenceClient(
    endpoint=os.environ["AZURE_DOCINTEL_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_DOCINTEL_KEY"])
)

openai_client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-06-01",
)

os.makedirs("extraction_metrics", exist_ok=True)


def get_content_type(filename):
    ext = filename.lower().split(".")[-1]
    return {
        "pdf": "application/pdf",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "tiff": "image/tiff",
    }.get(ext, "application/octet-stream")


def count_checkboxes(content):
    """Count checked and unchecked checkboxes in extracted markdown."""
    checked = content.count("☒") + content.count(":selected:") + content.count("[x]") + content.count("[X]")
    unchecked = content.count("☐") + content.count(":unselected:") + content.count("[ ]")
    return checked, unchecked


def count_tables(content):
    """Estimate table count from markdown pipe characters."""
    lines = content.split("\n")
    table_lines = [l for l in lines if l.strip().startswith("|") and l.strip().endswith("|")]
    # A table needs at least a header + separator + one row = 3 lines
    if len(table_lines) >= 3:
        # Count distinct tables by finding gaps between table lines
        tables = 1
        in_table = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                if not in_table:
                    tables += 1 if in_table == False and tables > 1 else 0
                in_table = True
            else:
                if in_table and stripped == "":
                    in_table = False
        return max(1, tables) if table_lines else 0
    return 1 if table_lines else 0


def count_headings(content):
    """Count markdown headings."""
    lines = content.split("\n")
    return len([l for l in lines if l.strip().startswith("#")])


def assess_field_completeness(content, filename):
    """
    Use GPT-4o to assess what percentage of expected POA fields
    were successfully extracted from the document.
    """
    response = openai_client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document extraction quality assessor. "
                    "Given extracted text from a Power of Attorney document, "
                    "assess which standard fields are present and which are missing. "
                    "Return ONLY valid JSON with no markdown or backticks."
                )
            },
            {
                "role": "user",
                "content": f"""Analyze this extracted POA document text and assess field completeness.

For each field below, mark it as "found" (true/false) based on whether the extracted text
contains that information. Also provide a brief extracted value or "NOT FOUND".

Return JSON in this exact format:
{{
  "fields": {{
    "principal_name": {{"found": true/false, "value": "..."}},
    "principal_address": {{"found": true/false, "value": "..."}},
    "agent_name": {{"found": true/false, "value": "..."}},
    "agent_address": {{"found": true/false, "value": "..."}},
    "agent_relationship": {{"found": true/false, "value": "..."}},
    "successor_agent": {{"found": true/false, "value": "..."}},
    "document_type": {{"found": true/false, "value": "..."}},
    "governing_state": {{"found": true/false, "value": "..."}},
    "governing_statute": {{"found": true/false, "value": "..."}},
    "powers_granted": {{"found": true/false, "value": "summary of powers"}},
    "effective_date": {{"found": true/false, "value": "..."}},
    "execution_date": {{"found": true/false, "value": "..."}},
    "witness_names": {{"found": true/false, "value": "..."}},
    "notary_info": {{"found": true/false, "value": "..."}},
    "signature_blocks": {{"found": true/false, "value": "present/not present"}},
    "checkboxes_or_selections": {{"found": true/false, "value": "number found or N/A"}}
  }},
  "fields_found": <count of found fields>,
  "fields_total": 16,
  "completeness_pct": <percentage>,
  "quality_notes": "brief notes on extraction quality issues if any"
}}

--- EXTRACTED DOCUMENT TEXT ---
Filename: {filename}

{content[:6000]}"""
            }
        ],
        temperature=0.1,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"fields_found": 0, "fields_total": 16, "completeness_pct": 0,
                "quality_notes": "Failed to parse GPT assessment"}


def analyze_document(filepath):
    """Run full extraction analysis on a single document."""
    filename = os.path.basename(filepath)
    print(f"\nAnalyzing: {filename}")

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    file_size_kb = len(file_bytes) / 1024
    content_type = get_content_type(filename)

    # Run Document Intelligence
    poller = doc_client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=file_bytes,
        content_type=content_type,
        output_content_format=DocumentContentFormat.MARKDOWN,
    )
    result = poller.result()

    content = result.content
    chars = len(content)

    # Count pages
    pages = len(result.pages) if result.pages else 0

    # Word-level confidence (average across all pages)
    word_confidences = []
    if result.pages:
        for page in result.pages:
            if page.words:
                for word in page.words:
                    if hasattr(word, 'confidence') and word.confidence is not None:
                        word_confidences.append(word.confidence)

    avg_confidence = sum(word_confidences) / len(word_confidences) if word_confidences else None
    min_confidence = min(word_confidences) if word_confidences else None
    low_conf_words = len([c for c in word_confidences if c < 0.8]) if word_confidences else 0

    # Count structure elements
    checked, unchecked = count_checkboxes(content)
    tables = count_tables(content)
    headings = count_headings(content)
    paragraphs = len([p for p in content.split("\n\n") if p.strip()])

    # Count selection marks from the API result directly
    selection_marks = 0
    if result.pages:
        for page in result.pages:
            if hasattr(page, 'selection_marks') and page.selection_marks:
                selection_marks += len(page.selection_marks)

    # Field completeness via GPT-4o
    print(f"  Assessing field completeness...")
    field_assessment = assess_field_completeness(content, filename)

    metrics = {
        "filename": filename,
        "file_size_kb": round(file_size_kb, 1),
        "file_type": content_type.split("/")[-1].upper(),
        "pages": pages,
        "chars_extracted": chars,
        "words_analyzed": len(word_confidences),
        "avg_word_confidence": round(avg_confidence, 4) if avg_confidence else "N/A",
        "min_word_confidence": round(min_confidence, 4) if min_confidence else "N/A",
        "low_confidence_words": low_conf_words,
        "low_confidence_pct": round(low_conf_words / len(word_confidences) * 100, 1) if word_confidences else "N/A",
        "headings_detected": headings,
        "tables_detected": tables,
        "paragraphs": paragraphs,
        "checkboxes_checked": checked,
        "checkboxes_unchecked": unchecked,
        "selection_marks_api": selection_marks,
        "fields_found": field_assessment.get("fields_found", "N/A"),
        "fields_total": field_assessment.get("fields_total", 16),
        "field_completeness_pct": field_assessment.get("completeness_pct", "N/A"),
        "quality_notes": field_assessment.get("quality_notes", ""),
    }

    # Save individual field assessment
    detail_path = f"extraction_metrics/{filename}_fields.json"
    with open(detail_path, "w", encoding="utf-8") as f:
        json.dump(field_assessment, f, indent=2)

    print(f"  Pages: {pages} | Chars: {chars} | Words: {len(word_confidences)}")
    if avg_confidence:
        print(f"  Avg confidence: {avg_confidence:.2%} | Low-conf words: {low_conf_words}")
    print(f"  Checkboxes: {checked} checked, {unchecked} unchecked | Selection marks (API): {selection_marks}")
    print(f"  Field completeness: {field_assessment.get('completeness_pct', 'N/A')}%")

    return metrics


def print_summary_table(all_metrics):
    """Print a formatted summary table."""

    print("\n" + "=" * 120)
    print("  EXTRACTION QUALITY METRICS SUMMARY")
    print("=" * 120)

    # Header
    print(f"\n{'Document':<45} {'Pages':>5} {'Chars':>7} {'Confidence':>11} {'Low-Conf%':>10} "
          f"{'Checks':>7} {'Fields':>8} {'Complete%':>10}")
    print("-" * 120)

    for m in all_metrics:
        name = m['filename'][:44]
        conf = f"{m['avg_word_confidence']:.2%}" if isinstance(m['avg_word_confidence'], float) else m['avg_word_confidence']
        low_pct = f"{m['low_confidence_pct']}%" if isinstance(m['low_confidence_pct'], (int, float)) else m['low_confidence_pct']
        checks = f"{m['checkboxes_checked']}✓/{m['checkboxes_unchecked']}✗"
        fields = f"{m['fields_found']}/{m['fields_total']}"
        complete = f"{m['field_completeness_pct']}%" if m['field_completeness_pct'] != "N/A" else "N/A"

        print(f"{name:<45} {m['pages']:>5} {m['chars_extracted']:>7} {conf:>11} {low_pct:>10} "
              f"{checks:>7} {fields:>8} {complete:>10}")

    print("-" * 120)

    # Overall stats
    confidences = [m['avg_word_confidence'] for m in all_metrics
                   if isinstance(m['avg_word_confidence'], float)]
    completeness = [m['field_completeness_pct'] for m in all_metrics
                    if isinstance(m['field_completeness_pct'], (int, float))]

    if confidences:
        print(f"\n  Overall avg word confidence:  {sum(confidences)/len(confidences):.2%}")
    if completeness:
        print(f"  Overall avg field completeness: {sum(completeness)/len(completeness):.1f}%")

    total_checks = sum(m['checkboxes_checked'] + m['checkboxes_unchecked'] for m in all_metrics)
    print(f"  Total checkboxes detected:     {total_checks}")
    print(f"  Total documents analyzed:      {len(all_metrics)}")


def main():
    print("=" * 60)
    print("  EXTRACTION QUALITY METRICS ANALYSIS")
    print("=" * 60)

    doc_files = sorted(glob.glob("docs/*"))
    doc_files = [f for f in doc_files if not f.endswith('.py')]  # Skip any scripts

    if not doc_files:
        print("ERROR: No files found in docs/ folder.")
        return

    print(f"Found {len(doc_files)} document(s) to analyze")

    all_metrics = []
    for filepath in doc_files:
        try:
            metrics = analyze_document(filepath)
            all_metrics.append(metrics)
        except Exception as e:
            print(f"  ERROR analyzing {filepath}: {e}")
            all_metrics.append({
                "filename": os.path.basename(filepath),
                "file_size_kb": 0, "file_type": "ERROR", "pages": 0,
                "chars_extracted": 0, "words_analyzed": 0,
                "avg_word_confidence": "ERROR", "min_word_confidence": "ERROR",
                "low_confidence_words": 0, "low_confidence_pct": "N/A",
                "headings_detected": 0, "tables_detected": 0, "paragraphs": 0,
                "checkboxes_checked": 0, "checkboxes_unchecked": 0,
                "selection_marks_api": 0,
                "fields_found": 0, "fields_total": 16,
                "field_completeness_pct": 0,
                "quality_notes": f"Extraction failed: {str(e)}"
            })

    # Print summary table
    print_summary_table(all_metrics)

    # Save JSON
    json_path = "extraction_metrics/metrics_summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=2)
    print(f"\n  JSON saved: {json_path}")

    # Save CSV
    csv_path = "extraction_metrics/metrics_summary.csv"
    if all_metrics:
        keys = all_metrics[0].keys()
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_metrics)
    print(f"  CSV saved:  {csv_path}")

    # Save per-field detail
    print(f"  Per-document field details saved in extraction_metrics/")

    print(f"\n{'='*60}")
    print(f"  Done! Use the CSV or JSON for your summary table.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

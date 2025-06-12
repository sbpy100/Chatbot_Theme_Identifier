import os
from PyPDF2 import PdfReader
from app.core.utils import extract_text_ocr, embed_and_store, search_vectors

def process_docs(files):
    processed = []

    # Ensure the data folder exists
    data_dir = os.path.join("backend", "data")
    os.makedirs(data_dir, exist_ok=True)

    for file in files:
        filename = file.filename
        filepath = os.path.join(data_dir, filename)
        file.save(filepath)

        text = extract_text_ocr(filepath)
        embed_and_store(text, filename)

        processed.append({"file": filename, "status": "processed"})
    
    return processed

from app.core.utils import search_vectors
def query_documents(question):
    raw_results, chunks = search_vectors(question, top_k=3)

    citations = []
    for item in raw_results:
        citation_info = {
            "doc_id": item["doc_id"],
            "text": item["text"],
            "citation": f"Page {item['page']}"
        }
        citations.append(citation_info)

    return citations, chunks


from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create FAISS index (384 dimensions for this model)
index = faiss.IndexFlatL2(384)

# Global lists to hold chunks and metadata
text_chunks = []
metadata = []

import os
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image

# ✅ Hardcode Tesseract path (safe for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_ocr(path):
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        chunks = []
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 20]
                for para in paragraphs:
                    chunks.append((page_num + 1, para))  # 1-based page number
        return chunks  # List of (page, para_text)

    else:
        # ✅ Handle image input with preprocessing
        try:
            # Check if Tesseract exists
            if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
                raise EnvironmentError("❌ Tesseract OCR is not installed or path is invalid.")

            image = Image.open(path).convert("L")  # Grayscale improves OCR
            text = pytesseract.image_to_string(image, config="--psm 6")  # PSM 6 = assume block of text

            if not text.strip():
                print(f"⚠️ No text detected in image: {path}")
                return []

            return [(1, text.strip())]

        except Exception as e:
            print(f"❌ Error during OCR on image '{path}': {e}")
            return []


# def extract_text_ocr(path):
#     if path.endswith(".pdf"):
#         reader = PdfReader(path)
#         chunks = []
#         for page_num, page in enumerate(reader.pages):
#             text = page.extract_text()
#             if text:
#                 paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 20]
#                 for para in paragraphs:
#                     chunks.append((page_num + 1, para))  #1-based page number
#         return chunks  # List of (page, para_text)
#     else:
#         text = pytesseract.image_to_string(Image.open(path))
#         return [(1, text)]


def embed_and_store(paged_chunks, doc_id):
    global text_chunks, metadata

    texts = [chunk[1] for chunk in paged_chunks]
    pages = [chunk[0] for chunk in paged_chunks]
    
    vectors = model.encode(texts)
    index.add(np.array(vectors))

    text_chunks.extend(texts)
    metadata.extend([(doc_id, pages[i]) for i in range(len(paged_chunks))])



def search_vectors(query, top_k=3):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), top_k)

    results = []
    selected_chunks = []

    for i in I[0]:
        if i < len(text_chunks):
            doc_id, page_num = metadata[i]
            text = text_chunks[i]
            results.append({
                "doc_id": doc_id,
                "page": page_num,
                "text": text
            })
            selected_chunks.append(text)

    return results, selected_chunks

from flask import Blueprint, request, jsonify
from app.services.doc_processor import process_docs, query_documents
from app.models.huggingface_model import summarize_themes

#  Define the blueprint correctly
api_bp = Blueprint("api", __name__)

@api_bp.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    result = process_docs(files)
    return jsonify({"status": "success", "details": result})

@api_bp.route('/query', methods=['POST'])
def query():
    question = request.json.get('question')
    citations, chunks = query_documents(question)
    themes = summarize_themes(chunks, question)
    return jsonify({"citations": citations, "themes": themes})

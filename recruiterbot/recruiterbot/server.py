import os
from flask import Flask, request, jsonify, send_from_directory
from app.graph import ask
from app.utils.upload import save_pdf, list_pdfs, delete_pdf

app = Flask(__name__, static_folder="static", static_url_path="")

MAX_QUESTION_LENGTH = 500  # basic abuse guard — reject absurdly long inputs


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Question is required"}), 400
    if len(question) > MAX_QUESTION_LENGTH:
        return jsonify({"error": "Question is too long"}), 400

    try:
        answer = ask(question)
    except Exception:
        # Never leak internal stack traces / API errors to the client
        app.logger.exception("Error handling chat request")
        return jsonify({"error": "Something went wrong processing that question"}), 500

    return jsonify({"answer": answer})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/upload", methods=["POST"])
def upload_pdf():
    """Upload a PDF file to the data directory."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    result = save_pdf(file)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@app.route("/api/pdfs", methods=["GET"])
def get_pdfs():
    """List all uploaded PDF files."""
    pdfs = list_pdfs()
    return jsonify({"pdfs": pdfs})


@app.route("/api/delete-pdf", methods=["POST"])
def delete_pdf_endpoint():
    """Delete a PDF file."""
    data = request.get_json(silent=True) or {}
    filename = data.get("filename", "").strip()
    
    if not filename:
        return jsonify({"error": "Filename is required"}), 400
    
    result = delete_pdf(filename)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))  # 7860 is HF Spaces' default port
    app.run(host="0.0.0.0", port=port, debug=False)
    
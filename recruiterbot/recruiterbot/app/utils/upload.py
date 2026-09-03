import os
from werkzeug.utils import secure_filename
from app.utils.retriever import reset_vectorstore

# Resolve data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_pdf(file, filename: str = None) -> dict:
    """
    Save uploaded PDF to data directory.
    
    Args:
        file: werkzeug FileStorage object from Flask request
        filename: optional override filename
    
    Returns:
        dict with success status and message
    """
    if not file or file.filename == '':
        return {"success": False, "error": "No file selected"}
    
    if not allowed_file(file.filename):
        return {"success": False, "error": "Only PDF files are allowed"}
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return {"success": False, "error": f"File too large (max {MAX_FILE_SIZE / 1024 / 1024}MB)"}
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Use provided filename or sanitize the uploaded one
        safe_filename = secure_filename(filename) if filename else secure_filename(file.filename)
        
        # Ensure .pdf extension
        if not safe_filename.lower().endswith('.pdf'):
            safe_filename += '.pdf'
        
        filepath = os.path.join(DATA_DIR, safe_filename)
        file.save(filepath)
        reset_vectorstore()
        
        return {
            "success": True,
            "message": f"PDF '{safe_filename}' uploaded successfully",
            "filename": safe_filename
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to save file: {str(e)}"}


def list_pdfs() -> list:
    """List all PDF files in data directory."""
    if not os.path.exists(DATA_DIR):
        return []
    
    return [f for f in os.listdir(DATA_DIR) if f.lower().endswith('.pdf')]


def delete_pdf(filename: str) -> dict:
    """Delete a PDF file from data directory."""
    safe_filename = secure_filename(filename)
    filepath = os.path.join(DATA_DIR, safe_filename)
    
    if not os.path.exists(filepath):
        return {"success": False, "error": "File not found"}
    
    try:
        os.remove(filepath)
        reset_vectorstore()
        return {"success": True, "message": f"PDF '{safe_filename}' deleted"}
    except Exception as e:
        return {"success": False, "error": f"Failed to delete file: {str(e)}"}

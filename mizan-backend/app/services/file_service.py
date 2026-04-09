# File upload service — handles all file ingestion for Mizan with Cloudinary storage
#
# Responsibilities:
#   - Receive UploadFile from FastAPI multipart form request
#   - Validate file type (CSV or image) and size before processing
#   - Upload CSV files to Cloudinary (mizan/classes/{class_id}/csv/) and return secure_url
#   - Upload student photos to Cloudinary (mizan/classes/{class_id}/photos/) and return secure_url
#   - Parse CSV content in-memory (from bytes) BEFORE or AFTER upload — never from disk
#   - Return (secure_url, parsed_rows) tuple to the calling route or service
#   - No local file storage anywhere — temp files and os.path usage are forbidden

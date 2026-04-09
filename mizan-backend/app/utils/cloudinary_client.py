# Cloudinary client setup and file upload utilities for Mizan
#
# All file storage goes through Cloudinary — no files are ever saved locally.
# This module handles:
#
# 1. CSV files (schedules, exams, projects, trombinoscope):
#    - Uploaded as raw files to Cloudinary
#    - Organized under: mizan/classes/{class_id}/csv/
#    - Example URL: https://res.cloudinary.com/.../mizan/classes/42/csv/emploi_du_temps.csv
#
# 2. Student photos (trombinoscope):
#    - Uploaded as images to Cloudinary
#    - Organized under: mizan/classes/{class_id}/photos/
#    - Example URL: https://res.cloudinary.com/.../mizan/classes/42/photos/student_123.jpg
#    - Auto-optimized on upload (format, quality)
#
# 3. Database storage:
#    - Only the Cloudinary secure_url string is persisted in the database
#    - The actual file bytes are never written to disk or stored in the DB
#
# Usage:
#   upload_csv(file_bytes, class_id, filename) -> secure_url: str
#   upload_photo(file_bytes, class_id, student_id) -> secure_url: str

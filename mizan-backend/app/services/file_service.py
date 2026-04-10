# app/services/file_service.py
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings

settings = get_settings()

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


async def upload_photo_to_cloudinary(file: UploadFile, public_id: str) -> str:
    try:
        full_public_id = f"mizan/students/{public_id}"
        result = cloudinary.uploader.upload(
            file.file,
            public_id=full_public_id,
            overwrite=True
        )
        return result.get("secure_url")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )


async def delete_photo_from_cloudinary(public_id: str) -> None:
    try:
        full_public_id = f"mizan/students/{public_id}"
        cloudinary.uploader.destroy(full_public_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete image: {str(e)}"
        )


def validate_csv_file(file: UploadFile) -> None:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a .csv"
        )
    
    if file.size and file.size > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 5MB limit"
        )


def validate_image_file(file: UploadFile) -> None:
    valid_extensions = (".jpg", ".jpeg", ".png")
    if not file.filename.lower().endswith(valid_extensions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a .jpg, .jpeg, or .png"
        )
    
    if file.size and file.size > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 2MB limit"
        )
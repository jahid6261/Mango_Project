
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from src.utils.settings import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


async def upload_image(image: UploadFile):
    result = cloudinary.uploader.upload(
        image.file,
        folder="products",
    )

    return {
        "image_url": result["secure_url"],
        "public_id": result["public_id"],
    }


async def delete_image(public_id: str):
    result = cloudinary.uploader.destroy(public_id)

    if result.get("result") != "ok":
        raise Exception("Image deletion failed.")

    return result


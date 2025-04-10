import os
import shutil
import logging
from fastapi import UploadFile
import uuid
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self, base_path: str = "data/audio"):
        self.base_path = base_path
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Ensure the base directory exists"""
        Path(self.base_path).mkdir(parents=True, exist_ok=True)

    async def save_audio_file(self, file: UploadFile, call_id: uuid.UUID) -> str:
        """
        Save an uploaded audio file to the storage directory
        Returns the relative path to the saved file
        """
        try:
            # Generate unique filename
            file_extension = file.filename.split('.')[-1]
            filename = f"{call_id}.{file_extension}"
            file_path = os.path.join(self.base_path, filename)

            # Save the file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            logger.info(f"File saved successfully: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise

    def get_file_path(self, call_id: uuid.UUID) -> Optional[str]:
        """
        Get the path to a stored audio file
        Returns None if file doesn't exist
        """
        try:
            # Check for common audio extensions
            extensions = ['.wav', '.mp3', '.ogg']
            for ext in extensions:
                file_path = os.path.join(self.base_path, f"{call_id}{ext}")
                if os.path.exists(file_path):
                    return file_path
            return None

        except Exception as e:
            logger.error(f"Error getting file path: {str(e)}")
            raise

    def delete_file(self, call_id: uuid.UUID) -> bool:
        """
        Delete a stored audio file
        Returns True if file was deleted, False if file didn't exist
        """
        try:
            file_path = self.get_file_path(call_id)
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted successfully: {file_path}")
                return True
            return False

        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise

# Create a singleton instance
storage_service = StorageService()

# Export the save_audio_file function for use in routers
async def save_audio_file(file: UploadFile, call_id: uuid.UUID) -> str:
    return await storage_service.save_audio_file(file, call_id) 
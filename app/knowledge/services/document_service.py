from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.knowledge.models.document import Document
from app.knowledge.repos.document_repository import DocumentRepository
from app.knowledge.enums import DocumentStatus


UPLOAD_DIR = Path("uploads")


class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
    ):
        self.repository = repository


    async def upload_document(
        self,
        file: UploadFile,
        user_id: str,
    ) -> Document:

        # Create upload directory
        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )


        # Generate unique filename
        if file.filename is None:
            raise ValueError("Uploaded file has no valid filename.")
        
        extension = Path(
            file.filename
        ).suffix

        stored_filename = (
            f"{uuid4()}{extension}"
        )


        file_path = (
            UPLOAD_DIR / stored_filename
        )


        # Save file
        content = await file.read()

        file_path.write_bytes(
            content
        )


        # Create DB record
        document = Document(
            filename=stored_filename,
            original_filename=file.filename,
            content_type=file.content_type,
            file_size=len(content),
            storage_path=str(file_path),
            status=DocumentStatus.UPLOADED,
            uploaded_by=user_id,
        )


        return await self.repository.create(
            document
        )
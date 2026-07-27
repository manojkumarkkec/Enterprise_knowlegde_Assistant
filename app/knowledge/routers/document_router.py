from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    UploadFile,
    File,
    status,
)

from app.auth.security.jwt_auth import get_current_user
from app.auth.models.user import User

from app.knowledge.services.document_service import DocumentService
from app.knowledge.repos.document_repository import DocumentRepository
from app.knowledge.tasks import process_document
from app.shared.dependencies import get_db_session

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


def get_document_service(
    session: AsyncSession = Depends(get_db_session),
):

    repository = DocumentRepository(
        session
    )

    return DocumentService(
        repository
    )


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    

    current_user: User = Depends(
        get_current_user
    ),

    service: DocumentService = Depends(
        get_document_service
    ),
):

    document = await service.upload_document(
        file=file,
        user_id=str(current_user.id),
        
    )

    background_tasks.add_task(
            process_document,
            document.id
        )


    return {
        "id": str(document.id),
        "filename": document.original_filename,
        "status": document.status,
    }
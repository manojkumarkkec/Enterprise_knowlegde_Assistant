from enum import Enum

class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    CHUNKED = "chunked"
    INDEXED = "indexed"
    FAILED = "failed"
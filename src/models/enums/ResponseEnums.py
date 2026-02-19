from enum import Enum

class ResponseSignal(Enum):
    FILE_VALID_SUCCESS = 'File is valid'
    FILE_TYPE_NOT_SUPPORTED = 'Invalid file type'
    FILE_SIZE_EXCEEDED = 'File size exceeds limit'
    FILE_UPLOAD_SUCCESS = 'File uploaded successfully'
    FILE_UPLOAD_FAILED = 'File upload failed'
    PROCESSING_FAILED = 'File processing failed'
    PRCESSING_SUCCESS = 'File processed successfully'
 
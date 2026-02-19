from fastapi import APIRouter, Depends, UploadFile, File,status
from fastapi.responses import JSONResponse
import os
import aiofiles
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController,ProcessControler
from models.enums.ResponseEnums import ResponseSignal
import logging
from routes.schemas.data import ProcessRequest

logger = logging.getLogger('uvicorn.error')


data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile , app_settings: Settings = Depends(get_settings)):
    
    is_valed,result_signal=DataController().validate_uploaded_file(file=file)

    if not is_valed:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": result_signal})
    
    #project_dir_path=ProjectController().get_project_path(project_id = project_id)

    #file_path=os.path.join(project_dir_path,file.filename)
    file_path, file_id = DataController().generate_unique_filepath(org_filename=file.filename,
                                                          project_id=project_id)

    logger.info(f"Uploading file: {file.filename}")
    logger.info(f"File path: {file_path}")
    logger.info(f"File ID: {file_id}")
    
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while True:
                chunk = await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE)# create the file
                if not chunk:
                    break
                await f.write(chunk)

    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value,"file_id": file_id})
    
    logger.info(f"File uploaded successfully to {file_path}")
    return JSONResponse(
        content={"Signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value ,
                  "file_id": file_id ,
                  "file_path": file_path}
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    # Placeholder for processing logic
    file_id = process_request.file_id
    chunk_size=process_request.chunk_size
    over_lap_size=process_request.overlap_size
    
    try:
        process_controller = ProcessControler(project_id=project_id)
        file_content = process_controller.get_file_content(file_id=file_id)

        file_chunks = process_controller.process_file_content(
                        file_content=file_content,
                        file_id=file_id,
                        chunk_size=chunk_size,
                        chunk_overlap=over_lap_size)
        
        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"signal": ResponseSignal.PROCESSING_FAILED.value})
        return file_chunks

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"error": "FILE_NOT_FOUND", "message": str(e)})
    except Exception as e:
        logger.error(f"Error processing file: {e}", exc_info=True)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"error": "PROCESSING_ERROR", "message": str(e)})
    
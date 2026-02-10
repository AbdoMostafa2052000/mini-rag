from fastapi import APIRouter, Depends, UploadFile, File,status
from fastapi.responses import JSONResponse
import os
import aiofiles
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models.enums.ResponseEnums import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')


data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile , app_settings: Settings = Depends(get_settings)):
    
    is_valed,result_signal=DataController().validate_uploaded_file(file=file)

    if not is_valed:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": result_signal})
    
    #project_dir_path=ProjectController().get_project_path(project_id = project_id)

    #file_path=os.path.join(project_dir_path,file.filename)
    file_path = DataController().generate_unique_filepath(org_filename=file.filename,
                                                          project_id=project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while True:
                chunk = await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE)# create the file
                if not chunk:
                    break
                await f.write(chunk)

    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value})
    
    return JSONResponse(
        content={"Signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value}
    )

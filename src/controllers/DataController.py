from .BaseController import  BaseController
from fastapi import FastAPI, APIRouter,Depends, UploadFile
from helpers.config import get_settings,Settings
from models import ResponseSignal
from .ProjectController import ProjectController
import os
import re
import uuid
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576

    def validate_uploaded_file(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTNSION:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True,ResponseSignal.FILE_VALID_SUCCESS.value


    def generate_unique_filepath(self, org_filename: str, project_id: str):
        project_path = ProjectController().get_project_path(project_id=project_id)

        # preserve the original filename (but strip any path components)
        filename = os.path.basename(org_filename)

        # prefer the original name if it's available
        new_filepath = os.path.join(project_path, filename)
        if not os.path.exists(new_filepath):
            return new_filepath

        # on collision, fallback to a UUID-prefixed filename until available
        while True:
            random_key = uuid.uuid4().hex
            new_filepath = os.path.join(project_path, f"{random_key}_{filename}")
            if not os.path.exists(new_filepath):
                return new_filepath

    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
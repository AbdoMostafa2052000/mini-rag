from helpers.config import get_settings,Settings
import os
import random
import string
import logging

logger = logging.getLogger(__name__)

class BaseController:
    def __init__(self):
        self.logger = logging.getLogger("uvicorn.error")
        self.app_settings = get_settings()  
        # Get the directory of this file (controllers/)
        controllers_dir = os.path.dirname(__file__)
        # Go up to src/ directory
        src_dir = os.path.dirname(controllers_dir)
        # Build the files directory path
        self.files_dir = os.path.join(src_dir, "assets", "Files")
        
        logger.info(f"Files directory: {self.files_dir}")

    def generate_random_string(self, length=12):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))
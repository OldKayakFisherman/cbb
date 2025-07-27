from dataclasses import dataclass
from dotenv import load_dotenv
from services.files import get_parent_dir
import os

env_path = os.path.join(get_parent_dir(__file__), '.env')

load_dotenv(env_path)

@dataclass
class AppSettings:


    db_user: str = None
    db_password: str = None
    database: str = None
    db_host: str = None
    db_port: int = 5432
    db_schema: str = None
    pipeline_hour_check: int = None
    is_governed: bool = False
    governer_threshold: int = None
    cbp_start_year: int = None
    cbp_end_year: int = None
    pep_year: int = None

    def str_to_bool(self, string_value: str):
        return string_value.lower() in ("yes", "true", "t", "1")
    
    def __init__(self):

        #Check if we are in a container
        if os.getenv("CONTAINER_RUNNING"):
            self.db_host = os.getenv("DB.CONTAINER.HOST")
        else:
            self.db_host = os.getenv("DB.HOST")

        self.db_user = os.getenv("DB.USER")
        self.db_password = os.getenv("DB.PASSWORD")
        self.database = os.getenv("DATABASE")
        self.db_port = int(os.getenv("DB.PORT"))
        self.db_schema = os.getenv("DB.SCHEMA")
        self.pipeline_hour_check = int(os.getenv("PIPELINE.HOUR.CHECK"))
        self.cbp_start_year = int(os.getenv("CBP.START.YEAR"))
        self.cbp_end_year = int(os.getenv("CBP.END.YEAR"))
        self.pep_year = int(os.getenv("PEP.TARGET.YEAR"))

        if os.getenv("PIPELINE.DATA.GOVERNOR.THRESHOLD"):
            self.is_governed = (int(os.getenv("PIPELINE.DATA.GOVERNOR.THRESHOLD")) !=0)
            self.governer_threshold = int(os.getenv("PIPELINE.DATA.GOVERNOR.THRESHOLD"))
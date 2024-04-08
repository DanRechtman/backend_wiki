from src.models.TestDTO import Test
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())

class Base:
    databaseURI = os.environ.get("URI")

    def __init__(self) -> None:
        self.engine = create_engine(self.databaseURI, echo=True)



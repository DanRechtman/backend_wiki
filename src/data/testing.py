
from models.TestDTO import Test
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())

class dataTest:
    '''
    DEMO CLASS for how to use database
    '''
    def __init__(self) -> None:
        self.engine = create_engine(os.environ.get("URI"), echo=True)

    def insertData(self,ip):
        with Session(self.engine) as session:
            test= Test(IP=ip)
            session.add(test)
            session.commit()
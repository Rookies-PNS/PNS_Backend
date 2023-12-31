import __init__
from typing import Optional
from abc import *

from Domains.Entities import Session,SimpleUser
from Applications.Results import Result,Fail
class SessionRepository(metaclass=ABCMeta):

    @abstractclassmethod
    def publish_Session(self,user:SimpleUser) -> Result[Session]:
        pass
    def load_session(self,session_key:str)->Result[Session]:
        pass
    def verify_Session(self,session_key:str)->bool:
        pass
    def delete_Session(self,user:SimpleUser)-> Optional[Fail]:
        pass
from pydantic import BaseModel


class LinkedinInCredentials(BaseModel):
    email : str
    password : str

class LinkedinWithUsername(BaseModel):
    username : str
    email : str
    password : str
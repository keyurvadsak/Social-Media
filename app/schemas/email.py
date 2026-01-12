from pydantic import BaseModel, EmailStr


class Email_Send(BaseModel):
    to_email:EmailStr
    subject:str
    body:str
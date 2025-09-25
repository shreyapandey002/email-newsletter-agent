from pydantic import BaseModel, EmailStr

# Subscriber schemas
class SubscriberCreate(BaseModel):
    name: str
    email: EmailStr

class SubscriberResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True 

# Email sending schema
class EmailRequest(BaseModel):
    html_body: str

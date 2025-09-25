from pydantic import BaseModel, EmailStr

# Subscriber schemas
class SubscriberCreate(BaseModel):
    email: EmailStr

class SubscriberResponse(BaseModel):
    id: int
    email: EmailStr
    is_subscribed: bool

    class Config:
        from_attributes = True 

# Email sending schema
class EmailRequest(BaseModel):
    html_body: str

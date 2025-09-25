import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import SessionLocal, engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mailtrap config from env
MAILTRAP_HOST = os.getenv("MAILTRAP_HOST", "sandbox.smtp.mailtrap.io")
MAILTRAP_PORT = int(os.getenv("MAILTRAP_PORT", 587))
MAILTRAP_USER = os.getenv("MAILTRAP_USER")
MAILTRAP_PASS = os.getenv("MAILTRAP_PASS")


# Subscribe API
@app.post("/subscribe", response_model=schemas.SubscriberResponse)
def subscribe(subscriber: schemas.SubscriberCreate, db: Session = Depends(get_db)):
    return crud.create_subscriber(db, subscriber)


# Send Email API
@app.post("/send-email")
def send_email(request: schemas.EmailRequest, db: Session = Depends(get_db)):
    html_body = request.html_body
    subscribers = crud.get_active_subscribers(db)

    # Setup SMTP connection
    with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
        server.starttls()
        server.login(MAILTRAP_USER, MAILTRAP_PASS)

        for sub in subscribers:
            msg = MIMEMultipart("alternative")
            msg["From"] = "Newsletter <newsletter@example.com>"
            msg["To"] = sub.email
            msg["Subject"] = "Newsletter"

            # Add HTML body
            msg.attach(MIMEText(html_body, "html"))

            server.sendmail(msg["From"], sub.email, msg.as_string())

    return {"message": f"Newsletter sent to {len(subscribers)} subscribers."}

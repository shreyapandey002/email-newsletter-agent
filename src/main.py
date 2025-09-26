import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, crud, schemas
from .db import SessionLocal, engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mailtrap config
MAILTRAP_HOST = os.getenv("MAILTRAP_HOST", "sandbox.smtp.mailtrap.io")
MAILTRAP_PORT = int(os.getenv("MAILTRAP_PORT", 587))
MAILTRAP_USER = os.getenv("MAILTRAP_USER")
MAILTRAP_PASS = os.getenv("MAILTRAP_PASS")

# Subscribe API
@app.post("/subscribe", response_model=schemas.SubscriberResponse)
def subscribe(subscriber: schemas.SubscriberCreate, db: Session = Depends(get_db)):
    return crud.create_subscriber(db, subscriber)

# Send Email API: batch recipients, send JSON payload
@app.post("/send-email")
def send_email(request: schemas.EmailRequest, db: Session = Depends(get_db)):
    html_body = request.html_body
    subscribers = crud.get_active_subscribers(db)

    if not subscribers:
        return {"message": "No subscribers to send email."}

    all_emails = [sub.email for sub in subscribers]

    # Setup SMTP connection
    with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
        server.starttls()
        server.login(MAILTRAP_USER, MAILTRAP_PASS)

        msg = MIMEMultipart("alternative")
        msg["From"] = "Newsletter <newsletter@example.com>"
        msg["To"] = ", ".join(all_emails)  # Batch all recipients
        msg["Subject"] = "Newsletter"
        msg.attach(MIMEText(html_body, "html"))

        try:
            server.sendmail(msg["From"], all_emails, msg.as_string())
            print(f"Newsletter sent to all subscribers: {all_emails}")
        except smtplib.SMTPDataError as e:
            print(f"⚠ Failed to send newsletter: {e}")
            return {"message": "Failed to send newsletter", "error": str(e)}

    return {"message": f"Newsletter sent to {len(subscribers)} subscribers (batched in one email)."}

# crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def create_subscriber(db: Session, subscriber: schemas.SubscriberCreate):
    db_subscriber = models.Subscribers(
        email=subscriber.email,
        is_subscribed=True
    )
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber

def get_active_subscribers(db: Session):
    return db.query(models.Subscribers).filter(models.Subscribers.is_subscribed == True).all()

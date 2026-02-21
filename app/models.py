from app import db
from datetime import datetime
import uuid

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="OPEN")

    created_by = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    assigned_to = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
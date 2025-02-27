from datetime import datetime
from extensions import db

class EmailReceipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    recipient_hash = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(10), default="sent", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

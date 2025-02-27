import uuid
from app.database import db

class EmailTrack(db.Model):
    __tablename__ = "email_tracks"

    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(255), nullable=False)
    uuid = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.Boolean, default=False)  # False = Unread, True = Read

    def __repr__(self):
        return f"<EmailTrack {self.recipient} - {self.status}>"

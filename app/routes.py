from flask import Blueprint, request, send_file, jsonify
from app.database import db
from app.models import EmailTrack
from app.image_generator import generate_read_receipt

routes = Blueprint("routes", __name__)

@routes.route("/generate", methods=["GET"])
def generate_uuid():
    recipient = request.args.get("recipient")
    if not recipient:
        return jsonify({"error": "Recipient email required"}), 400

    entry = EmailTrack(recipient=recipient)
    db.session.add(entry)
    db.session.commit()

    tracking_url = f"http://localhost:5000/track/{entry.uuid}.png"
    return jsonify({"uuid": entry.uuid, "tracking_url": tracking_url})

@routes.route("/track/<uuid>.png", methods=["GET"])
def track_email(uuid):
    entry = EmailTrack.query.filter_by(uuid=uuid).first()
    if entry:
        entry.status = True
        db.session.commit()
    return send_file(generate_read_receipt(entry.status), mimetype="image/png")

@routes.route("/status", methods=["GET"])
def get_status():
    emails = EmailTrack.query.all()
    return jsonify([{ "recipient": e.recipient, "uuid": e.uuid, "status": e.status } for e in emails])

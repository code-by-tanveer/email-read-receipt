import uuid
import hashlib
from flask import request, jsonify, send_from_directory
from models import EmailReceipt
from extensions import db

def init_routes(app):

    @app.route('/generate', methods=['GET'])
    def generate():
        recipient = request.args.get('recipient')
        if not recipient:
            return jsonify({"error": "Missing recipient parameter"}), 400

        new_uuid = str(uuid.uuid4())
        recipient_hash = hashlib.sha256(recipient.encode()).hexdigest()

        receipt = EmailReceipt(uuid=new_uuid, recipient_hash=recipient_hash, status="sent")
        db.session.add(receipt)
        db.session.commit()

        image_url = f"{request.host_url.rstrip('/')}/tick?uuid={new_uuid}&recipient={recipient_hash}"
        return jsonify({"uuid": new_uuid, "image_url": image_url})

    @app.route('/tick', methods=['GET'])
    def tick():
        uid = request.args.get('uuid')
        recipient_token = request.args.get('recipient')
        if not uid or not recipient_token:
            return jsonify({"error": "Missing parameters"}), 400

        receipt = EmailReceipt.query.filter_by(uuid=uid, recipient_hash=recipient_token).first()
        if not receipt:
            return jsonify({"error": "Record not found"}), 404

        if receipt.status != "read":
            receipt.status = "read"
            db.session.commit()

        image_file = 'blue.png' if receipt.status == "read" else 'grey.png'
        return send_from_directory('static', image_file, mimetype='image/png')

    @app.route('/records', methods=['GET'])
    def records():
        receipts = EmailReceipt.query.all()
        data = [{
            "uuid": rec.uuid,
            "status": rec.status,
            "created_at": rec.created_at.isoformat(),
            "updated_at": rec.updated_at.isoformat() if rec.updated_at else None
        } for rec in receipts]
        return jsonify(data)

    @app.route('/record/<string:uid>', methods=['GET'])
    def record(uid):
        receipt = EmailReceipt.query.filter_by(uuid=uid).first()
        if not receipt:
            return jsonify({"error": "Record not found"}), 404
        return jsonify({
            "uuid": receipt.uuid,
            "status": receipt.status,
            "created_at": receipt.created_at.isoformat(),
            "updated_at": receipt.updated_at.isoformat() if receipt.updated_at else None
        })

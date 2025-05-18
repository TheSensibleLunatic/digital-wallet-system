from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Transaction
from app import db
from app.utils.fraud_detection import check_transfer_fraud, check_large_withdrawal

wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
    data = request.get_json()
    amount = data.get('amount')

    if amount is None or amount <= 0:
        return jsonify({"message": "Invalid deposit amount"}), 400

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    user.balance += amount

    txn = Transaction(user_id=user.id, type='deposit', amount=amount)
    db.session.add(txn)
    db.session.commit()

    return jsonify({"message": f"{amount} deposited successfully"}), 200


@wallet_bp.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    data = request.get_json()
    amount = data.get('amount')

    if amount is None or amount <= 0:
        return jsonify({"message": "Invalid withdraw amount"}), 400

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.balance < amount:
        return jsonify({"message": "Insufficient balance"}), 400

    user.balance -= amount
    txn = Transaction(user_id=user.id, type='withdraw', amount=amount)

    # Check for large withdrawal fraud
    check_large_withdrawal(txn)

    db.session.add(txn)
    db.session.commit()

    return jsonify({"message": f"{amount} withdrawn successfully"}), 200


@wallet_bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    data = request.get_json()
    recipient_username = data.get('to')
    amount = data.get('amount')

    if amount is None or amount <= 0:
        return jsonify({"message": "Invalid transfer amount"}), 400

    sender_id = get_jwt_identity()
    sender = User.query.get(sender_id)
    recipient = User.query.filter_by(username=recipient_username).first()

    if not recipient:
        return jsonify({"message": "Recipient not found"}), 404

    if sender.balance < amount:
        return jsonify({"message": "Insufficient balance"}), 400

    sender.balance -= amount
    recipient.balance += amount

    txn = Transaction(user_id=sender.id, type='transfer', amount=amount, recipient_id=recipient.id)
    db.session.add(txn)
    db.session.commit()

    # Check for rapid transfers
    check_transfer_fraud(db, sender)

    return jsonify({"message": f"Transferred {amount} to {recipient.username}"}), 200


@wallet_bp.route('/history', methods=['GET'])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    result = []
    for t in transactions:
        result.append({
            "type": t.type,
            "amount": t.amount,
            "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "recipient_id": t.recipient_id,
            "flagged": t.flagged
        })

    return jsonify(result), 200

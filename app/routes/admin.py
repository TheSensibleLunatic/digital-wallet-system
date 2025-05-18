from flask import Blueprint, jsonify
from app.models import Transaction, User
from app import db
from sqlalchemy import func, desc

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/flagged', methods=['GET'])
def flagged_transactions():
    flagged = Transaction.query.filter_by(flagged=True).all()
    result = [{
        "user_id": t.user_id,
        "type": t.type,
        "amount": t.amount,
        "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for t in flagged]
    return jsonify(result)

@admin_bp.route('/admin/total_balance', methods=['GET'])
def total_balance():
    total = db.session.query(func.sum(User.balance)).scalar()
    return jsonify({"total_balance": total})

@admin_bp.route('/admin/top_users', methods=['GET'])
def top_users():
    user_ids = db.session.query(Transaction.user_id, func.count().label('txn_count'))\
        .group_by(Transaction.user_id)\
        .order_by(desc('txn_count')).limit(3).all()

    result = []
    for user_id, count in user_ids:
        user = User.query.get(user_id)
        result.append({
            "username": user.username,
            "transactions": count,
            "balance": user.balance
        })

    return jsonify(result)

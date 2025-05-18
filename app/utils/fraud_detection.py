from datetime import datetime, timedelta
from app.models import Transaction

def check_transfer_fraud(db, user):
    """Flag if 3 or more transfers within 1 minute"""
    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
    recent_transfers = Transaction.query.filter_by(user_id=user.id, type='transfer').filter(
        Transaction.timestamp >= one_minute_ago
    ).all()

    if len(recent_transfers) >= 3:
        for txn in recent_transfers:
            txn.flagged = True
        db.session.commit()

def check_large_withdrawal(txn):
    """Flag if withdrawal is over ₹10,000"""
    if txn.type == 'withdraw' and txn.amount >= 10000:
        txn.flagged = True

def scheduled_fraud_check(db):
    print("⏰ Running daily fraud check...")
    from app.models import Transaction
    suspicious_txns = Transaction.query.filter(Transaction.amount >= 10000, Transaction.type == 'withdraw').all()
    for txn in suspicious_txns:
        txn.flagged = True
    db.session.commit()

def alert_email(user_email, reason):
    print(f"[EMAIL ALERT] Sent to {user_email}: 🚨 {reason}")

def check_large_withdrawal(txn):
    if txn.type == 'withdraw' and txn.amount >= 10000:
        txn.flagged = True
        from app.models import User
        user = User.query.get(txn.user_id)
        alert_email(user.email, f"Large withdrawal of ₹{txn.amount}")



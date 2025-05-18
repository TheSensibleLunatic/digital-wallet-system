from flask import Flask
from .extensions import db, jwt
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.fraud_detection import scheduled_fraud_check


def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallet.db'
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'

    db.init_app(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    print("Registering auth blueprint")
    app.register_blueprint(auth_bp)

    from .routes.wallet import wallet_bp
    app.register_blueprint(wallet_bp)

    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: scheduled_fraud_check(db), trigger="interval", hours=24)
    scheduler.start()


    @app.route('/')
    def hello():
        return 'Flask is running! 🎉'

    return app

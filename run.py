from app import create_app, db

app = create_app()  # ✅ First define app

# ✅ Then use it
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

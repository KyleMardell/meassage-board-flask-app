from run import app
from messageboard import db

with app.app_context():
    db.create_all()
    print("Database tables created.")
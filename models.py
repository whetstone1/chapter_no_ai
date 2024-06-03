from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscription_active = db.Column(db.Boolean, default=True)
    chapters_per_email = db.Column(db.Integer, default=1)
    email_frequency = db.Column(db.Integer, default=7)
    stripe_customer_id = db.Column(db.String(120))
    book_title = db.Column(db.String(120))

# Run migration scripts to update the database schema
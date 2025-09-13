# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<HealthData {self.date} - Steps: {self.steps}, Calories: {self.calories}, HR: {self.heart_rate}>"

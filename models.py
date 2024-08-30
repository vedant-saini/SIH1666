from database import db

class StudentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interests = db.Column(db.String(200), nullable=False)
    dynamic_interests = db.Column(db.String(200), nullable=True)
    strengths = db.Column(db.String(200), nullable=False)
    academic_performance = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(50), nullable=False)

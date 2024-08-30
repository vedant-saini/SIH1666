from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the StudentData model
class StudentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interests = db.Column(db.String(200), nullable=False)
    dynamic_interests = db.Column(db.String(200), nullable=True)
    strengths = db.Column(db.String(200), nullable=False)
    academic_performance = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(50), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        interests = ','.join(request.form.getlist('interests'))
        dynamic_interests = request.form['dynamic_interests']
        strengths = request.form['strengths']
        academic_performance = request.form['academic_performance']
        age = request.form['age']
        location = request.form['location']
        language = request.form['language']

        # Save to database
        student_data = StudentData(
            interests=interests,
            dynamic_interests=dynamic_interests,
            strengths=strengths,
            academic_performance=academic_performance,
            age=age,
            location=location,
            language=language
        )
        db.session.add(student_data)
        db.session.commit()

        # Redirect to the Thank You page
        return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)

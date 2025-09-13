from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<HealthData {self.date}>"

# Create tables
with app.app_context():
    db.create_all()

# Home page → list all records
@app.route('/')
def index():
    data = HealthData.query.all()
    return render_template('index.html', data=data)

# Add new health entry
@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        entry = HealthData(
            date=request.form['date'],
            steps=int(request.form['steps']),
            calories=float(request.form['calories']),
            heart_rate=int(request.form['heart_rate'])
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_data.html')

# Delete record
@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    record = HealthData.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

# Dashboard → interactive charts
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# API for Chart.js → steps data
@app.route('/api/series/steps')
def api_steps_series():
    data = HealthData.query.order_by(HealthData.id).all()
    labels = [d.date for d in data]
    values = [d.steps for d in data]
    return jsonify({"labels": labels, "values": values})

# API for calories (optional)
@app.route('/api/series/calories')
def api_calories_series():
    data = HealthData.query.order_by(HealthData.id).all()
    labels = [d.date for d in data]
    values = [d.calories for d in data]
    return jsonify({"labels": labels, "values": values})

# API for heart rate (optional)
@app.route('/api/series/heart_rate')
def api_heart_rate_series():
    data = HealthData.query.order_by(HealthData.id).all()
    labels = [d.date for d in data]
    values = [d.heart_rate for d in data]
    return jsonify({"labels": labels, "values": values})

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student Model (No validation constraints like nullable=False or unique=True)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)  # No validation for name
    email = db.Column(db.String(100), nullable=True)  # No unique validation for email
    course = db.Column(db.String(100), nullable=True)  # Course is nullable
    phone = db.Column(db.String(100), nullable=True)  # Phone is nullable

    def __repr__(self):
        return f"Student: '{self.name}', email: '{self.email}', phone: '{self.phone}', course: '{self.course}'"

# Create tables in database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Welcome to the Python Flask project"

# Home route to display all students
@app.route('/home')
def home():
    student_home = Student.query.all()  # Query all students from the database
    return render_template('home.html', student_home=student_home)

# Route to add new student
@app.route('/add/student', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get data from form
        name = request.form.get('name')  # Use .get() to avoid errors if field is empty
        email = request.form.get('email')
        course = request.form.get('course')
        phone = request.form.get('phone')
        
        # Create new student object
        new_student = Student(name=name, email=email, course=course, phone=phone)

        # Add new student to the database
        db.session.add(new_student)
        db.session.commit()

        # Redirect to home after adding student
        return redirect(url_for('home'))

    return render_template('add_student.html')  # Render the form page when accessed via GET

# Route to delete a student
@app.route('/delete/student/<int:Student_id>', methods=['GET', 'POST'])
def delete(Student_id):
    student_delete = Student.query.get_or_404(Student_id)  # Get student by ID or return 404 if not found
    db.session.delete(student_delete)  # Delete the student
    db.session.commit()  # Commit the transaction to the database

    return redirect(url_for('home'))  # Redirect to home page after deletion

# Route to update student information
@app.route('/update/student/<int:Student_id>', methods=['GET', 'POST'])
def update(Student_id):
    student_update = Student.query.get_or_404(Student_id)  # Fetch student by ID or return 404 if not found

    if request.method == 'POST':  # If form is submitted via POST
        # Get updated data from form
        student_update.name = request.form['name']
        student_update.email = request.form['email']
        student_update.course = request.form['course']
        student_update.phone = request.form['phone']

        db.session.commit()  # Save the updated student details to database

        return redirect(url_for('home'))  # After update, redirect to home page
    
    return render_template('update_student.html', student=student_update)  # Display the update form pre-filled with current data

if __name__ == "__main__":
    app.run(debug=True)

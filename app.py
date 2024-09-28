import flask
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin123@localhost/staff_mangement1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Define Staff Model
class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)

    def __str__(self):
        return f'{self.name} - {self.designation}'

# Route for home page
@app.route('/')
def home():
    staff_data = Staff.query.all()  # Fetch the data from the database
    return render_template('index.html', sData=staff_data)

@app.route('/add', methods=['POST'])
def add_staff():
    sName = request.form['staffName']
    sDesg = request.form['designation']
    sDept = request.form['dept']
    sSalary = request.form['salary']

    new_staff = Staff(name=sName, designation=sDesg, dept=sDept, salary=sSalary)
    db.session.add(new_staff)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit_staff(id):
    sData = Staff.query.get_or_404(id)
    if request.method == 'POST':
        sData.name = request.form['staffName']
        sData.designation = request.form['designation']
        sData.dept = request.form['dept']
        sData.salary = request.form['salary']
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('edit.html', staff=sData)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_staff(id):
    sData = Staff.query.get_or_404(id)
    db.session.delete(sData)  # Delete the staff record
    db.session.commit()  # Commit the change to the database
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)

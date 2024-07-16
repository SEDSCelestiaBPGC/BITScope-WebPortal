# from flask import Flask, render_template, request, jsonify
# import requests
# from flask_sqlalchemy import SQLAlchemy
# import os
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, Email
# from datetime import datetime, timedelta, timezone

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecretkey'

# # Configuration for MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kali@localhost/telescope'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define the form
# class DataForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     exposure_time = StringField('Exposure Time', validators=[DataRequired()])
#     obj = StringField('Object', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Submit')

# class Data(db.Model):
#     __tablename__ = 'webportal'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(255), nullable=False)
#     exposure_time = db.Column(db.Time)
#     object = db.Column(db.String(255))
#     email = db.Column(db.String(255))
#     request_date = db.Column(db.Date)
#     request_time = db.Column(db.Time)
#     status = db.Column(db.Enum('not captured', 'captured', 'mailed'), default='not captured', nullable=False)
#     image_path = db.Column(db.String(255), default='/image')

#     def __repr__(self):
#         return f'<Data {self.name} - {self.obj}>'

# def arrange_data(data):
#     result = {}
#     for item in data:
#         category = item.get('Category')
#         obj = item.get('Object')
#         image_link = item.get('Image link')

#         if category not in result:
#             result[category] = {}
        
#         result[category][obj] = image_link
    
#     return result

# @app.route('/')
# def home():
#     url = 'https://opensheet.elk.sh/15x9oFZtisE5Bl3s3pc-pJvWzsIKkjzQnFPtz9gMTra4/Sheet1'
#     response = requests.get(url)
#     data = response.json()
#     arranged_data = arrange_data(data)
#     return render_template('index.html', arranged_data=arranged_data)

# @app.route('/send/', methods=['POST'])
# def send():
#     name = request.form.get('name')
#     exposure_time = request.form.get('exposure')
#     object = request.form.get('object')
#     email = request.form.get('email')
#     ist_offset = timedelta(hours=5, minutes=30)
#     ist_timezone = timezone(ist_offset)
#     current_datetime = datetime.now(ist_timezone)

#     new_data = Data(
#         name=name, 
#         exposure_time=exposure_time, 
#         object=object, 
#         email=email, 
#         request_date=current_datetime.date(), 
#         request_time=current_datetime.time(),
#         status=False  # Set default value for is_mail_sent to False
#     )
#     db.session.add(new_data)
#     db.session.commit()

#     return jsonify({'message': 'Data added successfully!'})

# @app.route('/team/')
# def team():
#     return render_template('team.html')

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Configuration for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kali@localhost/telescope'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the form
class DataForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    exposure_time = StringField('Exposure Time', validators=[DataRequired()])
    object = StringField('Object', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class Data(db.Model):
    __tablename__ = 'webportal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    exposure_time = db.Column(db.Time)
    object = db.Column(db.String(255))
    email = db.Column(db.String(255))
    request_date = db.Column(db.Date)
    request_time = db.Column(db.Time)
    status = db.Column(db.Enum('not captured', 'captured', 'mailed'), default='not captured', nullable=False)
    image_path = db.Column(db.String(255), default='/image')

    def __repr__(self):
        return f'<Data {self.name} - {self.obj}>'

def arrange_data(data):
    result = {}
    for item in data:
        category = item.get('Category')
        obj = item.get('Object')
        image_link = item.get('Image link')

        if category not in result:
            result[category] = {}
        
        result[category][obj] = image_link
    
    return result

@app.route('/')
def home():
    url = 'https://opensheet.elk.sh/15x9oFZtisE5Bl3s3pc-pJvWzsIKkjzQnFPtz9gMTra4/Sheet1'
    response = requests.get(url)
    data = response.json()
    arranged_data = arrange_data(data)
    return render_template('index.html', arranged_data=arranged_data)

@app.route('/send/', methods=['POST'])
def send():
    name = request.form.get('name')
    exposure_time = request.form.get('exposure')
    object = request.form.get('object')
    email = request.form.get('email')
    ist_offset = timedelta(hours=5, minutes=30)
    ist_timezone = timezone(ist_offset)
    current_datetime = datetime.now(ist_timezone)

    new_data = Data(
        name=name, 
        exposure_time=exposure_time, 
        object=object, 
        email=email, 
        request_date=current_datetime.date(), 
        request_time=current_datetime.time(),
        status='not captured',  # Default value for status
        image_path='/image'  # Default value for image_path
    )
    db.session.add(new_data)
    db.session.commit()

    return jsonify({'message': 'Data added successfully!'})

@app.route('/team/')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

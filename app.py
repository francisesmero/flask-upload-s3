from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from app_secrets import get_secrets
from botocore.exceptions import NoCredentialsError
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
import json
import boto3
import os

bucket_name = 'tm-csv-bucket'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tmdbadmin:Admin123!@tm-checkin-db.cyctbi29vh01.ap-southeast-1.rds.amazonaws.com/tmcheckindb'
db = SQLAlchemy(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)

class CheckinModel(db.Model):
        __tablename__ = 'table-checkin'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        user = db.Column(db.String(255))
        timestamp = db.Column(db.TIMESTAMP(6))
        hours = db.Column(db.DECIMAL(5))
        project = db.Column(db.String(255))

class MyTable(Table):
        id = Col('id')
        user = Col('user')
        timestamp = Col('timestamp')
        hours = Col('hours')
        project = Col('project')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():

    file = request.files['file']
    secret = json.loads(get_secrets())
    access_key = secret['aws_access_key_id']
    secret_key = secret['aws_secret_access_key']

    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
            file_name = file.filename
            file_path = os.path.join('static/tmp', file_name)
            file.save(file_path)

            s3.upload_file(file_path, bucket_name, 'raw_data/' + file_name)
            return render_template('index.html', success='File Upload Succesfully')
            return True
        
    except FileNotFoundError:
            return render_template('index.html', error='File not found')
            return False

    except NoCredentialsError:
            return render_template('index.html', error='No Credentials')
            return False


@app.route('/dashboard')
def dashboard():
        checkin_model = CheckinModel.query.all()
        return render_template('dashboard.html', checkin_model=checkin_model)

if __name__ == '__main__':
                port = os.getenv('PORT', default=8080)
                app.run(debug=True)
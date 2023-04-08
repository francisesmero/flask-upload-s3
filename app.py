from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from app_secrets import get_secrets
from botocore.exceptions import NoCredentialsError
import json
import boto3
import os

bucket_name = 'tm-csv-bucket'


app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)

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

if __name__ == '__main__':
    port = os.getenv('PORT', default=8080)
    app.run(debug=True, port=port)
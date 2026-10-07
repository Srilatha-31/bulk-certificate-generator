# Bulk Certificate Generator

A Django REST API for generating certificates in bulk from CSV files. The application validates recipient data, generates individual PDF certificates, tracks job progress, handles failed records, and provides APIs to view and download certificates.

## Features

* Bulk certificate generation from CSV
* CSV and recipient data validation
* PDF certificate generation
* Unique certificate IDs
* Job status and progress tracking
* Processed, successful, and failed certificate tracking
* Individual certificate details
* Certificate PDF download
* Automated API tests

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* ReportLab

## CSV Format

The uploaded CSV file must contain the following columns:

recipient_name,recipient_email
Srilatha,srilatha@gmail.com
Rahul,rahul@gmail.com
Priya,priya@gmail.com


### Create a Job

POST /api/jobs/

Creates a certificate generation job.

### List Jobs

GET /api/jobs/

Returns all certificate generation jobs.

### Upload CSV and Generate Certificates

POST /api/jobs/upload/

Uploads a CSV file, validates the recipient data, generates certificates, and updates the job status and progress.

### Get Job Details

GET /api/jobs/<id>/

Returns job information including:

* Total certificates
* Processed certificates
* Successful certificates
* Failed certificates
* Progress
* Job status
* Certificate details

### Get Certificate Details

GET /api/certificates/<id>/

Returns details of an individual certificate.

### Download Certificate

GET /api/certificates/<id>/download/

Downloads the generated certificate PDF.

## Validation and Error Handling

The application handles:

* Missing CSV file
* Invalid file type
* Missing required CSV columns
* Empty recipient name
* Missing recipient email
* Invalid email format
* Invalid CSV encoding
* Certificate generation failures

Failed records are stored with an error message while successful records continue to be processed.

## Setup

Clone the repository:

git clone <your-github-repository-url>
cd bulk_certificate_generator


Create a virtual environment:

python -m venv env


Activate the virtual environment on Windows:

env\Scripts\activate


Install the required dependencies:

pip install -r requirements.txt


Run database migrations:

python manage.py migrate


Start the development server:

python manage.py runserver


The API will be available at:

http://127.0.0.1:8000/

## Testing

Run the automated tests using:

python manage.py test certificates


## Author

Darsi Sri Latha


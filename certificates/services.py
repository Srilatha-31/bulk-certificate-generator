import csv
import uuid
from io import BytesIO
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile

from .models import CertificateJob, Certificate

def generate_certificate_pdf(certificate):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=(842, 595))
    pdf.setTitle("Certificate of Achievement")

    
    # PREDEFINED CERTIFICATE TEMPLATE
    pdf.setLineWidth(3)
    pdf.rect(30, 30, 782, 535)

    
    pdf.setLineWidth(1)
    pdf.rect(45, 45, 752, 535 - 30)

    
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        421,
        470,
        "CERTIFICATE OF ACHIEVEMENT"
    )


    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
        421,
        420,
        "This certificate is proudly presented to"
    )


    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(
        421,
        365,
        certificate.recipient_name
    )

    
    pdf.setLineWidth(1)
    pdf.line(220, 345, 622, 345)

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        421,
        285,
        f"Certificate ID: {certificate.certificate_id}"
    )

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        421,
        235,
        "Congratulations!"
    )

    
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        421,
        90,
        "Bulk Certificate Generator"
    )

    pdf.save()

    buffer.seek(0)

    certificate.file.save(
        f"{certificate.certificate_id}.pdf",
        ContentFile(buffer.read()),
        save=True
    )

def process_csv_file(job, file):
    try:
        decoded_file = file.read().decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        job.status = "failed"
        job.save()
        return job

    reader = csv.DictReader(decoded_file)
    rows = list(reader)

    required_columns = {"recipient_name", "recipient_email"}

    if not reader.fieldnames:
        job.status = "failed"
        job.save()
        return job

    missing_columns = required_columns - set(reader.fieldnames)

    if missing_columns:
        job.status = "failed"
        job.error_message = (
            f"Missing required columns: {', '.join(missing_columns)}"
        )
        job.save()
        return job

    if len(rows) == 0:
        job.status = "failed"
        job.save()
        return job

    total = 0
    successful = 0
    failed = 0

    job.total_certificates = len(rows)
    job.processed_certificates = 0
    job.successful_certificates = 0
    job.failed_certificates = 0
    job.progress = 0
    job.status = "processing"
    job.save()

    for row in rows:
        total += 1

        recipient_name = row.get("recipient_name", "").strip()
        recipient_email = row.get("recipient_email", "").strip()

        certificate = None

        try:
            if not recipient_name:
                raise ValueError("Recipient name is missing")

            if not recipient_email:
                raise ValueError("Recipient email is missing")

            if "@" not in recipient_email:
                raise ValueError("Invalid email address")

            certificate = Certificate.objects.create(
                job=job,
                recipient_name=recipient_name,
                recipient_email=recipient_email,
                certificate_id=str(uuid.uuid4()),
                status="pending",
            )

            generate_certificate_pdf(certificate)

            certificate.status = "success"
            certificate.save()

            successful += 1

        except Exception as e:
            failed += 1

            if certificate:
                certificate.status = "failed"
                certificate.error_message = str(e)
                certificate.save()
            else:
                Certificate.objects.create(
                    job=job,
                    recipient_name=recipient_name,
                    recipient_email=recipient_email,
                    certificate_id=str(uuid.uuid4()),
                    status="failed",
                    error_message=str(e),
                )

        job.processed_certificates = total
        job.successful_certificates = successful
        job.failed_certificates = failed
        job.progress = int((total / len(rows)) * 100)
        job.save()

    if failed == 0:
        job.status = "completed"
    elif successful > 0:
        job.status = "completed"
    else:
        job.status = "failed"

    job.save()

    return job
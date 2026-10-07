from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import CertificateJob, Certificate


class CertificateAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_job(self):
        response = self.client.post(
            "/api/jobs/",
            {
                "name": "Test Job",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(CertificateJob.objects.count(), 1)

    def test_input_validation_invalid_file(self):
        file = SimpleUploadedFile(
            "students.txt",
            b"some invalid content",
            content_type="text/plain",
        )

        response = self.client.post(
            "/api/jobs/upload/",
            {
                "name": "Invalid File Test",
                "file": file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)

    def test_upload_and_certificate_generation(self):
        csv_content = (
            "recipient_name,recipient_email\n"
            "Srilatha,srilatha@gmail.com\n"
            "Rahul,rahul@gmail.com\n"
        )

        csv_file = SimpleUploadedFile(
            "students.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )

        response = self.client.post(
            "/api/jobs/upload/",
            {
                "name": "Certificate Generation Test",
                "file": csv_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)

        job = CertificateJob.objects.get(
            id=response.data["job_id"]
        )

        self.assertEqual(job.total_certificates, 2)
        self.assertEqual(job.processed_certificates, 2)
        self.assertEqual(job.successful_certificates, 2)
        self.assertEqual(job.failed_certificates, 0)
        self.assertEqual(job.progress, 100)
        self.assertEqual(job.status, "completed")

        certificates = Certificate.objects.filter(job=job)

        self.assertEqual(certificates.count(), 2)

        for certificate in certificates:
            self.assertEqual(certificate.status, "success")
            self.assertTrue(certificate.file)

    def test_job_status_and_progress(self):
        job = CertificateJob.objects.create(
            name="Progress Test",
            status="completed",
            total_certificates=5,
            processed_certificates=5,
            successful_certificates=4,
            failed_certificates=1,
            progress=100,
        )

        response = self.client.get(
            f"/api/jobs/{job.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "completed")
        self.assertEqual(response.data["total_certificates"], 5)
        self.assertEqual(response.data["processed_certificates"], 5)
        self.assertEqual(response.data["successful_certificates"], 4)
        self.assertEqual(response.data["failed_certificates"], 1)
        self.assertEqual(response.data["progress"], 100)

    def test_individual_certificate_failure(self):
        csv_content = (
            "recipient_name,recipient_email\n"
            "Srilatha,srilatha@gmail.com\n"
            "Rahul,\n"
            "Priya,priya@gmail.com\n"
        )

        csv_file = SimpleUploadedFile(
            "students.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )

        response = self.client.post(
            "/api/jobs/upload/",
            {
                "name": "Failure Test",
                "file": csv_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)

        job = CertificateJob.objects.get(
            id=response.data["job_id"]
        )

        self.assertEqual(job.total_certificates, 3)
        self.assertEqual(job.processed_certificates, 3)
        self.assertEqual(job.successful_certificates, 2)
        self.assertEqual(job.failed_certificates, 1)
        self.assertEqual(job.progress, 100)
        self.assertEqual(job.status, "completed")

        failed_certificate = Certificate.objects.get(
            job=job,
            status="failed",
        )

        self.assertIn(
            "email",
            failed_certificate.error_message.lower()
        )

    def test_retrieve_certificate(self):
        job = CertificateJob.objects.create(
            name="Retrieval Test",
            status="completed",
        )

        certificate = Certificate.objects.create(
            job=job,
            recipient_name="Srilatha",
            recipient_email="srilatha@gmail.com",
            certificate_id="TEST-123",
            status="success",
        )

        response = self.client.get(
            f"/api/certificates/{certificate.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["recipient_name"],
            "Srilatha",
        )
        self.assertEqual(
            response.data["certificate_id"],
            "TEST-123",
        )
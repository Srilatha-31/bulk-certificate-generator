from django.db import models

# Create your models here.

class CertificateJob(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    name = models.CharField(max_length=200)
    total_certificates = models.IntegerField(default=0)
    processed_certificates = models.IntegerField(default=0)
    successful_certificates = models.IntegerField(default=0)
    failed_certificates = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    job = models.ForeignKey(
        CertificateJob,
        on_delete=models.CASCADE,
        related_name="certificates"
    )

    recipient_name = models.CharField(max_length=200)
    recipient_email = models.EmailField()
    certificate_id = models.CharField(max_length=100, unique=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    file = models.FileField(
        upload_to="certificates/",
        blank=True,
        null=True
    )

    error_message = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipient_name
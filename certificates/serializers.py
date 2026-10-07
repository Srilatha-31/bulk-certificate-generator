from rest_framework import serializers
from .models import CertificateJob, Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            "id",
            "recipient_name",
            "recipient_email",
            "certificate_id",
            "status",
            "file",
            "error_message",
            "created_at",
        ]


class CertificateJobSerializer(serializers.ModelSerializer):
    certificates = CertificateSerializer(many=True, read_only=True)

    class Meta:
        model = CertificateJob
        fields = [
            "id",
            "name",
            "total_certificates",
            "processed_certificates",
            "successful_certificates",
            "failed_certificates",
            "progress",
            "status",
            "created_at",
            "certificates",
        ]


class BulkUploadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.lower().endswith(".csv"):
            raise serializers.ValidationError(
                "Only CSV files are allowed."
            )

        return value
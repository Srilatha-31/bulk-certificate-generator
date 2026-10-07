from django.shortcuts import render
from rest_framework import generics,status
from .models import CertificateJob, Certificate
from .serializers import CertificateJobSerializer,BulkUploadSerializer,CertificateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import process_csv_file
from django.http import FileResponse

class CertificateJobListCreateView(generics.ListCreateAPIView):
    queryset = CertificateJob.objects.all().order_by("-created_at")
    serializer_class = CertificateJobSerializer

class BulkCertificateUploadView(APIView):

    def post(self, request):
        serializer = BulkUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        name = serializer.validated_data["name"]
        file = serializer.validated_data["file"]

        job = CertificateJob.objects.create(
            name=name,
            status="processing"
        )

        process_csv_file(job, file)

        return Response(
            {
                "message": "File processed successfully",
                "job_id": job.id,
                "status": job.status
            },
            status=status.HTTP_201_CREATED
        )


class CertificateJobDetailView(generics.RetrieveAPIView):
    queryset = CertificateJob.objects.all()
    serializer_class = CertificateJobSerializer



class CertificateDownloadView(APIView):

    def get(self, request, pk):
        from .models import Certificate

        try:
            certificate = Certificate.objects.get(pk=pk)
        except Certificate.DoesNotExist:
            return Response(
                {"error": "Certificate not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not certificate.file:
            return Response(
                {"error": "Certificate PDF not available"},
                status=status.HTTP_404_NOT_FOUND
            )

        return FileResponse(
            certificate.file.open("rb"),
            as_attachment=True,
            filename=f"{certificate.certificate_id}.pdf"
        )


class CertificateDetailView(generics.RetrieveAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
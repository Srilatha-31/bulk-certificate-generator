from django.urls import path
from .views import CertificateJobListCreateView,BulkCertificateUploadView,CertificateJobDetailView,CertificateDownloadView,CertificateDetailView

urlpatterns = [
    path("jobs/", CertificateJobListCreateView.as_view(), name="job-list-create"),
    path("jobs/upload/",BulkCertificateUploadView.as_view(),name="bulk-upload"),
    path("jobs/<int:pk>/",CertificateJobDetailView.as_view(),name="job-detail"),
    path("certificates/<int:pk>/download/",CertificateDownloadView.as_view(),name="certificate-download"),
    path("certificates/<int:pk>/",CertificateDetailView.as_view(),name="certificate-detail"),
]
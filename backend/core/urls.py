from django.urls import path
from core.views import DocumentUploadView, QueryView

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='file-upload'),
    path('query/', QueryView.as_view(), name='query'),
]
from django.urls import path

from .views import po_loading, process, update, qc_check

urlpatterns = [
    
    path("", po_loading, name="po_loading"),
    path("qc_check/", qc_check, name="qc_check"),
    path("process/", process, name="process"),
    path("update/", update, name="update"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('form_result/',views.form_result , name="form_result"),
    path('view_result/<int:result_id>/', views.view_result, name='view_result'),
    path("download/<int:result_id>/", views.download_result, name="download_result")
]
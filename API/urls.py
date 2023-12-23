from django.urls import path
from .views import GetStudents, GetStudentDetails

urlpatterns = [
    path('get-students/', GetStudents.as_view(), name='get_students'),
    path('get-info/<int:student_id>/', GetStudentDetails.as_view(), name='get_student_details'),
]

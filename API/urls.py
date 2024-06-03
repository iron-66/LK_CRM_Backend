from django.urls import path
from .views import GetStudents, GetStudentDetails, ExportStudentsXLSX, UpdateStudentStatus

urlpatterns = [
    path('get-students/', GetStudents.as_view(), name='get_students'),
    path('get-info/<int:student_id>/', GetStudentDetails.as_view(), name='get_student_details'),
    path('update-status/<str:data>/', UpdateStudentStatus.as_view(), name='update_student_status'),
    path('export-students-xlsx/', ExportStudentsXLSX.as_view(), name='export_students_xlsx'),
]

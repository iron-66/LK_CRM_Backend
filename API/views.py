from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from django.db import connections
from django.http import HttpResponse
import openpyxl


class GetStudents(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStudentDetails(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExportStudentsXLSX(APIView):
    def get(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Students'

        headers = ['Full Name', 'Course', 'University', 'Email', 'Telegram', 'Status', 'Is Test Send', 'Speciality', 'Degree', 'Phone', 'VK']
        ws.append(headers)

        for student in Student.objects.all():
            row = [
                student.full_name,
                student.course,
                student.university,
                student.email,
                student.telegram,
                student.status,
                'Yes' if student.is_test_send else 'No',
                student.speciality,
                student.degree,
                student.phone,
                student.vk
            ]
            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=students.xlsx'
        wb.save(response)
        return response


def check_database_connection():
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("Подключение к базе данных успешно!")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {str(e)}")

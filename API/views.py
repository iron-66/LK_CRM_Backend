from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from django.db import connections


# def students_list(request):
#     check_database_connection()
#     students = Student.objects.all()
#     data = [{'full_name': student.full_name, 'course': student.course, 'university': student.university,
#              'email': student.email, 'telegram': student.telegram, 'speciality': student.speciality,
#              'degree': student.degree, 'phone': student.phone, 'vk': student.vk} for student in students]
#     print(data)
#     return JsonResponse(data, safe=False)


class GetStudents(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def check_database_connection():
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("Подключение к базе данных успешно!")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {str(e)}")

from django.db import models


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    course = models.IntegerField
    university = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telegram = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='new')
    is_test_send = models.BooleanField(default=False)
    speciality = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    vk = models.CharField(max_length=255)

    def __str__(self):
        #return f"{self.full_name} - {self.course} - {self.university} - {self.email} - {self.telegram} - {self.status} - {self.is_test_send} - {self.speciality} - {self.degree} - {self.phone} - {self.vk}"
        return self.full_name

from django.db import models


class TestResult(models.Model):
    telegram_id = models.IntegerField()
    task1 = models.IntegerField()
    task2 = models.IntegerField()
    task3 = models.CharField(max_length=255)
    task4 = models.IntegerField()
    task5 = models.IntegerField()

    def __str__(self):
        return f"Result for {self.telegram_id}"

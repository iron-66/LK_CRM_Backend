from django.shortcuts import render, redirect
from django.views import View
from .forms import TestResultForm
from API.models import Student


class TestFormView(View):
    template_name = 'form/index.html'

    def get(self, request, telegram_id):
        form = TestResultForm(initial={'telegram_id': telegram_id})
        return render(request, self.template_name, {'form': form, 'telegram_id': telegram_id})

    def post(self, request, telegram_id):
        if request.method == 'POST':
            form = TestResultForm(request.POST)

            if form.is_valid():
                form.save()

                try:
                    student = Student.objects.get(telegram=telegram_id)
                    student.is_test_send = True
                    student.status = 'done_test'
                    student.save()
                    #bot.send_message(telegram_id, "Ссылка на организационный чат: https://t.me/H8c789cv8Nvg")

                    print("is_test_send updated successfully for student with telegram_id:", telegram_id)
                except Student.DoesNotExist:
                    print("Student with telegram_id", telegram_id, "not found")

                return redirect('https://t.me/H8c789cv8Nvg')
        else:
            form = TestResultForm(initial={'telegram_id': telegram_id})

        return render(request, self.template_name, {'form': form, 'telegram_id': telegram_id})

from django.shortcuts import render, redirect
from django.views import View
from .forms import TestResultForm


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
                return redirect('success_page')

        else:
            form = TestResultForm(initial={'telegram_id': telegram_id})

        return render(request, self.template_name, {'form': form, 'telegram_id': telegram_id})

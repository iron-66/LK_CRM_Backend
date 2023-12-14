from django.shortcuts import render, redirect
from django.db import connection
from .forms import StudentForm


def index(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            course = form.cleaned_data['course']
            study_org = form.cleaned_data['study_org']
            email = form.cleaned_data['email']
            telegram = form.cleaned_data['telegram']
            status = 'new'

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO students (full_name, course, study_org, email, telegram, status) VALUES (%s, %s, %s, %s, %s, %s)",
                    [fullname, course, study_org, email, telegram, status]
                )
            # return redirect('success_page')
        else:
            print("Форма не действительна. Ошибки:", form.errors)
    else:
        form = StudentForm()

    return render(request, 'form/index.html', {'form': form})

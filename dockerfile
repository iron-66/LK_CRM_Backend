FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 30960
CMD ["python3", "manage.py", "runserver", "0.0.0.0:30960"]
